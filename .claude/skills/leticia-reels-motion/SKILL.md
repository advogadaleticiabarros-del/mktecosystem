---
name: leticia-reels-motion
description: PADRÃO OFICIAL de Reels da Dra. Letícia Barros (v2 procedural, 10/10/2026). Use SEMPRE que a usuária mandar um vídeo ou áudio (NotebookLM, gravação, narração) para virar Reels, pedir Reels "virais", "com motion", "com animação procedural", "com efeitos e transições", ou uma série de Reels. Usa só o áudio e produz o vídeo inteiro como diretor: storyboard, cenas com fotos/vídeos reais + motion graphics contextual + camada procedural dourada (pó de ouro, energia da voz, tinta, luz), legenda palavra a palavra, área limpa da Meta verificada por código, som próprio, legendas SEO/IA e publicação automática pelo Orbit.
---

# Reels da Letícia — padrão motion v2 (procedural)

Você é o **diretor**: cada quadro tem função (informar, prender, levar ao envio). Nada decorativo solto.

- Código-base **versionado no Orbit**: `C:\Users\prosy\mktecosystem\producao\reels\motor\` (fonte da verdade desde 14/10/2026)
  - `motor.py`: motor genérico, não muda por série.
  - `serie.py`: modelo de roteiro.
  - `engine.html` + `fx.js`: visual e camada procedural.
  - `narrar.py`: roteiro → voz clonada da Letícia (ElevenLabs).
- v1 congelada (só para consulta): `producao\reels\motor-v1\`
- Roteiros, legendas e scripts de cada série já feita: `producao\reels\series\NN-nome\` (só texto).
- Mídia pesada (vídeos, áudios, fotos, renders) continua em `C:\tmp\videos-reels\NN-nome\`, fora do git.
- Exemplo v2 completo: `13-reels-procedural` (série "13º sem susto"); exemplo v1: `12-reel-direitos-gestante`.
- Mudou o motor? Edite no repositório e faça commit. Ao terminar uma série, copie para `producao\reels\series\` os arquivos de texto (serie.py, roteiro.txt, transcricao.json, LEGENDAS.md, scripts de subida) e faça commit.

## O que a v2 acrescenta (tudo em código, determinístico por tempo)

- **Energia da voz**: o motor mede a narração quadro a quadro. O pó dourado e a barra de progresso pulsam com a fala.
- **Pó de ouro** (`po(...)`): partículas se juntam e formam o número, a palavra ou o logo. O desenho assenta nítido, com brilho metálico.
  - Use para o dado principal da cena: 30/11, 13º, 15 dias, 120 dias.
  - O logo do fechamento sempre se forma assim.
- **Explosão + onda de choque** em carimbo, pílula e cartão (`burst`), com som sincronizado.
- **Soco (punch-in)**: micro-zoom elástico nas palavras de `destaques`, com no mínimo 2,2 s entre um e outro. É a quebra de padrão com sentido.
- **Ouro metálico animado** em todo `<em>` e `.ouro`: um brilho que percorre o texto.
- **Transições novas**:
  - `tinta`: máscara de ruído que escorre, com borda incandescente. Use `tdur` de .7 a .8.
  - `luz`: clarão dourado na diagonal.
  - Continuam valendo corte, whip, whipV, zoom, íris, sobe e dissolve. Nunca a mesma em tudo.
- **Blocos novos**:
  - `foto_card` (grade de perfis com moldura dourada);
  - `calendario` (exemplo em serie.py do 13º);
  - `centro(w)` (centraliza pílulas);
  - `BALANCA` (traço).

## Regras de direção (não mudam)

- **Só o áudio** do material enviado. O visual é 100% nosso; nunca encaixar o vídeo do NotebookLM.
- **Fatos conferidos** antes de cortar: anotar a lei de cada trecho no docstring de serie.py. Ficam de fora:
  - trecho errado;
  - fala truncada pela IA (ex.: "contos contos de INSS");
  - termo vetado pela OAB ("especialista", oferta de serviço).
- **Vídeo longo vira série de 3**, de 20 a 45 s cada.
  - Gancho na tela já no quadro 0, com a pergunta que a pessoa faria.
  - Virada ou recompensa perto de 70%: carimbo, número em pó de ouro.
  - A última fala puxa a próxima parte.
- **Área limpa (Meta)**:
  - topo de 270 px, base de 672 px (35%) e laterais de 65 px livres;
  - margem de texto de **90 px**, porque a câmera dá zoom de até 3%;
  - gráficos entre y=350 e ~1085; legenda entre 1110 e 1240;
  - **rodar `py serie.py --checar`** antes de renderizar e só seguir com "área limpa: ok" nos 3 Reels.
- **Leitura**:
  - título com no máximo ~15 caracteres por segundo na tela (o `--checar` avisa "LEITURA");
  - no máximo 3 textos disputando o olhar ao mesmo tempo (kicker + título + pílula/carimbo);
  - a legenda adianta 0,12 s em relação à voz.
- **Rosto nunca sob texto nítido**: mova o texto para o terço livre ou desloque a foto (`kb`). Se não der, use desfoque de 7 a 9 e um véu mais escuro.
- **Identidade**:
  - cores: café `#231E1A`/`#1A1511`, dourado `#C9A962`, areia `#E8DED1`;
  - **EB Garamond** nos títulos (nunca Cormorant), Inter na legenda e nos rótulos;
  - faixas douradas e grão.
- **Representatividade**: maioria de pessoas negras nas fotos. Use pessoas brancas com menos frequência.
- **Imagens**: fotos e vídeos reais do Pexels, curados à mão em folha de contato. Ficam de fora:
  - texto em inglês ou marca;
  - dinheiro estrangeiro (dólar, euro);
  - nudez.
- **Legenda na tela**: no máximo 24 caracteres por bloco, com a palavra falada em destaque dourado.
  - Corrija a transcrição em `corrige`. Um valor vazio apaga a palavra; exemplos: "contra"+"cheques" vira "contracheques", "da" vira "dá".
- **Fechamento** (`outro(a, proxima, publico, gestante)`):
  - logo em pó de ouro;
  - "Salve e mande para …" (o envio por mensagem pesa mais que a curtida);
  - pílula da próxima parte;
  - "Cada caso tem detalhes. Procure uma advogada de confiança.";
  - assinatura: "Dra. Letícia Barros" + área, ou, em tema de gestante, "a advogada da Gestante trabalhadora";
  - OAB/ES 39.948 · @adv.leticiabarros2.
  - Se a narração termina com o CTA, o fechamento começa na frase "Cada caso…" (`outro(seg[k], ...)`).
- **Som**:
  - voz tratada (highpass, EQ, compressor, loudnorm −15 LUFS);
  - efeitos sintetizados: whoosh, pop, carimbo, boom no gancho, brilho no fim, "po" na formação do pó;
  - base própria com pulso e ducking;
  - entregar com e sem música.
- **Exportação**: 1080×1920, 30 fps, H.264 CRF 18, `+faststart`, áudio AAC **128 kbps** 48 kHz (192 kbps é recusado pela API).

## Passo a passo

1. Criar `C:\tmp\videos-reels\NN-nome\fontes\` com o vídeo ou o roteiro e `work\` com cópia de `producao\reels\motor` (do repositório) + `videos\` + `fotos\`.
2. Áudio. **Padrão desde 14/10/2026: voz clonada da Letícia no ElevenLabs** (`narrar.py`):
   - escrever `fontes\roteiro.txt` com uma parte por Reels (`## Parte 1`...), fatos conferidos ANTES, escrito como se fala (números, "13º", siglas e "art." por extenso);
   - `py narrar.py ..\fontes\roteiro.txt ..\fontes --checar` até sem AVISO; depois sem `--checar`;
   - sai `narracao.wav` (CFG `src`) + `transcricao.json` com tempo exato por palavra (não precisa de Whisper nem de `corrige`); o script imprime os `trechos` de cada parte;
   - chave/voz: `ELEVENLABS_API_KEY`/`ELEVENLABS_VOICE_ID` ou `C:\Users\prosy\.elevenlabs-leticia.json`; cache em `cache_voz\` evita cobrar o mesmo texto duas vezes.
   - Áudio enviado (NotebookLM/gravação): transcrever com `py transcrever.py vN.wav vN.json` e copiar para `work\transcricao.json`. Se um trecho sair estranho, retranscrever só ele com o modelo `medium`.
   - Legenda do post continua com "🔊 Narração produzida com inteligência artificial." (voz clonada também é IA).
3. Ler a transcrição, conferir os fatos e escolher os trechos (`REELS[n]["trechos"]`) e os cortes.
4. Pexels pela chave do Orbit (script na VPS, `obter_chave(db, tenant, "pexels")`):
   - fotos verticais `large2x` e vídeos verticais;
   - folha de contato e escolha à mão;
   - nomes `f-<tema>-i-id.jpg` em `fotos\` e `v-<tema>-i-id.mp4` em `videos\`.
5. `serie.py`:
   - preencher `CFG` (src, serie, corrige, destaques) e as funções `reelN(W, seg, fim)`;
   - âncoras sempre por palavra: `W("palavra", depois)`; cuidado com palavras repetidas ("A"): passe `depois`.
6. `py serie.py --checar` até "área limpa: ok" e sem "LEITURA".
7. `py serie.py N --amostras` (ou `TS="1.2,5.8"`) e revisar como diretor. Procurar:
   - texto sobre rosto;
   - ordem dos textos versus a fala;
   - sobreposição e acentos;
   - cada cena com uma ideia só.
8. Render completo em segundo plano: `py serie.py 1 2 3`. Sai em `NN-nome\<prefixo>N.mp4` e `_sem_musica.mp4`.
9. Conferir os vídeos finais (gancho, pico e fechamento) antes de entregar.
10. Legendas SEO/IA (skill `ai-seo`):
    - primeira linha com a pergunta + a resposta;
    - bloco de resposta de 40 a 60 palavras;
    - "As perguntas que mais chegam aqui" (3 ou 4);
    - fontes legais e a entidade fixa;
    - bordão trabalhista quando o tema for trabalhista;
    - "Atualizado em <mês/ano>";
    - "🔊 Narração produzida com inteligência artificial.";
    - 5 hashtags.
    - Primeiro comentário: base legal + uma pergunta de conversa.
11. Orbit:
    - subir o mp4 para a mídia (`docker compose cp` para `api:/app/media`);
    - criar a peça `tipo="reels"` com `corpo.video`, `legenda`, `primeiro_comentario`, `programacao`;
    - aprovar e criar o ScheduledPost `formato="reels"`, às 20h30, em dias sem outro post noturno;
    - backup do banco antes.
    - O Orbit publica sozinho.
