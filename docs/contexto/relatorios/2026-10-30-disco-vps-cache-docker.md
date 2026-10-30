# 30/10/2026: disco da VPS e cache de build do Docker

## Pedido
A Jessica perguntou quanto de memória o Orbit usa na VPS. O painel da Hostinger mostrava 50% de memória e o disco em 86/100 GB, e ela disse: "é o uso do disco que está influenciando". Depois perguntou: "como resolvemos isso (cache de build do Docker)".

## Feito
- Consulta: o Orbit usa cerca de 250 MB de RAM (`vps-api-1` com 175 MB e `vps-db-1` com 75 MB), uns 3% da VPS.
- Disco em 90% (11 GB livres). Causas: o cache de build do Docker tinha 44,6 GB (112 entradas, sobras dos `docker compose up -d --build`), e havia 23 dumps `crm-backup-*.sql` em `/tmp`, de ~930 MB cada, somando 21 GB.
- Limpeza com `docker builder prune -af` na VPS: o cache foi a 0 B e o disco caiu para 45 GB usados (47%).
- O que aconteceu foi registrado em `docs/CONTEXTO_PROJETO.md` (seção do disco da VPS).

## Verificado
- `df -h /` depois da limpeza: 45G usados, 51G livres, 47%.
- `docker system df`: Build Cache em 0B. Os contêineres do Orbit não foram tocados.
- O cron atual (domingo às 4h, `--filter until=168h`) está rodando, mas não segura o crescimento, porque todas as entradas tinham menos de 7 dias.

## Decisões e porquês
- Foi usado `prune -af` (tudo), porque nenhuma entrada estava ativa. O custo é só que o próximo `--build` do Orbit demora alguns minutos a mais.
- A troca do cron para diário com teto de 5 GB (`--max-used-space 5GB`) foi **bloqueada pelo modo automático**, por se tratar de uma mudança persistente em produção. Ela precisa do ok explícito da Jessica.

## Pendente
1. **Cron com teto de 5 GB** (decide a Jessica): `crontab -e` do root, trocando a linha de domingo por `0 4 * * * /usr/bin/docker builder prune -f --max-used-space 5GB >> /var/log/docker-builder-prune.log 2>&1`.
2. **Backup do CRM da Letícia falhando** (projeto CRMLRTICIA, não é do Orbit): o último `.sql.gz.enc` em `/home/crmapp/backups-crm` é de 28/10 às 22h. O syslog registra OOM-kill do `node /home/crmapp...` (pm2-crmapp, com 4,2 GB de RSS) às 05:47 de 30/10, na hora do backup das 05:45. Hipótese: o processo de backup estoura a memória, morre e deixa o dump cru em `/tmp`. Não investigado.
3. Os 21 GB de dumps em `/tmp` continuam lá. Foram mantidos porque, sem backup válido desde 28/10, o mais recente pode ser o único recente.
4. `laya-serve` (`/opt/laya`, usuário crmapp) usa 1,7 GB de RAM. A origem não foi verificada.

## Próxima sessão
Com o ok da Jessica, aplicar o cron (item 1). Depois, abrir o CRMLRTICIA (ler `docs/contexto/LEIA-PRIMEIRO.md` e `ESTADO.md`) e diagnosticar o OOM do backup (skill `diagnosing-bugs`). Só depois de um backup válido, apagar os dumps antigos de `/tmp`.
