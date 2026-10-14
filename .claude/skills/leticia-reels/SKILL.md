---
name: leticia-reels
description: Use quando a usuária pedir para editar um Reel a partir de gravação real (vídeo bruto dela falando pra câmera), no padrão do escritório. Para vídeo/áudio que vira Reels com motion design (NotebookLM, narração, série), use a skill leticia-reels-motion, que é o padrão oficial desde 09/10/2026. Cobre corte de sobras/silêncio, limpeza de áudio, transições suaves, marca d'água e identidade final. Não é sobre montagem sem gravação (isso é outro formato, ver README do repo videos-reels, pipelines 06/07).
---

# Reel institucional — edição de vídeo real

> **Regras obrigatórias:** `C:/Users/prosy/mktecosystem/docs/MANUAL_CONTEUDO_REDES.md` (OAB, Meta, specs, design system, checklist). Em conflito, o manual vence esta skill.


Pipeline usado pela primeira vez no Reel institucional #05 (repo
`C:\tmp\videos-reels`), a partir de gravação real da Dra. Letícia falando
direto pra câmera em várias cenas. Reusar essa mesma técnica sempre que
houver vídeo bruto pra editar — não regravar o processo do zero.

**Papel no funil do dia:** conteúdo de **noite/alcance** (ver
[[orbit-estrategia-crescimento-instagram]]) — Reels são o formato pra
alcançar quem ainda não segue o perfil.

## 1. Receber o vídeo bruto

Perguntar onde estão os arquivos (normalmente `Downloads` ou uma pasta
específica no Desktop) — **nunca supor qual arquivo é o certo se houver
mais de um candidato**; a usuária costuma nomear o arquivo certo
explicitamente (ex: "video correto para usar.MOV"). Se vier em várias
cenas separadas (`1.mp4`, `2.mp4`...), tratar cada uma como um clipe.

## 2. Mapear os clipes e os cortes

Extrair frames de amostra de cada clipe pra ver onde a fala começa/termina
e se há sobra no início/fim (ex: pessoa ajeitando a câmera, silêncio antes
de falar). Definir os tempos de corte (`inicio`, `fim`) por clipe.

Se precisar remover um trecho **do meio** de um plano contínuo (ex: gesto
de desligar a câmera no meio da fala), **não usar dissolve** — juntar os
dois sub-trechos com **corte seco** (ffmpeg concat demuxer), senão gera
ghosting/duplo-exposição. Só usar dissolve **entre cenas diferentes**.

## 3. Montar (ffmpeg)

Reusar `C:\tmp\videos-reels\05-reel-institucional\work\montar_reel.py`
como base — copiar pra uma nova pasta de trabalho e ajustar:
- `SRC`: pasta com os brutos
- `CLIPES`: lista de `(arquivo, inicio, fim)` por cena (ou lista de
  sub-trechos pra corte seco dentro da mesma cena)
- `OUT_FINAL`: caminho de saída

Parâmetros já validados, não reinventar:
- `XFADE = 0.4` — transição suave e sutil entre cenas
- Filtro de vídeo: `scale=1080:1920` (vertical nativo) + correção de cor
  (ver "Correção de cor" abaixo, **não é um valor fixo único** — depende
  da exposição do bruto) + reset de PTS
- **Áudio tratado UMA VEZ SÓ, depois de tudo concatenado** — nunca por
  clipe individual antes da concatenação (isso foi a causa de um
  desencontro de áudio/vídeo na v1, corrigido na v2). Cadeia:
  `highpass=f=90,afftdn=nr=12:nf=-25,loudnorm=I=-16:TP=-1.5:LRA=11`
- FFmpeg local:
  `C:\Users\prosy\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.2-full_build\bin\ffmpeg.exe`

## 4. Identidade visual (abertura, fechamento, marca d'água)

- Abertura (`INTRO_DUR`) e fechamento (`OUTRO_DUR`) com selo dourado +
  "Letícia Barros" + OAB/ES 39.948 — mesma identidade oficial de todo
  conteúdo do escritório.
- Marca d'água (avatar + `@adv.leticiabarros2` + ✓) durante a parte
  falada, no mesmo padrão visual da skill `leticia-criativo-pergunta`
  (gerada via `identificacao.html` → `identificacao.png`).
- Rodapé especial "advogada da Gestante trabalhadora" — **só na legenda**,
  nunca no vídeo/card, se o tema for sobre gestante (ver
  [[voz-leticia-rodape-gestante]]).

## 5. Padrão de produção (não mudar sem a usuária pedir)

- Formato: 1080×1920, ~20-45s, várias cenas
- Paleta: fundo escuro + dourado `#C9A84C` + texto branco
- Conteúdo informativo, **sem CTA comercial, sem captação de clientela**
  (mesma regra de ética OAB do resto do conteúdo — ver `voz-leticia`)
- Encerramento sempre com logo oficial + OAB/ES 39.948

## Correção de cor — CRÍTICO, checar sempre (tom de pele)

**A personagem é negra — nunca aplicar filtro que clareie/lave o tom de
pele.** Erro real cometido no Reel #08: copiei cegamente o filtro do
Reel #05 (`eq=contrast=1.06:saturation=1.08:brightness=0.01`) sem
verificar se o bruto novo tinha a mesma exposição. O bruto do #08 já
vinha com testa/maçãs do rosto superexpostas pela câmera do celular —
aplicar brilho POSITIVO em cima disso estourou ainda mais, deixando o
rosto visivelmente esbranquiçado.

**Processo obrigatório antes de aplicar qualquer filtro de cor:**
1. Extrair um frame do bruto em um ponto com boa luz no rosto.
2. Medir objetivamente a exposição da testa/maçãs com Python/PIL (RGB
   médio de um crop da região) — não confiar só no olho.
3. Se já estiver clara/estourada no bruto: **reduzir brilho**
   (`brightness` negativo), não aumentar. Combinar com curva de
   recuperação de altas-luzes.
4. Manter saturação (~1.10-1.15) pra preservar o calor natural do tom de
   pele — não deixar dessaturar junto com a correção de exposição.
5. **Testar e medir de novo** (RGB médio da mesma região) até o tom
   ficar fiel ao bruto original ou mais escuro — nunca mais claro que o
   bruto. **Não ter medo de ser agressivo**: no Reel #08 a primeira
   correção (brightness=-0.05) pareceu suficiente nos números mas a
   usuária ainda achou claro demais na inspeção visual — o valor final
   que aprovou foi bem mais forte (ver filtro abaixo). Prefira pecar
   por escurecer demais e ajustar pra cima do que entregar ainda claro.
6. Cuidado com curvas mal calibradas: uma tentativa com pontos de
   controle muito próximos/desalinhados gerou um cast de cor
   amarelo-esverdeado estranho no cabelo/pele — sempre inspecionar o
   resultado visualmente, não só confiar que "mais pontos = mais
   controle".
7. Só depois de aprovado, replicar o mesmo filtro no vídeo inteiro. Cada
   vídeo bruto pode ter exposição diferente (câmera, luz do ambiente) —
   não existe um filtro fixo válido pra sempre, é sempre um recalibre
   por vídeo.

**Filtro validado no Reel #08** (bruto vindo com testa/maçãs
superexpostas por luz de topo do celular), como ponto de partida pra
próximos vídeos com problema parecido — ainda assim, sempre recalibrar
com o processo acima, não copiar cego:
```
eq=contrast=1.10:saturation=1.13:brightness=-0.16,
curves=all='0/0 0.35/0.27 0.7/0.55 1/0.85'
```

## Bug conhecido (corrigido em 05/08/2026, Reel #08)

No cálculo de `inicio_fala`/`fim_fala` em `concatenar_com_transicoes`,
usar o **fim** do dissolve (`offset + XFADE`), não o início (`offset`) —
senão a marca d'água liga 0,4s cedo demais e fica sobreposta com a
intro/outro ainda em transição. Testar sempre extraindo frame no
milissegundo exato da borda do dissolve antes de considerar pronto.

## 6. Verificar antes de considerar pronto

- Rodar `ffprobe` ou extrair frames no ponto de cada corte pra confirmar
  que não há ghosting nas transições
- Conferir que o áudio está sincronizado do início ao fim (não só no
  começo) — desvios costumam aparecer só perto do final do vídeo
- Mostrar o vídeo final pra usuária aprovar antes de considerar
  concluído

## 7. Onde salvar

Nova pasta em `C:\tmp\videos-reels\NN-nome-do-reel\`, seguindo a
numeração sequencial existente (próximo é 08). Adicionar entrada no
`README.md` do repo com duração, observação e caminho do pipeline usado.
