# 22/10/2026 — Frente 2 do plano: ajustes no Perfil da Empresa (feitos pelo Orbit)

## Aplicado no Google (aceito na hora, sem edição pendente)
- **Link do site:** saiu `contato.advogadaleticiabarros.com.br` (WordPress antigo, `noindex`, sem Analytics). Entrou
  `https://advogadaleticiabarros.com.br/?utm_source=google&utm_medium=organic&utm_campaign=perfil-empresa`.
- **Serviços:**
  - Corrigidos: "RescÏsão" → "Rescisão", "Assedío"/"assedíio" → "Assédio", "resgatórias" → "rescisórias",
    "alimenticia" → "alimentícia", "Previdenciaria" → "previdenciária".
  - Previdenciário ganhou descrição. Vínculo empregatício: "precisa garantir os direitos" → "quer ter os direitos
    trabalhistas reconhecidos".
  - "Advogada Penal" e "Advogada Consumidor" ficaram como estavam (decisão da Dra.). Os 7 serviços padrão do Google
    foram mantidos.
- **Descrição nova** (697 caracteres): cita Vitória/ES e a Enseada do Suá, tem a lista de atuação e não usa
  "Especialista" (se a Dra. tiver o título, dá para devolver).
- **Botão "Agendar"** (APPOINTMENT) criado: `wa.me/5527995151402` com o texto "Olá, vim pelo Google e gostaria de
  agendar um atendimento".
- **Avaliações:** as 15 já estavam respondidas (as 2 pendentes foram respondidas hoje fora do Orbit).

## Posts do Google
- **22 posts** da produção anterior (`apps/api/_saida_producao_1510/pecas/`) foram para a fila do Orbit
  (`google_posts`). As imagens estão em `/app/media/google-post-<slug>.jpg`. Cada post tem o botão "Saiba mais" para
  o artigo com `utm_campaign=post-perfil`.
- **Publicado agora (LIVE):** Outubro Rosa / Lei 15.377.
- **8 agendados (`aprovado`):** terças, 10h de Brasília, de 27/10 a 15/12. Todos os artigos deles respondem 200.
- **13 rascunhos** (novembro e dezembro): os artigos ainda dão 404. Ela aprova na tela ("Aprovar e agendar", botão
  novo) quando o artigo for ao ar.

## Código
- `conformidade_oab.py`: "garantimos/garanto/garantia de êxito" bloqueiam; "a lei garante" passa. Oferta
  comercial (% de desconto, parcelamos, R$) bloqueia; "os descontos do 13º" passa. Testes novos; 308 passando.
- Tela Posts: botão "Aprovar e agendar" para rascunho ou erro.

## Pendente com a Dra.
- 10 fotos para o Perfil.
- Pedir avaliação a clientes com caso encerrado.
- Decidir "Penal" e "Consumidor".
- Confirmar o título de especialista.
