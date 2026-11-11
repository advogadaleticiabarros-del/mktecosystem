# APIs públicas no Orbit (11/11/2026)

## Pedido
A Jessica clonou `public-apis/public-apis` e perguntou quais APIs melhorariam o Orbit e os outros projetos. Depois
pediu: "vamos instalar e colocar tudo até mesmo nos demais projetos".

## Feito (Orbit)
- Integrações novas, cada uma com interface pequena e transporte HTTP injetável:
  - `apps/api/app/integrations/brasil.py`: feriados, CEP e CNPJ;
  - `imagens/outros_bancos.py` (Openverse e Pixabay), `imagens/banco.py` (`BancoDeFotos`) e `imagens/remove_bg.py`;
  - `noticias/newsdata.py` e `noticias/camara.py`;
  - `site/pagespeed.py` e `site/safe_browsing.py`;
  - `email/verificador.py` e `links/bitly.py`.
- `services/datas_editoriais.py`: feriados nacionais mais as datas das áreas da Dra.
- Jornalista (`services/jornalista.py`): o NewsData entra quando há chave; a Câmara entra só sob encomenda.
- Chaves novas no painel de Configurações (`services/chaves_api.py`), com validação: Pixabay, NewsData, Google, Bitly
  e remove.bg. As variáveis correspondentes foram para `config.py` e `deploy/vps/.env.example`.
- Rotas `/ferramentas/*` (`routers/ferramentas.py`) e tela `/ferramentas` no painel (menu "Ferramentas").
- Resumo no `docs/CONTEXTO_PROJETO.md`, seção "APIs públicas e tela Ferramentas".

## Verificado
- `tests/test_apis_publicas.py`: 25 testes passando.
- Suíte inteira: 396 passaram. `test_renderiza_card_de_pergunta_1080x1350` falhou uma vez na suíte e passou sozinho,
  com ou sem estas mudanças (instabilidade de tempo do Playwright).
- Chamadas reais, sem chave:
  - funcionaram: feriados 2026/2027, CEP 01001-000, CNPJ de teste, Openverse, Câmara e Disify (detectou o
    mailinator como descartável);
  - não funcionou: o PageSpeed sem chave deu 429.
- `npm run build` do web: compilou, com a página `/ferramentas` gerada.
- **Não verificado:** deploy na VPS (não foi feito) e as rotas com chave real (Pixabay, NewsData, Google, Bitly e
  remove.bg), porque não há chaves cadastradas.

## Decisões e porquês
- Openverse filtrado só em CC0 e domínio público, para evitar obrigação de atribuição.
- Unsplash ficou de fora: exige aprovação do app.
- A Câmara não entra na ronda diária, porque projeto de lei não é notícia do dia e o risco com a OAB é maior.
- O verificador de e-mail aceita o contato quando os dois serviços caem (`conferido=False`): é melhor do que perder
  um contato real.
- Raspagem de Instagram e TikTok foi descartada (política da Meta).

## Pendente
- Jessica: criar e cadastrar as chaves (Pixabay, NewsData, Google Cloud com PageSpeed e Safe Browsing ativados, Bitly
  e remove.bg) e autorizar o deploy no Orbit.
- Safe Browsing v4 é para uso não comercial. Se o Orbit for vendido como SaaS, trocar pelo Web Risk.
- Scripts de produção em `apps/api/_saida_producao_1510/` ainda chamam `Pexels(...)` direto; podem passar para
  `criar_banco_de_fotos`.
- Outros projetos (CRM jurídico, CRM Comercial, Agenda, site da Rafa): ver o relatório de cada repositório.

## Próxima sessão
Depois das chaves, abrir `/ferramentas` no painel e testar cada bloco. Deploy pelo runbook `deploy/vps/README.md`.
Skills: `contexto-orbit`, `codebase-design`.
