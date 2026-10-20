# 20/10/2026 — Série 18: Reels "Limbo previdenciário"

## Pedido
"Vou te entregar mais um vídeo para fazermos alguns reels, está na pasta de Downloads, IMG_0330."

## Feito
- Transcrição (Whisper medium) do vídeo de 3 min 07 s. O tema é limbo previdenciário.
- Ela aprovou o plano de 2 Reels com 3 cortes:
  - "auxílio-acidente", nome errado do benefício;
  - "o contrato fica suspenso", tecnicamente errado;
  - o caso de 10 meses do escritório, risco perante a OAB.
- Falas montadas por corte entre palavras. 8 vídeos do Pexels escolhidos em folha de contato (créditos em `creditos-pexels.txt`).
- Roteiro visual no motor v2, no padrão da série 17.
- Legendas: sem aviso de IA, porque a voz é real.
- Tudo de texto em `producao/reels/series/18-limbo-previdenciario/`. Mídia em `C:\tmp\videos-reels\18-limbo-previdenciario\`.
- No Orbit: 2 peças novas em rascunho, sem data.

## Verificado
- `serie.py --checar`: área limpa ok nos 2 Reels, sem aviso de LEITURA depois do ajuste da âncora.
- Amostras e quadros dos vídeos finais revisados:
  - com zoom 1.22 a testa saía cortada; mudei para 1.12 e `DY -200`;
  - no Reels 2, "É da empresa" aparecia antes da hora porque a âncora pegou o "é" da pergunta; corrigido e renderizado de novo.
- Arquivos: 1080×1920, H.264, AAC 128 kbps, 54,9 s e 54,0 s.
- Orbit: contagem de Reels de 36 para 38. Os dois vídeos respondem 200 pelo link público de mídia.
- **Não verificado:** a reprodução completa com som (conferi só quadros).

## Decisões e porquês
- **2 Reels de cerca de 55 s, e não 3 partes:** a fala útil, depois dos cortes, rende cerca de 100 s.
- **Cortes extras** de trechos repetidos (o exemplo repetido e "o médico constatou…") para caber.
- **Assinatura:** o Whisper ouviu "aqui nesse vídeo eu" no Reels 2; a legenda na tela foi corrigida para "nesse perfil", como no Reels 1 (é o mesmo áudio).
- **Vídeo do Pexels "empresa":** é o mesmo vídeo usado no "treinamento" da série 17 (8124286). Pode ser trocado se ela achar repetitivo.

## Pendente
- A Jessica (ou a Dra.) aprovar no Orbit e escolher os dias: às 21h, em dia sem outro post, com a parte 2 logo depois da 1.

## Próxima sessão
1. Se ela pedir ajuste, fazer versão nova (`-v2`, peça nova; regra "material pronto nunca some").
2. Rodar a partir de `C:\tmp\videos-reels\18-limbo-previdenciario\work` com `py serie.py N`.

Skills: `leticia-reels-motion`, `contexto-orbit`.
