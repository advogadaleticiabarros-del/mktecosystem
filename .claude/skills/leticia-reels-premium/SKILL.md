---
name: leticia-reels-premium
description: Edição premium de Reels da Dra. Letícia a partir de gravação dela (padrão desde 21/10/2026). Use para "editar vídeo", "fazer reels" com um arquivo enviado, ou para construir/ajustar fala.py e conferir.py.
---

# Reels premium (padrão de 21/10/2026)

Teoria e regras completas: manual aprovado pela Jessica, "Manual de edição premium dos Reels" (Claude Docs, https://claude.ai/artifact/YbcSqBtFYo3ZF1vAbRCBDk). Leia o manual só quando a dúvida não estiver resolvida aqui. Detalhes do motor (blocos, área segura, transições, `serie.py`): skill `leticia-reels-motion`. Regras de conteúdo: `docs/MANUAL_CONTEUDO_REDES.md`.

## Regras fixas

- **Uma versão só por vídeo** (Jessica, 21/10/2026: economizar token e trabalho). Tudo é conferido antes do render final (`fala ok`, `--checar`, amostras); nada de versões de teste guardadas. Se o `conferir.py` acusar algo, corrija e gere de novo no mesmo nome, apagando antes o arquivo ainda não entregue (nunca o que já foi ao Orbit).
- **Sem música e sem ambiência**: voz tratada + efeitos sonoros. A ambiência (ruído de sala a −32 LUFS) virou chiado que abafava a voz da Dra. e foi tirada do motor em 21/10/2026.
- Fala **limpa**: sem pausa maior que 0,25 s, sem repetição, gaguejo ou muleta ("né", "então"), sem palavra cortada.
- Toda emenda no rosto tem **punch-in** alternado (8% a 15%) ou cobertura.
- **Algo muda na tela a cada 2 a 4 s.** No máximo 2 transições vistosas por vídeo; o resto é corte seco, punch-in ou match cut.
- Cada evento visual tem seu efeito sonoro, de 8 a 12 dB abaixo da voz; o efeito nunca cobre palavra.
- Motion graphics (catálogo do manual) para explicar; **3D obrigatório em 1 ou 2 momentos de destaque**; vídeo de banco só como fundo. O 3D sai do `producao/reels/motor3d/` (three.js) como clipe curto em `work/videos/` e entra no `serie.py` como cena de fundo. A validação de 21/10 ficou sem 3D e ela sentiu falta ("ficou menos dinâmico").
- Fechamento: pedido de envio **com o motivo** ("Manda para quem está afastado pelo INSS").
- Exportação: 1080×1920, 30 fps, H.264 de 10 a 12 Mbps, AAC 128 kbps a 48 kHz, −14 LUFS, pico −1 dBTP.
- Versão nova é peça e arquivo novos (`-v2`); nada pronto é sobrescrito.

## Economia de contexto

- Scripts imprimem só o resumo e os avisos. Nunca imprimir a transcrição inteira nem listas de arquivos.
- Imagem só na revisão final: uma folha pequena (10 quadros, 240 px de largura).
- Uma sessão por vídeo. Ao terminar, registre em `docs/CONTEXTO_PROJETO.md` e no relatório do dia.

## Passos

1. **Ferramentas.** Se `producao/reels/motor/fala.py` e `conferir.py` não existirem, construa-os primeiro (seção "Ferramentas" abaixo, com TDD e a skill `codebase-design`). Pronto quando os testes passam e as duas ferramentas rodam no vídeo da série 18 (`Downloads/IMG_0330.MOV`) reproduzindo o resultado da v2.
2. **Pasta.** `C:\tmp\videos-reels\NN-nome\` com `fontes\` e `work\` (cópia de `producao\reels\motor`). Pronto quando o bruto está lá e foi recebido em qualidade original.
3. **Fatos.** Transcreva (`py fala.py transcrever`), confira cada afirmação jurídica e anote lei e cortes no docstring do roteiro. Pronto quando toda afirmação mantida tem base legal anotada e o que é errado ou vetado pela OAB está na lista de cortes.
4. **Fala.** Liste os trechos em `fala.py` e rode até "fala ok". Pronto quando a ferramenta não acusa nenhuma emenda (palavra comida, sobra, repetição, pausa longa) e a transcrição da fala montada bate com o texto esperado.
5. **Roteiro de cena e som.** `serie.py`: cada frase com um tipo de cena (rosto com punch-in, peça de motion graphics, 3D, banco) e cada evento com seu efeito. Rode `--checar`. Pronto quando sai "área limpa: ok" sem aviso de LEITURA.
6. **Render e conferência.** Render completo; depois `py conferir.py <mp4>`. Pronto quando o relatório não tem aviso (congelamento, volume, área segura) e a folha final de quadros foi revisada uma vez.
7. **Orbit.** Backup do banco, mídia em `api:/app/media`, peça nova em rascunho com legenda (sem aviso de IA quando a voz é real). Pronto quando a contagem de Reels sobe e a mídia responde 200.
8. **Registro.** `docs/CONTEXTO_PROJETO.md`, arquivos de texto em `producao/reels/series/NN-nome/`, commit e push. Avise que ela precisa assistir com som antes de aprovar.

## Ferramentas

**Prontas desde 21/10/2026** (passo 1 feito; validação em `series/18-limbo-previdenciario/falas_premium.py` e `serie_premium.py`). Ao usar:
- `falas.py` de cada vídeo: `SRC`, `FALAS = {n: [(início, fim, "texto esperado"[, "fixo"])]}`, `VOCABULARIO` (termos do tema; sem ele o Whisper ouve "língua" por "limbo"). O texto esperado é o que ela fala no trecho, não o que se quer na legenda.
- Linha "nota:" não reprova: o corte ali só tirou silêncio, então a divergência é do Whisper. Corrija a legenda em `CORRIGE` do `serie.py`.
- Roteiro: marque `"rosto": True` no bg das cenas de rosto (punch-in automático) e use `m.fim_da_fala(...)` para o fim da fala.
- Rodar `fala.py montar` leva uns 10 min por Reel no processador (Whisper medium, precisa de ~3 GB livres).

Base: `producao/reels/series/18-limbo-previdenciario/montar_falas_v2.py` (pausas reais e `encostar`) e a v2 da série 18.

- **`fala.py`**
  - `transcrever <bruto>`: Whisper medium com palavras; grava o JSON e imprime só a duração e o número de palavras.
  - `montar`: recebe os trechos (início, fim, texto esperado).
    - Mede as pausas com silencedetect (−44 dB, ≥ 0,25 s) e encosta as pontas na pausa real.
    - Encurta as pausas internas para 0,18 s e acelera no máximo 5%.
    - Faz fusão de 10 a 30 ms nas emendas.
    - Retranscreve cada trecho isolado e compara com o texto esperado.
    - Imprime "fala ok" ou só as emendas com problema.
- **`conferir.py <mp4>`** imprime em poucas linhas:
  - imagem congelada (freezedetect, ignorando o fechamento);
  - volume integrado e pico (alvo −14 LUFS e −1 dBTP);
  - duração, resolução e taxa de bits;
  - cenas de banco mais longas que o clipe.
  - Também gera a folha de 10 quadros.
- **Ao construir, ajuste o motor:**
  - tirar a trilha musical;
  - loudnorm de −15 para −14;
  - CRF para taxa de 10 a 12 Mbps;
  - biblioteca de efeitos com 3 a 4 variações por tipo, sorteadas com semente fixa;
  - punch-in alternado nas cenas de rosto.
