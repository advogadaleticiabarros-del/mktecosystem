# Manual de Conteúdo: Instagram e Facebook (regras obrigatórias)

Versão de 08/10/2026. Documento completo e comentado, com fontes:
https://claude.ai/code/artifact/3927cd5d-9428-4056-a928-2c779b46ea2b

Toda peça (carrossel, frase, pergunta, estático, Reels, Stories, post de Facebook)
gerada pelo Orbit ou montada à mão segue estas regras. Ordem de prioridade quando
houver conflito: **OAB > Meta > design system > criatividade/algoritmo**.

## 1. OAB (eliminatório)

Base: Provimento 205/2021 (em vigor; revisão no Conselho Federal ainda não publicada)
e Código de Ética e Disciplina.

- Proibido prometer ou insinuar resultado. Usar "pode ter direito", "a lei prevê".
- Proibido mencionar valores, honorários, "consulta gratuita", "sem compromisso",
  desconto, parcelamento (art. 3º I).
- Proibido divulgar caso concreto, sentença, acordo ou decisão de processo em que ela
  atua; depoimento, print de conversa, foto com cliente (art. 4º §2º, art. 5º §3º,
  CED art. 42 IV). Decisão pública de STF/STJ/TST de outros processos pode.
- Proibido "especialista em X" sem título certificado; usar "atuação em" (art. 3º III).
- Proibido superlativo, autoengrandecimento, comparação com colegas (art. 3º IV).
- CTA sempre impessoal: "procure uma advogada de confiança". Nunca "me chama",
  "contrate", "foi lesado? posso te ajudar", urgência de venda.
- Texto não pode induzir a litigar ("entre com ação!"); informa a regra.
- Responder dúvidas só em tese, encerrando com "cada caso precisa ser avaliado";
  nunca analisar o caso de alguém em público (CED art. 42 I).
- Impulsionar só conteúdo informativo, sem oferta de serviço.
- Proibido ostentação (carro, viagem, bens), símbolos oficiais da OAB, pagar por
  ranking/prêmio, comprar engajamento.
- Imagem gerada por IA nunca representa a Letícia, clientes ou o escritório
  (induz a erro, art. 3º II). Último slide usa foto real dela.
- OAB/ES 39.948 na legenda ou no último slide.

## 2. Meta (eliminatório)

- Só conteúdo original; notícia de terceiro entra transformada (nossa leitura e design).
- Sem marca d'água de outro app (CapCut, TikTok).
- Vídeo/áudio fotorrealista feito ou alterado com IA: ligar o rótulo "Informações de IA".
- Máximo **5 hashtags** por post/Reels (limite da plataforma desde 18/12/2025),
  específicas, em CamelCase. A regra antiga de 8-12 está revogada.
- Música: em peça que pode ser impulsionada, só Meta Sound Collection ou voz original.
- Reels elegível à recomendação: até 3 min, 9:16 tela cheia, sem borda, boa resolução.

## 3. Especificações

| Formato | Canvas | Área segura |
| --- | --- | --- |
| Carrossel / estático / frase / pergunta | 1080×1440 (3:4) — padrão novo; render atual ainda gera 1080×1350 | conteúdo crítico na faixa central 1080×1350; 60 px laterais |
| Reels | 1080×1920 | texto entre y=250 e y=1250; 120 px livres à direita |
| Capa do Reels | 1080×1920 | título no recorte central 3:4 (aparece no grid) |
| Stories | 1080×1920 | 250 px livres topo e base |
| Feed Facebook | 1080×1350 (4:5) | mesma faixa central |

Carrossel: 7 a 10 slides, todos na mesma proporção. Exportar em 1080 px de largura,
sRGB, PNG para texto, JPG 90+ para foto. Reels: MP4 H.264, 30 fps, áudio AAC, 20-60 s.

## 4. Design system (valores em `TenantConfig.identidade_visual`)

- Contraste medido: branco/fundo_escuro 15,3:1; areia/fundo_escuro 12,4:1;
  café/areia_light 11,3:1; dourado/fundo_escuro 7,3:1; fundo_escuro/dourado 7,3:1.
- **Proibido**: texto dourado em fundo claro (1,9:1) e texto branco em fundo dourado (2,1:1).
- Proporção 60-30-10: fundos escuros / texto branco-areia / dourado. Slide claro
  (areia_light + café) no máximo 1 a cada 4.
- Escala no canvas 1080: gancho Cormorant Garamond 96-120 px; título Playfair Display
  60-72 px; destaque Playfair itálico dourado (1 a 3 palavras); corpo Inter 32-36 px
  (até 40 palavras/slide); kicker Inter 600 caixa-alta 24-26 px; rodapé 22-24 px.
  **Nada abaixo de 22 px.**
- Grid: margens 72 px, 6 colunas, calha 24 px, ritmo de 8 px. Raios 8/12/20/30.
- Assinatura: acabamento dourado topo/rodapé sempre; kicker com a área do direito;
  paginador "03 / 08"; foto real da Letícia no fechamento.
- Foto de fundo com overlay fundo_escuro 55-70%; conferir o render final (logos,
  dados pessoais). Sem clichê de banco (martelo, balança, aperto de mão).
- Texto alternativo em toda imagem, com a palavra-chave. Reels com legenda queimada.

## 5. Copy

- Gancho = dúvida real da cliente, nas palavras dela. Nunca "Foi sancionada a lei X".
- Palavra-chave na capa, na linha 1 da legenda e no alt text (posts aparecem no Google).
- Legenda: palavra-chave + gancho; contexto curto; até 5 itens com emoji-ícone;
  ressalva "cada caso tem detalhes"; CTA de engajamento (salvar/enviar) obrigatório;
  CTA jurídico impessoal; assinatura com OAB; 3-5 hashtags.
- Voz: sem travessão, sem clichês de IA, sem superlativo vazio, sem lista automática
  de três, nunca "deficiência" (usar "necessidades especiais"), sempre direito + risco.
- Reels: 0-3 s gancho falado e escrito; 3-10 s problema; 10-35 s regra com corte a cada
  2-4 s; fechamento com ressalva + "manda pra quem precisa", emendando no início (replay).

## 6. Algoritmo e métricas

- Sinais que importam: tempo assistido, envios por alcance (3-5x a curtida),
  curtidas por alcance; salvamentos como indicador de valor.
- Primeira hora: responder todos os comentários.
- Mínimo 2 Reels/semana, um testado como Trial Reels.
- Avaliar após 7 dias: envios e salvamentos por alcance, % até o último slide,
  retenção nos 3 primeiros segundos, visitas ao perfil.

## 7. Não fazemos

Trend de dancinha, "POV: cliente ganhou a causa", quiz "você tem direito?" que termina
em convite a contratar, grid em mosaico, repost de vídeo alheio.
