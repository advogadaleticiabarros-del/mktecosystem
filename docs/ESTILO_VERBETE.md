# Estilo Verbete

Estilo visual aprovado pela Jessica em 04/11/2026 ("Agora esse, gostei também", na sequência de "salve esse como mais um estilo nosso"). É mais um estilo da marca e não substitui os outros. Nenhuma peça foi publicada ainda, e a Dra. Letícia ainda não avaliou o estilo.

**A ideia:** a peça imita uma página de dicionário, com termo, separação de sílabas, definição numerada, exemplo de uso e figura com legenda. O formato inesperado ajuda a fixar uma definição, como "Letícia Barros: a advogada da mulher que trabalha".

- Código: `producao/estilos/verbete/gerar.py`, com a função `verbete(...)`. Usa `base.py` de `producao/estilos/palavra-de-ouro/`.
- Peça de referência: `producao/estilos/verbete/pecas/01-leticia-barros.jpg`. Fica só no computador da Jessica, porque o git ignora JPG em `producao/`. O `gerar.py` a recria.

## Regras visuais

| Item | Valor |
| --- | --- |
| Formato | 1080×1440 |
| Fundo | Papel `#EFE6D9`, fosco, com grão e fibra muito leves |
| Termo | EB Garamond 500, 128 px |
| Sílabas e classe | EB Garamond itálico 400, 42 px |
| Definição 1 | EB Garamond 500, 80 px, numerada |
| Definição 2 | Inter 400, 32 px, número em 600 |
| Exemplo | EB Garamond itálico 400, 42 px, começando com "Ex.:" |
| Figura | 344 px de largura, à direita, sem véu nem filtro, com legenda "Fig. 1." em Inter, 24 px |
| Ouro | Fios com o gradiente `FIO` de `gerar.py` e faixas de topo e rodapé com brilho. Sem letra dourada, porque o fundo é claro |
| Margens | 96 px nas laterais |
| Cabeçalho | Fio duplo, chapéu "Dicionário" e a letra inicial do termo à direita |
| Assinatura | Logo, Letícia Barros · OAB/ES 39.948 |

## Como usar

- **Serve para:** o nome da Dra. e termos que o público usa sem entender, como "justa causa", "estabilidade" ou "alimentos gravídicos" (exemplos ainda não produzidos).
- **Definição curta:** cabe em até 3 linhas no tamanho de 80 px.
- **Foto da Dra.:** sempre original, sem filtro, grão nem alteração de cor. Foto de banco só em verbete de termo, nunca em verbete do nome dela.
- **Termo jurídico:** sempre cite a lei no item 2 ou no exemplo, em tese, sem caso real.

## Antes de publicar

- **Frase do nome:** "a advogada da mulher que trabalha" ainda é proposta, e a decisão é da Jessica com a Dra.
- **OAB:** o verbete do nome destaca a própria advogada. Confirme com a OAB-ES se ele fica informativo e não soa como promoção pessoal (Provimento 205/2021). A definição não pode usar superlativo nem "especialista" sem título.
- **Exemplo e legenda:** "Foi a Letícia Barros que explicou o art. 391" e "Em atividade" são textos propostos, sem revisão da Dra.
- **Retrato:** o da peça de referência parece feito com IA. O manual aceita, mas um retrato do ensaio real é preferível.
- **Art. 391:** o exemplo cita a lei, e a Dra. precisa conferir.
- **Grade:** a peça é clara e combina com as peças escuras do estilo [Palavra de Ouro](ESTILO_PALAVRA_DE_OURO.md).
