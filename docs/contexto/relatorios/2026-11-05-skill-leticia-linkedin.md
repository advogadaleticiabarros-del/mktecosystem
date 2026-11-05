# Skill leticia-linkedin (05/11/2026)

## Pedido
Jessica pediu para achar a skill `hattip-linkedin-os` e dizer como ajuda. Depois: "crie a nossa com o que já temos definido e mais essas informações e ferramentas que podemos usar, vamos aproveitar e aprimorar".

## Feito
- Criada `.claude/skills/leticia-linkedin/`: `SKILL.md` (caminhos Escrever e Revisar), `referencias/` (escrita, formatos, entrevista semanal, notícias e gatilhos, desempenho) e `conferir_post.py` com testes.
- O verificador reutiliza `verificar_texto_oab` do Orbit e acrescenta palavras proibidas, travessão, oferta direta, datas relativas, experiência afirmada, fórmulas de IA, tamanho, gancho e hashtags.
- Primeiro teste: `producao/linkedin/revisao-2026-11-05-fila-10-a-19-nov.md` e `revisao-2026-11-05-textos-sugeridos.json`.
- Ponteiros em `CLAUDE.md`, `docs/ESTRATEGIA_LINKEDIN_PME.md` e `docs/CONTEXTO_PROJETO.md`.
- Fila do Orbit, código de produção e site não foram alterados.

## Verificado
- `pytest` da skill: 10 passaram. Os testes pegaram um bug real ("O ex-empregado" era bloqueado).
- Verificador rodado na fila e nos textos sugeridos: nenhum bloqueio.
- Em 05/11, LP de empresas e PDF do checklist deram 404. Artigos dos posts de 17, 18 e 19/11 estão no ar, escritos para o trabalhador.
- Tema 27: Pleno em 28/09/2026 segundo Conjur; o acórdão não foi lido.
- 13º: 20/12/2026 é domingo; notícias e `docs/PLANO_CONTEUDO_DEZ_2026.md` tratam o prazo como 18/12.
- **Não verificado:** fila real no Orbit (leitura em produção bloqueada pela permissão automática; revisão feita nos JSON de 23/10), publicação do post de 05/11, art. 477 da CLT, Resolução CFM 1.658/2002 e Lei 14.457/2022 na fonte oficial, e uso da skill numa sessão nova.

## Decisões e porquês
- Skill própria em vez de instalar a Hat Tip: é em inglês, para fundadores de tecnologia, com formatos que esbarram na OAB, estratégia própria e oferta da agência.
- Pilares, cadência e funil continuam os da estratégia até 31/01/2027, como a Jessica pediu.
- Dos 9 formatos da Hat Tip, 8 foram adaptados. Marcar pessoas ficou fora de uso, e o print de tweet virou "Frase que se ouve". "Bastidor sem caso" vem da `voz-leticia`.
- Regras da Hat Tip contra pergunta e contraste foram suavizadas, porque são marcas da voz da Dra.: fica o que ensina, sai o decorativo.
- As regras novas ficaram no verificador da skill, não em `conformidade_oab.py`, para não mudar o que bloqueia no Orbit e no Google. `sugerir_post` (`VOZ_LINKEDIN`) também não mudou.
- Tamanho do gancho (140 caracteres) é aproximado, sem fonte oficial.

## Pendente
- **Jessica e Dra.:** aprovar os textos sugeridos de 10/11 e 11/11, os dois com erro de fato, antes das datas.
- **Jessica:** subir a LP e o PDF até 11/11 ou mudar a data do post de 12/11.
- **Jessica:** decidir o link dos posts de 17, 18 e 19/11 e confirmar se o "caso dos supermercados no ES" é público e não é da Dra.
- **Dra.:** confirmar "os erros que mais vejo" e fazer a primeira entrevista semanal.
- **Jessica:** push. Em 04/11, `alcancelegalmkt-collab` recebeu 403 neste repositório, e o uso de `advogadaleticiabarros-del` depende de ok.
- Ideias sem pedido: bloco "Para empresas" nos artigos, posts com imagem no Orbit e alinhar `VOZ_LINKEDIN` à skill.

## Próxima sessão
Com o ok da Jessica, comparar os textos com a tela `/linkedin` e aplicar 10/11 e 11/11. Skills: `leticia-linkedin`, `contexto-orbit`.
