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
- O cron passou a ser diário com teto de 5 GB (`--max-used-space 5GB`) em vez de semanal com filtro de idade: mesmo com muitos builds na semana, o cache nunca passa de 5 GB. O modo automático bloqueou a primeira tentativa, e a troca foi aplicada depois do ok da Jessica ("ok, faça a limpeza diária").

## Pendente
1. ~~Cron com teto de 5 GB~~: aplicado em 30/10. O crontab do root agora tem `0 4 * * * /usr/bin/docker builder prune -f --max-used-space 5GB >> /var/log/docker-builder-prune.log 2>&1`.
2. **Backup do CRM da Letícia** (projeto CRMLRTICIA): o OOM-kill do Node na hora do backup acontecia desde pelo menos 20/10 (4,5 a 5,3 GB de RSS). Outra sessão corrigiu no commit `8b70e13` do CRMLRTICIA (backup em fluxo, mais a limpeza das sobras em `/tmp`). O deploy estava em andamento às 11h54 UTC de 30/10. Falta conferir se o próximo backup sai completo; nada foi mexido daqui.
3. Os 21 GB de dumps em `/tmp`: a própria correção do CRM (`limparSobrasDeTentativas`) apaga essas sobras no próximo backup.
4. `laya-serve` (`/opt/laya`, usuário crmapp) usa 1,7 GB de RAM. A origem não foi verificada.

## Próxima sessão
Conferir `/var/log/docker-builder-prune.log` depois das 4h de 31/10. No CRMLRTICIA, conferir se o backup seguinte ao deploy de `8b70e13` gerou o `.sql.gz.enc` e se `/tmp` ficou sem `crm-backup-*.sql`.
