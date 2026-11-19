# 19/11/2026: carrossel "Decreto da escala 5x2 assinado" (a partir de referência do TST)

## Pedido
A Jessica mandou o carrossel do TST (instagram.com/p/Df7ZFwQhh2r) e pediu "Faça um desse", depois "Aplicando a Dra
Letícia é claro".

## Feito
- Carrossel de 8 páginas (1080×1440) em `producao/estilos/escala-5x2/` (ver o `README.md` da pasta): capa-manchete,
  as duas etapas (16/12/2026 e 16/12/2027), 14,8 milhões na 6x1, mulheres com 6,8 h a mais de tarefas da casa,
  jornada longa = salário menor (café, sem "R$", barras), descanso e produtividade, "Guarde desde já" (salvável) e
  fecho com o retrato real da Dra.
- Legenda e primeiro comentário em `editorial.json`; página de conferência publicada:
  https://claude.ai/artifact/Dgf7zpuSyUWP78B452Chh5.

## Verificado
- Decreto assinado em 19/11/2026: notícias do Planalto e do MTE. 14,8 milhões: MTE/eSocial (março de 2026).
- As 8 artes foram vistas uma a uma depois do render (sem marca de terceiro nem texto estrangeiro visível).
- O artigo do blog "escala-42-horas-16-de-dezembro…" ainda dá 404, por isso o link saiu do comentário.
- Não verificado por conta própria: PNAD 2022 (6,8 h), Ipea/RAIS 2023 e OIT (citados como o TST cita).

## Decisões e porquês
- Estrutura da referência com a identidade da marca (regra das referências de 18/11), mais as duas páginas padrão da
  Dra. (salvável e fecho com retrato). 8 páginas em vez de 7 do v5.
- Fotos novas do Pexels baixadas por link direto: a busca pela chave do Orbit na VPS foi bloqueada pelo modo automático,
  e as candidatas do banco local já tinham sido usadas em outras peças.
- Página de salário em café: é o acento escuro do carrossel (feed claro).

## Pendente
- Jessica: aprovar e escolher a data. Proposta: dom 22/11, 12h, no lugar da frase dos alimentos gravídicos (vai para
  a reserva). Nada foi agendado nem enviado ao Orbit.
- Dra.: conferir os textos (seção "Textos novos" da conferência).
- Antes de publicar: reconferir a liminar do STF (ADIs 8.041 e 8.042), que vai ao Plenário.

## Próxima sessão
Com a aprovação, subir as 8 artes ao Orbit e trocar a peça de 22/11 na agenda (ver `referencias-1811/agendar.py` como
modelo). Skills: `leticia-carrossel`, `contexto-orbit`.
