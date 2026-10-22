# 22/10/2026 — Analytics nas LPs e plano de cliques, conversões, Google e IAs

## Feito no site (no ar)
- Código do Google Analytics (G-5B513VWB4D, com carregamento adiado igual ao da home) colocado nas 23 páginas que
  estavam sem ele: `lp/` (6), `lp-v3/` (10) e `areas/` (7). Originais em `/root/orbit-backups/site-20261022-174308/`
  na VPS.
- LP `lp/guia-direitos-gestante-trabalhadora.html`: pixel da Meta de exemplo (`SEU_PIXEL_ID_AQUI`) trocado pelo
  real (858690737244687).

## Achados que mudaram o plano
- **Nenhuma conversão é medida.** Os cliques em `wa.me` e o envio de formulário não mandam evento ao Analytics nem
  ao pixel. Os formulários enviam para o CRM jurídico (`js/pages.js`).
- **Não existe link `tel:`** em nenhuma página.
- **O link do site no Perfil** vai para `contato.advogadaleticiabarros.com.br`, uma página antiga de WordPress com
  `noindex` e sem Analytics.
- **Search Console por artigo:**
  - Limpeza de banheiro: "atendente pode fazer limpeza de banheiro" (97 aparições, posição 8,3), "recepcionista pode
    fazer limpeza" (47; 6,7), "atendente pode lavar banheiro" (40; 9,3), "lavar banheiro é desvio de função" (37; 5,7).
  - Licença de 180 dias: "licença maternidade mudou para 180 dias" (24; posição 10). Para "quem tem direito" o
    artigo já está em 1º.

## Artigos reforçados (rascunho, NÃO publicados)
A pedido dela, viraram o item 1 do plano em vez de serem publicados. Estão em
`producao/blog/reforco-2026-10-22/` (`*.original.html`, `*.v2.html` e o script `reforcar.py`). Têm título,
descrição, H1, `dateModified`, seção nova e 3 perguntas a mais no FAQ (texto e JSON-LD validados). Antes de
publicar: decidir o bloco "Caso real do escritório" do artigo da limpeza (divulga a condenação de R$ 15 mil e o
total de R$ 28 mil, o que é risco pela OAB).

## Plano
Claude Doc "Plano: mais cliques, ligações e formulários (Google e IAs)":
https://claude.ai/artifact/HdTr66d4Hzd27VqrFjmQpd. Tem números de hoje, metas até 31/12, quatro frentes
(cliques, Perfil, conversões, IAs), cronograma de 27/10 a 31/12, regras da OAB e decisões da Dra.

## Observação técnica
`conformidade_oab.py` acusa "garante" e "R$" também em texto informativo de artigo ("a lei garante"). Ele é usado só
em textos que vão para o Google (posts, respostas, perfil), onde essa rigidez é desejada. Para usar em artigos,
precisa de um modo que diferencie promessa de informação.
