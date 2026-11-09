# Estilo Flagrante (Reels motion)

Nome dado em 09/11/2026, quando a Jessica aprovou os 13 primeiros ("Todos aprovados"). Quando ela pedir
"faz um Flagrante" ou "Reels no estilo Flagrante", é este. Começou no Reels 23:47 (06/11/2026).

## O que é
- Uma cena do dia a dia do trabalho "pega no flagra": mensagem do chefe, holerite, folha de ponto, extrato,
  calendário, cronômetro.
- Fundo café, fios de ouro em cima e embaixo, cartões cor de papel, números grandes em EB Garamond.
- Sem narração e sem música, só efeitos sonoros reais da Mixkit e a vibração do celular. Rótulo de IA desligado.
- Volume a -14 LUFS.
- Pergunta final em marca-texto dourado ("Pode descontar?", "Cadê o depósito?") e um pedido de comentário.
- Fechamento fixo:
  - logo e OAB;
  - **"Leia a legenda"**;
  - "Quer ficar por dentro dos seus direitos? Clique em seguir e compartilhe com quem precisa saber disso.";
  - "Cada caso tem detalhes. Procure uma advogada de confiança."
- Duração de 22 s, com o fechamento nos últimos 6 s.
- A explicação jurídica fica **na legenda**, com o artigo de lei e 📌 do que vale saber. A legenda leva a frase de
  seguir e compartilhar e 5 hashtags.

## Como fazer um novo
1. Copie um episódio de `producao/estilos/papel-e-ouro/motion-diario/` (por exemplo `11_fgts.py`) para `NN_assunto.py`.
2. Troque a cena, os sons e a legenda. A mecânica visual deve ser nova a cada assunto.
3. Gere a prévia com `python NN_assunto.py amostras` e confira a folha `amostras.jpg` e a mensagem "ok" da área segura.
4. Gere o vídeo com `python NN_assunto.py video`. O resultado sai em `NN-assunto/NN-assunto-v2.mp4`, junto com `legenda.json`.
5. Inclua o episódio em `gerar_pagina.py` e republique a página de aprovação para a Dra.

## Regras
- Situação fictícia: comentários respondidos só em tese.
- Ritmo de pelo menos 2 por semana.
- Material pronto não é sobrescrito: uma versão nova é um arquivo novo.
