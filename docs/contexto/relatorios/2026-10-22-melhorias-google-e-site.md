# 22/10/2026 — Melhorias da tela "Google e site" aplicadas

## Posts do Google
- Os 8 posts agendados com artigo no ar foram publicados de uma vez, a pedido dela. Com o do Outubro Rosa, são 9 no
  ar.
- Os 13 de novembro e dezembro foram aprovados por ela na tela, mas os artigos ainda dão 404. **Trava nova**
  (`central_google.artigo_no_ar`, por SFTP): o job e o "Publicar agora" só publicam quando o artigo do link existe no
  site. Até lá o post fica `aprovado` com o aviso "Aguardando o artigo ir ao ar" e é tentado de novo a cada 5 min.
  Teste novo; 309 passando.

## Site (originais em `/root/orbit-backups/site-20261022-182256/` e `.../site-20261022-182336/`)
- **Título e descrição novos**, com as buscas reais do Search Console:
  - aborto espontâneo: "quantos dias de atestado", art. 395;
  - carga horária: "8h por dia, 44h por semana";
  - mãe adotante: título encurtado;
  - pai não paga pensão: "pai não pagou ou atrasou a pensão".
- **`blog/index.html`** ganhou meta description.
- **Artigos reforçados no ar:**
  - Limpeza de banheiro (v3): título "Atendente pode lavar banheiro?", seção função por função, 3 perguntas novas no
    FAQ. O bloco "Caso real do escritório" virou "Um exemplo que chega ao escritório", **sem o resultado e sem os
    valores** (R$ 15 mil / R$ 28 mil), pela OAB. O texto anterior está no backup e em
    `producao/blog/reforco-2026-10-22/`.
  - Licença de 180 dias (v2): "Licença-maternidade mudou para 180 dias?", resposta rápida, seção "Quem tem direito a
    180 dias", 3 perguntas novas no FAQ.
- O site grava os arquivos com quebra de linha CRLF; os arquivos novos foram gravados assim também.

## Perfil
- Serviço "Advogada Consumidor" → "Advogada do consumidor", com a descrição tirada de `areas/direito-consumidor.html`.
- "Advogada Penal" segue sem descrição: não há página de área penal no site, então a decisão é da Dra.

## Melhorias marcadas como feitas
`gsc-quase-primeira-pagina`, `gsc-ctr-baixo`, `palavras-so-marca`. `site-sem-descricao` some na próxima coleta.

## Pendências
- Fotos reais para o Perfil (não há sessão de fotos; foto de banco é proibida pelo Google).
- Pedidos de avaliação a clientes.
- Decidir o serviço "Penal".
- **IndexNow respondeu 403** ("UserForbiddedToAccessSite"): a chave abre no navegador e para o bingbot, então o mais
  provável é a proteção anti-robô da Hostinger barrando o verificador do IndexNow. Solução: liberar no hPanel ou criar
  a conta no Bing Webmaster (importar do Search Console) e enviar o sitemap por lá.

## Atualização: chave do Bing (commit 3382c1e, no ar)
- Configurações → chaves ganhou o provedor **"Bing Webmaster"** (`chaves_api.PROVEDORES["bing"]`). A chave é
  validada com `GetUrlSubmissionQuota` para o site.
- O publicador do blog, depois de publicar, envia `[url do artigo, /blog/]` pela API `SubmitUrlbatch`
  (`site_descoberta.avisar_bing`) quando a chave existe. O IndexNow continua sendo chamado.
- Falta: ela criar a conta no Bing Webmaster (importar do Search Console), gerar a chave e colar no Orbit.
