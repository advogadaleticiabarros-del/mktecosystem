# Capas dos Reels e simulação do feed

## Pedido

"Precisamos apenas definir as capas dos Reels agora", "tem que ser harmonioso como o feed vai ficar", "inclua na grade do feed e me dê um documento para mostrar para a Dra.".

## Feito

- `producao/estilos/papel-e-ouro/motion-diario/capas.py` gera `<episódio>/capa.jpg` (1080×1920) para os 33 Reels Flagrante. O fundo é papel claro, com faixas douradas no limite do recorte 3:4 da grade (y 240 e 1666). Cada capa traz um tema curto (dicionário `TEMAS`), a fala do conflito tirada do vídeo e a pergunta em marca-texto dourado. Tema, fala e pergunta ficam centrados na área visível. Os vídeos não foram alterados.
- Documento para a Dra.: https://claude.ai/artifact/URPDUfCgHpyhk2BSxXK2Gx (grade de 15 peças misturando Reels, posts revisados do editor e carrosséis, mais 3 capas inteiras com a área da grade marcada). É privado: a Jessica precisa compartilhar.

## Verificado

- 33 capas geradas e conferidas por imagem numa grade simulada.
- Não verificado: celular real; capa publicada no Instagram.

## Decisões e porquês

- Antes, a capa era o quadro de 1,2 s (`CAPA_PADRAO_MS` em `apps/api/app/services/midia_instagram.py`), que na grade sai quase todo café e vazio.
- Capa em papel claro para alternar com carrosséis escuros e combinar com Manchete e Papel e Ouro.
- A Jessica achou a grade com os carrosséis atuais harmoniosa: os carrosséis não foram mudados.

## Pendente

- Dra.: aprovar a grade e as capas.
- Para publicar com a capa, o publicador precisa enviar `cover_url` (imagem) em vez de `thumb_offset`. Não foi implementado: precisa de aprovação e de deploy.

## Próxima sessão

Com aprovação, adicionar `cover_url` em `instagram_api.publicar_reels` e `midia_instagram` (TDD), subir as capas em `/media` e ligar cada Reels agendado à sua capa. Skills: `codebase-design`, `tdd`.
