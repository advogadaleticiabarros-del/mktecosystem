# 22/10/2026 — Medição de contatos e botões de contato no site (Frente 3)

## `/js/conversoes.js` (fonte: `producao/site/conversoes.js`)
- Incluído antes de `</body>` nas **83 páginas .html** do site com `?v=20261022b`. A tag é trocada a cada versão,
  porque a hospedagem manda guardar o arquivo por 30 dias. Originais em
  `/root/orbit-backups/site-20261022-193509-conversoes/`.
- Também nos templates `blog_artigo.html` e `jornal.html`, para os artigos novos já saírem com ele.
- **Eventos** (Analytics + pixel da Meta):
  - `contato_whatsapp`: clique em `wa.me` → pixel `Contact`;
  - `contato_ligacao`: clique em `tel:` → pixel `Contact`;
  - `generate_lead`: `fetch` para `/api/public/lead` com resposta OK → pixel `Lead`. O script intercepta o `fetch`,
    então vale para o `pages.js` e para os formulários próprios das LPs.
- A mensagem do WhatsApp passa a terminar com "(vim pela página: <título>)", com `%20` nos espaços.
- **Pixel da Meta (858690737244687):** é carregado nas páginas que não o tinham (artigos do template novo, LP
  gestante-clt…), na primeira interação ou em 2 s. Onde a página já tem o `fbevents.js`, não carrega de novo.
- **Ligar:**
  - botão "Ligar: (27) 99515-1402" dentro de `.article-cta`;
  - botão flutuante à esquerda no celular (até 768 px).
- **Bloco "Está passando por isso?"** no meio dos artigos, antes do `h2` seguinte a "Como provar" / "O que fazer" /
  "O que acontece", com WhatsApp contextual e Ligar. Texto impessoal, pela OAB.
- **Testado:**
  - Playwright com página de teste: eventos, mensagem do WhatsApp, posição do bloco, botão flutuante só no celular;
  - no site real: artigo 500, LP gestante-clt e home com os eventos no `dataLayer`, pixel carregado com o ID certo.

## Orbit
- `presenca_google._analytics` traz `contatos` (30 dias, por tipo e por página, pelo `eventCount` dos 3 eventos).
  A tela mostra o card "Contatos pelo site" no Resumo e a tabela "Que páginas geram contato" em Site e IAs.
- O primeiro número real deve aparecer em até 24 a 48 h (atraso do Analytics). Testes feitos hoje podem somar
  alguns contatos.

## Pendente (Jessica)
- Marcar `contato_whatsapp`, `contato_ligacao` e `generate_lead` como **eventos principais** no Analytics.
- A LP `lp/empresas-adequacao-trabalhista-2026.html` (não publicada) recebeu o script no repositório, mas não tem o
  código do Analytics.
- `lp/guia-direitos-gestante-trabalhadora.html` no repositório foi alinhada com a versão do site.
