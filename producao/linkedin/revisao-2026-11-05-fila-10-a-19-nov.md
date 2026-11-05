# Revisão dos posts do LinkedIn de 10/11 a 19/11/2026

Primeiro teste da skill `leticia-linkedin`. **Nada foi alterado na fila.** Os textos sugeridos, com só os trechos abaixo
mudados, estão em `revisao-2026-11-05-textos-sugeridos.json`.

Versão lida: arquivos aprovados em 23/10 (`posts-*.json`). A fila do Orbit não foi aberta: se algum post foi editado lá,
compare antes de trocar.

## Resumo

| Data | Tema | Veredito | O que resolver |
| --- | --- | --- | --- |
| 10/11 | 13º salário | **AJUSTAR (fato)** | Na prática, o prazo de 2026 é 18/12, não 20/12 |
| 11/11 | TST, Tema 27 | **AJUSTAR (fato)** | "Deste mês" está errado: o julgamento foi em setembro |
| 12/11 | Checklist 2027 | **AJUSTAR (parado)** | A LP e o PDF estão fora do ar; sem eles o post não sai |
| 17/11 | Multa do art. 477 | **AJUSTAR (leve)** | O artigo do link fala com o trabalhador |
| 18/11 | Atestado médico | **AJUSTAR (leve)** | "Toda semana" sem confirmação; artigo fala com o trabalhador |
| 19/11 | Consciência Negra | **AJUSTAR** | O artigo do link fala com o trabalhador |

## Post a post

### 10/11, 13º salário
- **Fato:** 20/12/2026 é domingo. O próprio `docs/PLANO_CONTEUDO_DEZ_2026.md` já trata o prazo como 18/12. O post diz 20/12
  e ainda alerta para "não deixar para o último dia".
- **Ganho:** a correção rende um gancho melhor: "13º salário: em 2026, a 2ª parcela precisa sair até 18/12, não 20/12."
- **Experiência:** "os erros que mais vejo" afirma vivência da Dra. O texto sugerido usa "erros comuns". Se ela confirmar,
  a frase original pode voltar, porque é mais forte.

### 11/11, TST, Tema 27
- **Fato:** o post diz "uma decisão do TST deste mês", mas sai em novembro e o Pleno julgou em 28/09/2026, segundo a
  [Conjur](https://conjur.com.br/2026-set-29/sindicato-pode-defender-um-unico-trabalhador-em-todas-as-fases-do-processo/).
  O texto sugerido usa "decisão recente" e "julgado em setembro de 2026".
- **Falta conferir:** a data veio de notícias; o acórdão do TST não foi lido.

### 12/11, Checklist 2027
- **Bloqueio:** em 05/11, `lp/empresas-adequacao-trabalhista-2026.html` e `assets/downloads/checklist-2027-empresas.pdf`
  responderam 404 no site. O Orbit segura o post até o link estar no ar, então ele atrasa sem aviso público.
- **Decisão:** aprovar e subir a LP até 11/11, ou mudar a data do post. Os outros posts com essa LP (01/12, 07/01 e 14/01)
  dependem da mesma decisão.
- **Texto:** "tudo o que muda" virou "as principais mudanças", porque um checklist não esgota o assunto.

### 17/11, Multa do art. 477
- **Melhor post do grupo:** gancho específico, prazo claro e rotina no fechamento. Só "onde as empresas mais erram" vira
  "onde costuma dar errado", porque não temos dado de frequência.
- **Link:** o artigo fala de "quem tem direito" e "como provar", para o trabalhador. O post fala com a empresa.

### 18/11, Atestado médico
- **Texto:** "chegam toda semana ao RH" não tem fonte; virou "dúvidas comuns no RH".
- **Link:** o artigo fala em "seus direitos" e cita o "caso dos supermercados no ES". Confirme que esse caso é público e não
  é da Dra. antes de divulgar (manual, seção 1).

### 19/11, Consciência Negra
- **Link:** o artigo se chama "como provar e quais são seus direitos" e abre com "Sofreu racismo?". Num post para empresas,
  ele desvia o leitor. O texto sugerido sai sem link e sem a última frase.
- **Alternativa:** escrever um artigo para empresas e manter o link.

## O que aparece em todos

- **Artigos para o público errado:** três dos seis posts mandam a empresa para texto escrito para o trabalhador. Isso quebra o
  funil da estratégia (post, artigo, LP, checklist). Uma solução é um bloco "Para empresas" no fim desses artigos, levando
  à LP. Exige pedido, porque mexe no site.
- **Falta a voz própria da Dra.:** os posts estão corretos e úteis, mas parecem resumos bem feitos. Uma observação real dela
  é o que os diferenciaria. A entrevista semanal da skill serve para isso.
- **Fórmula repetida:** quase todos têm gancho, regra, lista numerada e fechamento. Vale variar com os formatos da skill em
  janeiro, sem mudar pilares nem cadência.

## O que foi conferido

| Item | Situação |
| --- | --- |
| Verificador `conferir_post.py` | Textos sugeridos sem bloqueio. Único aviso: "Amanhã" de 19/11, correto (véspera do feriado) |
| Tema 27: tese e data | Notícias conferidas; acórdão **não lido** |
| 13º: 18/12 em 2026 | Notícias e plano interno; é leitura do calendário, sem texto oficial |
| Art. 473, XI, da CLT | Texto reproduzido em fonte secundária |
| Links do site | Abertos em 05/11 |
| Art. 477 da CLT, Resolução CFM 1.658/2002, Lei 14.457/2022 e demais citações | **Não conferidos na fonte oficial.** Precisam da leitura da Dra. |
| Post de 05/11 | Fora da revisão: já estava programado para hoje, às 8h, e o status não foi conferido |
