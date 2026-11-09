# Reels: onde achar a calculadora do 13º na bio (09/11/2026)

- Vídeo motion `producao/reels/bio-calculadora-13/reels-bio-calculadora-13.mp4` (24 s, 1080×1920, HyperFrames, projeto em `video/`).
- Fluxo: perfil (desenho genérico, sem marca do app) → toque no link → página /bio/ rolando até a calculadora → salário R$ 3.000 → contato → resultado real (R$ 2.751,40) → CTA "Clique no link da bio e faça o seu cálculo".
- Telas reais capturadas por `capturar.py`, com rede bloqueada e o envio ao CRM respondido localmente: **nenhum lead de teste foi criado**. Nome/e-mail no vídeo são fictícios (Maria Souza).
- Sons: cliques e um sino sintetizados, sem música.
- Legenda com foco em SEO e respostas de IA: `legenda.md`.
- Não agendado. Reels só terça e sexta 21h (próximas: 10/11 e 13/11).

## Versão 2, detalhada (09/11/2026)

- `reels-bio-calculadora-13-v2.mp4` (47 s). A v1 continua guardada.
- Abertura com o **perfil real** (@adv.leticiabarros2, foto, números e os 12 últimos posts, lidos pela API do Instagram com `baixar_feed.py`, só leitura). Atenção: o @ certo tem o "2"; a v1 mostrava @adv.leticiabarros.
- Navegação real gravada quadro a quadro (`gravar.py`): salário R$ 4.500, comissão R$ 800, horas extras R$ 300, 1 dependente → total R$ 4.829,38 (INSS R$ 585,51, IR R$ 185,11). Rede bloqueada, nenhum lead criado.
- Composição gerada por `montar.py`; legenda nova em `legenda-v2.md`.
- Página de aprovação atualizada: https://claude.ai/artifact/9AwWip5MJtxiWnNa1pMXMW (registro em `aprovacoes/reels-bio-calculadora-13-v2`).

## Versão 3 (09/11/2026)

- `reels-bio-calculadora-13-v3.mp4` (50 s): igual à v2, mais zoom no Seguir → "Seguindo ✓" → volta e toque no link; som de moedas quando o resultado aparece (sino mantido no total). v1 e v2 guardadas.
- Página de aprovação atualizada (registro em `aprovacoes/reels-bio-calculadora-13-v3`).

## Aprovado e programado (09/11/2026)

- A Jessica aprovou a v3 e pediu para postar hoje no horário de maior atividade. Programado para **09/11/2026 às 21h** no Instagram (peça `72b8aca8`, pauta `9ef1e59b`), com `subir_reels.py`; vídeo em `/media/reels-bio-calculadora-13-v3.mp4`.
- A API não devolveu dados de seguidores online (`online_followers` vazio); 21h é o horário de pico dos Reels pelos dados do perfil usados na agenda.
- Exceção pedida por ela à regra "Reels só terça e sexta": hoje é segunda. Amanhã (10/11, 21h) já há outro Reels na fila (13º proporcional).
- Lembrete: trocar o link do perfil para advogadaleticiabarros.com.br/bio antes das 21h.
