---
name: leticia-linkedin
description: LinkedIn da Dra. Letícia Barros (PMEs, RH e contadores). Use SEMPRE que o assunto for LinkedIn, mesmo com grafia errada ("linkdin") ou pergunta simples: escrever ou revisar post, fila, pautas, entrevista semanal, notícia ou decisão recente, desempenho, página da empresa.
---

# LinkedIn da Dra. Letícia

Fontes de verdade, nesta ordem: OAB (`docs/MANUAL_CONTEUDO_REDES.md`, seção 1), estratégia e fila
(`docs/ESTRATEGIA_LINKEDIN_PME.md`) e voz (skill `voz-leticia`, adaptada em [escrita.md](referencias/escrita.md)).
Esta skill melhora cada post: pilares, cadência e funil continuam os da estratégia até 31/01/2027. Mudança neles só
com pedido da Jessica. Método adaptado do Hat Tip LinkedIn OS (licença MIT).

Identifique o caminho e siga só ele:

| Pedido | Caminho |
| --- | --- |
| Escrever um post | **Escrever**, abaixo |
| Revisar um post ou a fila | **Revisar**, abaixo |
| Colher pautas com a Dra. | [entrevista-semanal.md](referencias/entrevista-semanal.md) |
| Notícia, decisão ou lei recente | [noticia-e-gatilhos.md](referencias/noticia-e-gatilhos.md) |
| Ver o que funcionou | [desempenho.md](referencias/desempenho.md) |

## Escrever

1. **Fonte.** Junte a fonte primária de cada fato jurídico (lei, tribunal, órgão) e o relato da Dra., se houver.
   Concluído quando cada afirmação do post tem origem; o que faltar fica marcado `[CONFIRMAR]`, nunca preenchido.
2. **Plano CPIO**, mostrado antes do texto:
   - **Convey:** a única ideia, em uma frase, e o que o leitor faz depois de ler.
   - **Package:** o formato (ver [formatos.md](referencias/formatos.md)), o ângulo e o que o gancho promete e segura.
   - **Information:** os fatos que entram, o que fica de fora e o que falta.
   - **Order:** gancho, contexto, desenvolvimento, prova, fechamento. O fechamento conclui a ideia, sem resumo forçado.
3. **Texto** conforme [escrita.md](referencias/escrita.md).
4. **Conferência:** rode `python .claude/skills/leticia-linkedin/conferir_post.py ARQUIVO`, na raiz do repositório.
   Concluído quando nada bloqueia e cada aviso de atenção foi resolvido ou justificado.
5. **Entrega:** rascunho em `producao/linkedin/`, com o plano e as pendências. Quem aprova é a Jessica ou a Dra.
   Peça pronta nunca é sobrescrita: versão nova é arquivo novo.

## Revisar

Revisão só aponta: alterar a fila no Orbit exige ok da Jessica.

1. **Conferência automática:** rode `conferir_post.py` no post ou na faixa de datas
   (`producao/linkedin/posts-*.json --de AAAA-MM-DD --ate AAAA-MM-DD`). Os JSON são a versão aprovada em 23/10; o texto
   vigente é o da tela `/linkedin` do Orbit, e a Jessica pode ter editado lá. Diga qual versão você leu.
2. **Fatos:** confira na fonte cada lei, tese, prazo e data, inclusive datas relativas contra a data de publicação.
3. **Link:** abra o link do post. Confirme que está no ar e que fala com o mesmo leitor do post (empresa, não
   trabalhador). Post com link fora do ar fica parado na fila.
4. **Julgamento**, primeiro a ideia e depois as frases:
   - O leitor é dono de PME, RH ou contador e sai sabendo o que fazer?
   - O gancho faz uma promessa específica que o post cumpre, e dá para entender sem contexto?
   - Dá para distinguir este post de um resumo da lei? A observação própria da Dra. está lá, ou falta?
5. **Veredito** de cada post, com até 3 motivos, os de maior impacto, e a correção sugerida em texto pronto:
   - **APROVADO:** pode sair, no máximo com retoque.
   - **AJUSTAR:** ideia boa, execução ou fato a corrigir.
   - **REPENSAR:** ideia fraca ou formato errado; ajuste de frase não resolve.

Concluído quando todo post da faixa tem veredito e cada fato jurídico está conferido ou marcado como não conferido.

## Limites do canal

- O Orbit publica só no perfil pessoal, texto com ou sem card de link. Post com imagem própria ou documento, publicação
  na página da empresa e números de post ainda não existem (dependem de código ou da Community Management API).
- Comentar, aceitar conexões e responder são da Dra. O LinkedIn proíbe automatizar essa rotina.
- Agent Reach no LinkedIn só lê vagas públicas. Referências de post vêm de link que a Jessica mandar.
