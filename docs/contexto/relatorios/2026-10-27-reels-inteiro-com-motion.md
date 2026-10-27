# 27/10/2026 · Reels: R1 do contrato intermitente no estilo inteiro com as animações da tela dividida

## Pedido
"Faça agora na versão inteira, mas use os mesmos tipos de animações que a outra está usando (motion em código)...
Faça primeiro a versão desse vídeo, depois se eu aprovar você faz o restante." Antes: analisar Manim, Motion Canvas e
SVG/Lottie e dizer quais ficariam mais interessantes.

## Feito
- `producao/reels/series/19-contrato-intermitente/serie_inteiro_motion.py`: a Dra. em tela cheia nas falas diretas; nos
  trechos de explicação, banco ou 3D bem escurecido com os diagramas da tela dividida (relógio que volta e se completa,
  calendário, recibo, dezembro), descidos 150 px para a faixa limpa do quadro cheio.
- Pasta de trabalho `C:\tmp\videos-reels\19-video1\work-motion\` (motor/ + engine, fx e diagramas da motor-dividida/).
  O `motor/` e o `motor-dividida/` não mudaram.
- Entregue: `Desktop\NOVOS REELS\VIDEO 1\PRONTOS\contrato-intermitente-inteiro-motion-1.mp4` (47,2 s).
- Contexto em `docs/CONTEXTO_PROJETO.md` (série 19, terceira variação).

## Verificado
- `--checar`: área limpa ok, sem aviso de leitura. `conferir.py`: sem avisos (1080×1920, 30 fps, 11 Mbps, -19,8 LUFS,
  pico -2,0 dBTP). Folha de quadros revisada.
- A fala é o mesmo arquivo da v3 (byte a byte), já conferida na transcrição literal; cor `bt709`.
- Não verificado: ninguém assistiu com som; nada foi ao Orbit.

## Decisões e porquês
- Vídeo escolhido: R1, o único que já tinha as duas versões (inteiro v3 e dividida v3), para comparar lado a lado.
- O banco `stock-calendario` saiu: tem corações vermelhos, fora da paleta; no lugar, outro trecho do clipe do celular.
- Ferramentas: o motor já é "motion em código" (HTML renderizado quadro a quadro, mesmo princípio do Motion Canvas) e já
  desenha traço SVG (`stroke-dasharray`). Manim e Motion Canvas trariam outra cadeia de ferramentas sem ganho visual para
  o nosso conteúdo; Lottie só para ícones pontuais, com licença conferida.

## Pendente
- Jessica: assistir com som e aprovar. Se aprovar: R2 do contrato e os 3 da série 20 no mesmo estilo.

## Próxima sessão
Copiar `serie_inteiro_motion.py` como base: trocar `painel` por `diagrama()` com banco escurecido e `desce()`.
