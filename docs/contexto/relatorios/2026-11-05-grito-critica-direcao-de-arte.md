# "GRITAR não é cobrar": crítica de direção de arte aplicada

## Pedido

A Jessica colou uma crítica de direção de arte da peça `grito-A-perfil` e pediu: "Aplique em uma arte para vermos o que melhora".

## Feito

- Peça nova `grito-D-editorial` em `producao/estilos/palavra-de-ouro/gerar.py`; a `grito-A-perfil` não foi alterada.
- `foto_grito` ganhou `teto` (comprime só as altas luzes da pele) e `main` ganhou `ACAB_PROPRIO` (peça que desenha as próprias faixas). As outras peças continuam com o acabamento de antes.
- Arquivos, só neste computador (o git ignora JPG em `producao/`): `pecas/grito-D-editorial.jpg` e `pecas/grito-comparativo-A-D.jpg`.

Aplicado da crítica: GRITAR 15% menor (318 para 270 px), eixo único em x=320 para texto e assinatura, brilho de ouro só em GRITAR e ouro sólido no resto, rosto menor (860 para 740 px) e com altas luzes suavizadas, assinatura editorial com fio, frase de apoio nova, "ASSÉDIO MORAL" maior (24 para 32 px).

## Verificado

- Render conferido por imagem, inclusive acentos.
- Não verificado: celular real, licença da foto (pendência já registrada em `docs/ESTILO_PALAVRA_DE_OURO.md`), avaliação da Dra.

## Decisões e porquês

- **Fonte:** continua EB Garamond + Inter. A crítica sugeria Cormorant, que a Dra. reprovou por causa dos acentos. A peça já usava só duas famílias.
- **Faixas:** ficaram finas (6 px, ouro sólido), mas não saíram. A Dra. já reclamou quando sumiram ("não tire minha identidade"). Afinar é só teste e não virou regra do estilo.
- **Foto:** mantida, para a comparação mostrar só o efeito da diagramação. A troca por cena de gestor e trabalhador não foi feita. A crítica do "filme de terror" continua válida, porque o capuz segue na foto.
- **Texto:** acrescentado "Abuso repetido pode configurar assédio moral." A frase curta sugerida tirava a ressalva jurídica, e a OAB tem prioridade sobre o design.
- **Publicação:** sem agendamento e sem link público, porque a peça não foi aprovada.

## Pendente

- Jessica: aprovar ou não a diagramação; decidir faixa fina e troca de foto.
- Dra.: revisar o texto novo e avaliar o estilo.

## Próxima sessão

Se aprovado, buscar uma foto de cena de trabalho e gerar nova peça com nome novo (a licença da Pexels precisa ser lida antes). Se as faixas finas forem aceitas, registrar em `docs/ESTILO_PALAVRA_DE_OURO.md`. Skills: `voz-leticia`, `contexto-orbit`.
