# Estáticos planejados refeitos no estilo Manchete

## Pedido

"Pegue tudo que temos produzido e coloque nesses novos estilos, principalmente os estáticos."

## Feito

- `producao/estilos/manchete/conteudo_planejado.py` lê `apps/api/_saida_producao_1510/conteudo_<mes>.py` e monta, com o texto já aprovado, três modelos Manchete:
  - pergunta: a foto Pexels da peça dissolvendo no café, com a pergunta empilhada à esquerda;
  - frase: papel claro, fecho em faixa dourada;
  - Mito ou Lei: café, afirmação (riscada fino se for mito), carimbo MITO / É LEI, explicação e lei.
- Texto longo encolhe sozinho (`data-max`). A peça já gravada nunca é sobrescrita.
- 72 peças em `manchete/pecas/`: dezembro inteiro (13 perguntas, 13 frases, 14 Mito ou Lei) e novembro de 10/11 a 02/12 (32). O que é anterior a 10/11 já saiu e ficou de fora.
- As 72 entraram no editor (`manchete-nov-*`, `manchete-dez-*`; o editor tem 109 peças). `importar_estilos.py` ganhou `LOTES` para importar scripts com argumentos.
- Página de revisão: https://claude.ai/artifact/P2iDXq82BeeT4NjX5qumTA (privada).

## Verificado

- Todas as peças conferidas por folha de contato. A pergunta e a frase de 03/12, renderizadas pelo editor, têm diferença média de 0,7 e 1,1 em 255 em relação à peça pronta.
- Não verificado: celular real; revisão jurídica dos textos (são os mesmos já aprovados pela Dra.).

## Decisões e porquês

- Carrosséis ficaram como estão (a Jessica achou a grade harmoniosa com eles). Reels ganharam capa própria (relatório das capas).
- Nada foi trocado no Orbit: o acesso ao servidor foi negado pela permissão automática nesta sessão. Novembro está aprovado e agendado com a arte antiga, e trocar exige o ok da Dra. e esse acesso.
- Alterações de outras sessões em `manchete/gerar.py`, `legendas.md`, `flagrante_estaticos.py` e `motion-diario/` ficaram fora dos commits.

## Pendente

- Dra.: aprovar a arte nova.
- Jessica: liberar o acesso ao servidor para trocar a arte das peças agendadas (novembro) e dos rascunhos (dezembro), com backup antes.

## Próxima sessão

Com aprovação e acesso: backup do banco, subir os JPG para `/media` e trocar `corpo.imagem` das peças de pergunta, frase e Mito ou Lei (por data e chave). Para outro mês: `python conteudo_planejado.py <mes>` e `python ../../editor/importar_estilos.py` com um `LOTES` novo.

## Aprovação e troca no Orbit (mesmo dia)

- A Jessica aprovou ("Aprovadíssimo!") e pediu para alterar todas. O editorial produzido vai até 31/12/2026; não há plano de janeiro.
- `apps/api/_saida_producao_1510/trocar_arte_manchete.py` (commit 64692bd), roda no container. Troca só `corpo.imagem` das perguntas, frases e Mito ou Lei de 10/11 em diante, guarda a URL antiga em `corpo.imagem_anterior` e pula peça publicada ou ambígua. Sem `--aplicar`, só simula.
- Os 72 JPG estão prontos em `producao/estilos/manchete/envio/` com o prefixo `manchete-` (fora do git).
- Não aplicado: o SSH para a VPS foi negado duas vezes pela permissão automática. Falta a Jessica liberar `Bash(ssh -i ~/.ssh/orbit_vps:*)` e `Bash(scp -i ~/.ssh/orbit_vps:*)`.
- (Histórico) Passos quando liberar: backup do banco (`pg_dumpall`, conferir tamanho), scp dos JPG e de `conteudo_nov.py`, `conteudo_dez.py` e `trocar_arte_manchete.py` para `/tmp/manchete`, `docker compose cp` dos JPG para `api:/app/media`, rodar sem `--aplicar`, conferir e rodar com `--aplicar`, abrir 2 URLs públicas.

## Troca aplicada no Orbit (09/11/2026, noite)

A Jessica liberou o acesso ("Está permitido troque agora e programe corretamente").

- Backup antes: `/root/orbit-backups/antes-manchete-20261109.sql.gz` (1,2 MB).
- 72 JPG copiados para `api:/app/media`. A simulação encontrou as 72 peças, todas `aprovado`, sem aviso. `--aplicar` trocou 72, e uma segunda simulação trocaria 0.
- Conferido no ar (HTTP 200, image/jpeg): mito de 20/11, frase de 21/11, pergunta de 24/12, mito de 30/12.
- Programação: o publicador usa `corpo.imagem` na hora de publicar (`midia_instagram.py`), então as peças agendadas já saem com a arte Manchete. Nenhuma data, horário ou status foi mudado.
- Calendário (`calendario.py`, só leitura): o feed tem 1 post por dia até 31/12. 18 das 72 peças estão agendadas: 12 Mito ou Lei, 5 frases e 1 pergunta. As outras 54 (34 perguntas, 27 frases e 25 estáticos aprovados ao todo sem agendamento) não cabem pela regra de 1 por dia e ficam como reserva.
- Dias sem post no feed: só 25/11 e 09/12. `agendar_vagas.py` põe ali as perguntas "aposentadoria da mulher 2026" e "assédio moral" às 14h. **Não aplicado**: a permissão automática bloqueou porque cria agendamento novo, além da troca aprovada. Falta o ok da Jessica.
- Observado e não mexido: em 8 dias de Reels também há post de feed às 14h (17/11, 20/11, 08/12, 11/12, 15/12, 18/12, 22/12 e 29/12), contra a regra "em dia de Reels, só o Reels". Esses agendamentos já existiam.
- Para voltar a arte antiga: `corpo.imagem_anterior` de cada peça, ou o backup acima.

## Grade visual do feed até 01/01/2027 (10/11/2026)

- Pedido: "Coloque em um documento ... formato de grade Instagram com data e hora".
- Página privada: https://claude.ai/artifact/ANhFGaQydP9XewYQoE59Kg. Mostra os 74 posts do feed de 25/10 a 31/12: 16 já publicados, 1 segurado e 58 agendados (26 carrosséis, 13 Reels e 19 estáticos). O mais novo fica no topo, cada quadro tem dia e hora, e dá para esconder os rótulos e os já publicados.
- Dados lidos do Orbit, só leitura: `scheduled_posts` do Instagram sem Stories, com a primeira imagem de `corpo`. Reels aparecem como um quadro do próprio vídeo (1,2 s), recortado em 3:4.
- Achado: 18/11 tem um Mito ou Lei com a arte antiga (pauta de 08/11 remarcada, fora da troca). 01/01/2027 não tem post. Em janeiro só há Reels em 05/01 e 08/01.
