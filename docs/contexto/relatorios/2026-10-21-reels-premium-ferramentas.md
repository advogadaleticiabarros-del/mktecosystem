# 21/10/2026: Reels premium, ferramentas `fala.py` e `conferir.py` e ajustes do motor

## Pedido
"Construa as ferramentas do passo 1 (fala.py e conferir.py) e ajuste o motor como a skill descreve. Valide reproduzindo a v2 da série 18 com o IMG_0330 dos Downloads. Não publique nada no Orbit." (skill `leticia-reels-premium`).
Antes disso, ela tinha pedido os Reels de um vídeo novo (`Desktop\Leticia conteudos\novos videos\em produção\20250815_164956.mp4`, 77 s, 4K): **não começado**, ela reduziu o escopo para o passo 1.
No meio do trabalho ela também pediu: verificar se dá para acessar os efeitos do Pixabay, sem fazer nada.

## Feito
- `producao/reels/motor/fala.py`, `conferir.py` e testes `test_fala.py`, `test_conferir.py`, `test_motor.py`.
- Motor (`motor.py`, `engine.html`, `README.md`):
  - sem trilha;
  - mix a −14 LUFS por ganho + limitador;
  - CBR a 11 Mbps;
  - biblioteca de efeitos com variações e semente;
  - sidechain dos efeitos sob a voz;
  - ambiência;
  - punch-in nas emendas do rosto;
  - `fim_da_fala()`;
  - `codificar` recusa sobrescrever.
- Validação da série 18: `producao/reels/series/18-limbo-previdenciario/falas_premium.py` e `serie_premium.py`. Vídeos em `C:\tmp\videos-reels\18-limbo-previdenciario\validacao-premium\`.
- Notas de uso na skill (`.claude/skills/leticia-reels-premium/SKILL.md`, seção Ferramentas) e resumo em `docs/CONTEXTO_PROJETO.md` ("Reels premium: ferramentas e motor").

## Verificado
- `py -m pytest` em `producao/reels/motor`: **39 testes passando**.
- `fala.py montar` no IMG_0330 com os trechos da v2: **"fala ok"** nos dois Reels (41,2 s e 34,1 s).
  - Uma nota no Reel 1: "médico do" ouvido como "médio de". O trecho cortado ali tem pico −41 dB, então é silêncio.
- `conferir.py` em `limbo-previdenciario-premium-c-{1,2}.mp4`: **sem avisos**.
  - Duração 45,0 s e 37,9 s; 1080×1920 a 30 fps; 11,0 Mbps.
  - Volume −14,1 e −14,2 LUFS; pico −1,9 e −1,8 dBTP.
- Folhas de quadros revisadas uma vez: punch-in visível, área limpa ok, fechamento com motivo.
- **Não verificado:** ninguém ouviu os vídeos com som (a qualidade do limitador na voz e o nível dos efeitos precisam de ouvido humano).
- **Não verificado:** os efeitos abaixam sob a voz pela compressão lateral (sidechain), mas não há teste que meça isso.

## Decisões e porquês
- **Pausa partida por estalo:** só entra no corte se, medida a −40 dB, tiver ≥ 60% de silêncio a −44 dB.
  - Juntar silêncios "próximos" (< 0,08 s) foi tentado e **descartado**: comeu a consoante de "atestado".
  - −36 dB também foi descartado, porque pega fala.
- **Aviso de texto exige divergência no trecho isolado e na fala inteira**, porque o Whisper chuta em trecho menor que 1 s ("Errado" virou "e RAB"). Troca ou palavra comida onde o corte só tirou silêncio vira "nota". Artigos trocados (um/o/a) são tolerados.
- **Volume:** o loudnorm linear parava em −15 LUFS porque a voz tratada tem picos de consoante. A correção foi ganho + limitador iterativo.
- **Taxa:** CBR em vez de taxa média. A taxa média deu 4 a 9 Mbps em imagem simples, e duas passadas também não resolvem (testado: 4,9 Mbps).
- **Whisper:** sem memória para o medium, cai para o small com AVISO. Nesta sessão o medium carregou depois que liberou memória.
- **Arquivos:** os vídeos `-` e `-b-` da validação ficaram como registro, e os bons são os `-c-`. Nada foi sobrescrito, conforme a regra.

## Pendente
- **Push:** os commits estão só no computador. A conta ativa `alcancelegalmkt-collab` recebe 403 neste repositório. Falta a Jessica autorizar o push pela `advogadaleticiabarros-del` (como em 20/10) ou dar acesso à colaboradora.
- O vídeo novo `20250815_164956.mp4` (passos 2 a 8 da skill) depende de ela pedir de novo.
- Pixabay: a página abre pela leitura web, mas o download por linha de comando dá 403 e a API não tem áudio. Se ela quiser usar, baixa à mão e conferimos a licença (uso comercial). Quem decide: Jessica.
- Ouvir um Reel `-c-` com som para aprovar o padrão de áudio novo. Quem decide: Jessica.

## Próxima sessão
- Para fazer os Reels do vídeo novo, use a skill `leticia-reels-premium` a partir do passo 2.
- Copie `producao/reels/motor` para `C:\tmp\videos-reels\19-<tema>\work\`.
- Rode `py fala.py transcrever "<bruto>"`. Feche programas antes: o Whisper medium precisa de ~3 GB livres.
