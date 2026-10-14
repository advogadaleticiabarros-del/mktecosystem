# 🎬 Vídeos Reels — Advocacia & Consultoria (OAB/ES 39.948)

Reels informativos de direito para Instagram, produzidos no padrão visual oficial do escritório (identidade dourada premium, conformidade com o Código de Ética da OAB).

## Padrão de produção
- Formato: 1080×1920 (Reels), 24 segundos, 5 cenas
- Paleta: fundo escuro + dourado `#C9A84C` + texto branco
- Conteúdo 100% informativo (sem CTA comercial, sem captação de clientela)
- Trilha institucional livre de direitos autorais
- Encerramento com a logo oficial + OAB/ES 39.948

## Conteúdos

### 01 — Direito Trabalhista: folga em dia de jogo do Brasil
Reel sobre o direito (ou não) à folga em dia de jogo da Seleção, com base na CLT (Art. 130).

| Arquivo | Duração | Observação |
|---------|---------|------------|
| `reel_v1_18s.mp4` | 18s | Versão inicial |
| `reel_v2_24s.mp4` | 24s | Padrão visual oficial (logo + ritmo de leitura) |
| `reel_v3_24s_musica.mp4` | 24s | Padrão + trilha sonora institucional |

### 05 — Reel institucional (edição de vídeo real, não animado)
Primeiro reel editado a partir de gravação real da Dra. Letícia (falando
direto pra câmera), não gerado por template animado. Pipeline em
`05-reel-institucional/work/montar_reel.py` (ffmpeg): corte de
silêncio/sobra no início e fim de cada cena, remoção de ruído de fundo,
normalização de volume, correção leve de cor/contraste, transições em
dissolve suave (0,35s) entre as 7 cenas, abertura e fechamento com a
identidade oficial (selo dourado + Letícia Barros + OAB/ES 39.948),
formato nativo vertical 1080×1920.

| Arquivo | Duração | Observação |
|---------|---------|------------|
| `05-reel-institucional/reel_v1.mp4` | 42s | 7 cenas, brutos em `Downloads/videos Leticia` |

### 06 — Trabalhista: "3 erros que fazem você perder direitos na demissão"
Reel de montagem (texto cinético, sem gravação), no padrão dourado/preto
oficial. Pipeline reutilizável em `montar_reel_montagem.py` (raiz do
repo): renderiza cenas via Playwright a partir de `work/scene.html`,
monta com ffmpeg (dissolve 0,4s entre cenas). Sem áudio — pensado pra
usar áudio em alta do próprio Instagram na hora de postar.

| Arquivo | Duração | Observação |
|---------|---------|------------|
| `06-reel-3-erros-demissao/reel.mp4` | 20s | 5 cenas, sem áudio |

### 07 — Trabalhista: "Assédio moral: 3 sinais que ninguém te conta"
Mesmo pipeline de montagem do #06.

| Arquivo | Duração | Observação |
|---------|---------|------------|
| `07-reel-assedio-moral-sinais/reel.mp4` | 20s | 5 cenas, sem áudio |

### 10 — Gestante CLT: "Engravidou durante o aviso prévio? Isso muda alguma coisa"
Reel genérico do calendário 17/08 (dia de artigo + carrossel + pergunta +
reel), mesmo pipeline de montagem do #06/#07 — sem gravação da Letícia,
cenas de texto cinético. Conteúdo: estabilidade começa na confirmação da
gravidez (não na assinatura de papel), vale mesmo com aviso prévio já
comunicado, proteção até 5 meses após o parto.

| Arquivo | Duração | Observação |
|---------|---------|------------|
| `10-reel-gestante-aviso-previo/reel.mp4` | ~19,7s | 5 cenas, sem áudio |

### 11 — Gestante CLT: mesmo tema do #10, versão com b-roll real (Pexels)
Segunda versão do reel de 17/08, produzida pela squad ExpxAgents
`marketing/redes-sociais/reels/reel-generico` (Camila Duarte → Rafael
Nogueira → Bruno Aragão). Diferente do #10 (fundo sólido dourado/preto),
aqui o fundo de cada cena é um clipe de vídeo real buscado na API do
Pexels (mulher grávida em ambiente doméstico/escritório, advogada de
terno), com gradiente de escurecimento (scrim) por baixo do texto pra
garantir legibilidade. Pipeline em `11-reel-broll-aviso-previo/work/gerar.py`.

| Arquivo | Duração | Observação |
|---------|---------|------------|
| `11-reel-broll-aviso-previo/reel.mp4` | ~19,8s | 5 cenas, b-roll Pexels, sem áudio |

---
Reels 01-04 produzidos com ExpxAgents — Squad Editor de Vídeo.
Reel 05 em diante: edição real via ffmpeg, script neste repositório.
Reels 06-07: montagem 100% nossa (`montar_reel_montagem.py`), sem
depender de gravação — usar quando não houver vídeo bruto disponível.
Reel 11 em diante (reels genéricos com b-roll): squad ExpxAgents
`marketing/redes-sociais/reels/reel-generico`, busca automática de b-roll
via API do Pexels + composição de texto sobre vídeo (não sobre fundo
sólido).

### 13 — Série "13º sem susto" (3 Reels) · motor v2 procedural (10/10/2026)
Só o áudio do vídeo do NotebookLM ("O Guia Definitivo do Décimo Terceiro Para Trabalhadoras"). Primeira série no
motor v2 (`_padrao-motion/`): pó de ouro que forma números e o logo, poeira dourada reativa à voz, explosões nos
carimbos, soco nas palavras-chave, transições "tinta" e "luz", verificador automático da área limpa e da leitura.
Pipeline: `13-reels-procedural/work/serie.py` (+ `motor.py`, `engine.html`, `fx.js`). Legendas em `LEGENDAS.md`.

| Arquivo | Duração | Observação |
|---------|---------|------------|
| `13-reels-procedural/13-sem-susto-1.mp4` | ~25s | Prazos do 13º (03/11) |
| `13-reels-procedural/13-sem-susto-2.mp4` | ~29s | 13º proporcional (05/11) |
| `13-reels-procedural/13-sem-susto-3.mp4` | ~25s | Licença-maternidade e 13º (07/11) |
