# Reels animado "demissão por vingança" (assédio eleitoral) · 27/10/2026

## Pedido
Jessica: "gerar um reels completo sobre o assunto que já falamos, assédio eleitoral em vingança"; "conseguimos clonar a
voz da Dra. Letícia dos reels que já temos? veja se alguma dessas skills.sh ajudam"; "reels completo com animações
[...] use toda aquela estratégia para viralizar".

## Feito
- Roteiro v2 no ângulo "vingança" pós-eleição: `producao/reels/series/22-assedio-eleitoral-motion/roteiro-vinganca.txt`
  (a v1 `roteiro.txt` + `serie.py` ficou intacta). Duas partes com o mesmo corpo: gancho A "Perdeu o emprego por
  vingança, depois da eleição?" (seguidores) e gancho B "A eleição acabou. Mas o seu voto não pode custar o seu
  emprego." (Trial Reels).
- Cenas: `serie_vinganca.py` (gancho → 140 denúncias em pó de ouro → voto secreto na foto real da urna → carimbo
  "Dispensa discriminatória" → "Voltar ao trabalho" → "2x" + dano moral → provas "antes de sair do grupo da empresa" →
  denúncia sigilosa → "Salve e mande para quem precisa saber"). Gancho B na foto da urna (TSE, domínio público); cena
  do voto secreto na urna da Agência Senado (CC BY 2.0, crédito na tela). Créditos em `creditos-pexels.txt`.
- Legenda, primeiro comentário e TikTok: `legendas_vinganca.py` (linha 1 com 122 caracteres, 5 hashtags, aviso de
  narração com IA, pergunta de opinião no primeiro comentário).
- `clonar_voz.py`: cria o clone Instant pela API com a amostra de 3 min 54 s e grava o voice id novo no arquivo de
  config (guarda o antigo).
- Prévias com a voz antiga (só para aprovar o visual): `C:\tmp\videos-reels\22-assedio-eleitoral-motion\PREVIA-voz-provisoria-demissao-por-vinganca-1.mp4` e `-2.mp4`.
- `docs/CONTEXTO_PROJETO.md`, seção da campanha.

## Verificado
- `narrar.py --checar` sem aviso; `serie_vinganca.py --checar`: "área limpa: ok" nos dois, sem aviso de LEITURA.
- Amostras conferidas por imagem (acentos, contraste, texto fora do rosto); gancho B e cena da urna ajustados (véu e
  desfoque) depois da 1ª revisão.
- Chave do ElevenLabs testada: só tem Text to Speech (401 em `voices_read` e `user_read`), então não cria clone.
- Render das prévias: as duas em 1080×1920 H.264 + AAC, 44,0 s (gancho A) e 42,6 s (gancho B), voz em −15 LUFS;
  quadros do gancho, do "140", do "2x" e do fechamento conferidos. Cópias em `Desktop\ASSEDIO ELEITORALeels-previa-voz-provisoria\`
  e em `https://api.orbit.advogadaleticiabarros.com.br/media/PREVIA-voz-provisoria-demissao-por-vinganca-1.mp4` (e `-2`).
- Não verificado: qualidade do clone novo (não existe ainda).

## Decisões e porquês
- Arquivos novos em vez de editar a v1 (regra "material pronto nunca some").
- "Recorde no ano" e "Cada caso tem detalhes..." saíram da fala e ficaram só na tela: com a voz antiga a parte 1 dava
  46 s + fechamento; agora 40 s de fala (teto do perfil: 45 s).
- Skills do skills.sh: nenhuma clona voz. `hyperframes-animation` (HeyGen) traz receitas GSAP que o motor já cobre;
  `instagram-marketing` ajuda em gancho e legenda; `Trail-Code/` é mapa de código para agentes. Clone local
  (VoiceStudio) continua parado esperando liberação dela (pedido de 18/10).
- Clonar pelo site ou pela API dá o mesmo resultado; o script existe para não depender de copiar o id à mão.

## Pendente
- Jessica: no ElevenLabs, dar à chave a permissão "Voices: Write" (Developers → API Keys → editar) **ou** criar a voz
  em Voices → Add a new voice → Instant Voice Clone com `Desktop\NOVOS REELS\voz-para-clonar-leticia.wav` e mandar o
  voice id.
- Jessica: aprovar o visual pelas prévias e escolher o dia (Reels 1 terça ou sexta 21h; Reels 2 como Trial).
- Impulsionamento continua exigindo a autorização de "temas sociais, eleições ou política" da Meta.

## Próxima sessão
Com a permissão: `cd C:\tmp\videos-reels\22-assedio-eleitoral-motion\work` → `py clonar_voz.py` → frase de teste para
ela aprovar → `py narrar.py ../fontes/roteiro-vinganca.txt ../fontes/vinganca` → `NARRACAO=vinganca py
serie_vinganca.py --checar` → `--amostras` → `1 2` → subir no Orbit (skill `leticia-reels-motion`, passo 11).
