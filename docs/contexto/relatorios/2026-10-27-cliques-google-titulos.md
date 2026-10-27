# 27/10/2026 · Cliques no Google: títulos e descrições do site

## Pedido
Print da tela "Google e site": "o que devemos fazer para aumentar esses cliques?", depois "faça tudo que puder para
mim, vamos reverter isso, mais cliques, mais conversões".

## Feito
- Auditoria pública das 71 páginas do sitemap (título, descrição, eventos de contato). Quase todo título passava de
  60 caracteres (sufixo `| Dra. Letícia Barros`), descrições de 160-220, três com termos vetados pela OAB, índice do blog
  com duas meta descriptions.
- Gerador de artigos (Orbit): `titulo_da_aba` (marca só quando cabe em 60) nos templates de artigo e jornal;
  `REGRAS_TITULO_GOOGLE` nos prompts de artigo e jornal.
- `blog_seo.trocar_titulo_e_descricao` (troca só `<title>` e meta description, junta metas repetidas em qualquer ordem
  de atributo) e `apps/api/scripts/aplicar_titulos_google.py` (simula por padrão, backup .tgz, IndexNow).
- 66 títulos/descrições novos em `producao/seo/2026-10-27-titulos-google.json`, com o motivo de cada um.
- Contexto em `docs/CONTEXTO_PROJETO.md` (seção "Cliques no Google" e pendência).

## Verificado
- Testes: 344 da API passaram após a mudança do template e do prompt; depois, 19 de `test_blog_seo` e
  `test_render_artigo_blog` (5 novos).
- Simulação nas cópias baixadas das 66 páginas: todas ficam com um `<title>` e uma meta description.
- Todos os títulos ≤ 60 caracteres; descrições entre 110 e 155; sem travessão nem termos vetados.
- Não verificado: nada foi aplicado no site nem publicado no Orbit (deploy da API não feito).

## Decisões e porquês
- Sem os dados de consultas do Search Console (leitura em produção barrada), a correção foi pelo que vale para todas
  as páginas: título que cabe no Google e descrição com a resposta. Refinar por consulta fica para quando houver os dados.
- H1 e og:title não mudam: o título da aba é para o Google; o H1 e o compartilhamento seguem com o texto da página.

## Pendente
- Jessica: autorizar o acesso à VPS para (1) simular e aplicar os títulos, (2) fazer o deploy da API, (3) ler a aba
  Buscas do painel salvo.
- Jessica/Dra.: marcar `contato_whatsapp`, `contato_ligacao` e `generate_lead` como eventos principais no GA4; conferir o
  campo "site" do Perfil da Empresa; corrigir os artigos de aposentadoria híbrida e carga horária.

## Próxima sessão
Na VPS: `docker compose cp` do JSON e do script para `/tmp`, rodar sem `--aplicar`, conferir, rodar com `--aplicar`,
copiar o .tgz para `/root/orbit-backups/`.
