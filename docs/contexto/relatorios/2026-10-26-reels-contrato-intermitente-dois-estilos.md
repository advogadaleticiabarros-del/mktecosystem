# 26/10/2026 · Reels do contrato intermitente em dois estilos

## Pedido
Editar os Reels de `Desktop\NOVOS REELS` ("vamos fazer as animações em código, json, para que fique bonito e explicativo").
Durante a sessão: usar as referências visuais mandadas (dois Reels do @viniciusguimaraes.ia) misturadas com a edição atual;
"deixe o motor antigo intacto", "deixe com os dois estilos, e sempre me pergunte"; "vamos fazer um vídeo em cada formato,
assim consigo testar"; "eu quero furar a bolha". Também: instalar a skill `watch` (claude-video) e "o que der" do GitHub trending.

## Feito
- VIDEO 1 (IMG_0384 + IMG_0385) virou a série 19, 2 Reels (escolha dela). Fatos, cortes e trechos em
  `producao/reels/series/19-contrato-intermitente/falas.py`; legenda em `legendas.py` do mesmo lugar.
- **R1 pronto nos dois estilos:** `contrato-intermitente-inteiro-1.mp4` (roteiro `serie_inteiro.py`, banco Pexels + 3D) e
  `contrato-intermitente-dividida-1.mp4` (roteiro `serie_dividida.py`, diagramas no painel). Arquivos em
  `C:\tmp\videos-reels\19-video1\` e cópias em `Desktop\NOVOS REELS\VIDEO 1\PRONTOS`.
- Estilo novo **tela dividida** em `producao/reels/motor-dividida/` (README explica o uso). `producao/reels/motor/` não mudou.
- `producao/reels/motor3d/clip3d.py`: clipes 3D curtos sem textos (semana, cofre) para cena de fundo do motor 2D.
- Skill `leticia-reels-premium`: regra "dois estilos, pergunte sempre".
- Contexto em `docs/CONTEXTO_PROJETO.md`, seção "Série 19".
- Fora do git (conta do Claude): skills `watch`, `impeccable`, `hallmark`; yt-dlp via pip --user (Scripts no PATH do usuário).

- **Correção de cor (pedido: "não quero que mexa na imagem da Dra., deixe com a imagem original"):** a gravação é HDR
  (HLG); estava convertida como SDR. `fala.py` converte HDR (tonemap mobius, escolhido entre 4 opções), engines sem filtro e sem
  grão no rosto, véu só no peito. Saíram as v2 dos dois estilos (as v1 ficam).

## Verificado
- `fala.py montar`: R1 "fala ok" (46,8 s). R2 ainda com avisos nos trechos 9, 10 e 15.
- `serie.py 1 --checar` nos dois estilos: "área limpa: ok", sem aviso de LEITURA.
- `conferir.py` nos dois R1: sem avisos (50,5 s, 1080×1920, 30 fps, 11 Mbps, −19,9 LUFS, pico ≤ −2,0 dBTP). Folha final revisada.
- v2: `conferir.py` sem avisos nos dois; folha revisada (pele no tom real). `py -m pytest` em `motor/`: 42 passaram.
- Não verificado: os vídeos não foram assistidos com som por uma pessoa; nada foi ao Orbit.

## Decisões e porquês
- Teste justo: **o mesmo R1 nos dois estilos**, com a mesma legenda, como Trial Reels (só não seguidores). Ela escolheu
  essa opção. É exceção pedida à regra "uma versão só por vídeo".
- Volume em −19,9 LUFS (e não −14): a gravação tem picos fortes; a regra permite até −20 para o limitador não cortar > 2 dB.
- Fala montada de uma cópia 1080 do bruto (`fontes/bruto-1080.mp4`): o 4K HEVC 10 bits dava "Cannot allocate memory".
- Fechamento sem "comenta X que eu te mando" das referências: perto de captação (OAB).
- `hallmark` só para site novo: proíbe itálico em título e rótulo em caixa-alta espaçada, marcas da identidade.
- SkillSpector (NVIDIA) não instalado: o controle de permissões bloqueou; não houve contorno.

## Pendente
- Jessica: assistir os dois R1 **v2** com som e aprovar; dizer se sobe ao Orbit como Trial Reels (o Orbit já tem `corpo.trial_reels`).
- Depois do teste (24 a 72 h): escolher o estilo vencedor; o R2 sai nele.
- R2: acertar as emendas dos trechos 9 ("grandes empresas… utilizam"), 10 ("ah" no fim) e 15 ("Ou" no começo).
- VIDEO 2 (IMG_0387, 0388, 0390): ainda não começou; perguntar o estilo antes.
- Jessica: liberar ou não a instalação da SkillSpector.

## Próxima sessão
Ler a seção "Série 19" do `docs/CONTEXTO_PROJETO.md`. Se ela aprovou o R1, fazer o passo 7 da skill
`leticia-reels-premium` (backup, mídia, rascunho com `trial_reels`) para os dois arquivos. Skills: `leticia-reels-premium`,
`contexto-orbit`.
