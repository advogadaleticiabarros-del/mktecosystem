"""Comparação com o 1º resultado do Google (28/10/2026, docs/SEO_PLANO_GOOGLE_IA.md): gera
2026-10-28-trocas-site.json para apps/api/scripts/aplicar_trocas_site.py.

- Licença-maternidade 180 dias (1.336 aparições, posição 8,7): quem lidera a busca responde "como conseguir"
  (passo a passo, prazo, quem paga, tabela por situação); o nosso artigo era notícia do STF. Entram essas seções,
  uma pergunta frequente (no texto e nos dados estruturados) e leituras do mesmo assunto no lugar de pet no
  divórcio, violência de gênero e Pix da pensão.
- Banheiro (2.583 aparições, posição 5,7): os resultados de cima são notícias de tribunal e fórum. Entra
  "O que a Justiça já decidiu" com duas decisões públicas (TRT-SC 2016, garçom; TRT-MG 2023, atendente de
  fast-food), sem valores.

Fatos: Lei 11.770/2008, art. 1º, § 1º (pedido até o fim do 1º mês após o parto; começa logo após os 120 dias),
art. 3º (remuneração integral), art. 4º (sem outro trabalho remunerado e sem creche), art. 5º (dedução do IR no
lucro real); Decreto 6.690/2008 (servidora federal). Notícias: portal.trt12.jus.br (18/05/2016) e O Tempo
(20/07/2023, 1ª Turma do TRT-MG).

Uso: py producao/seo/2026-10-28-trocas-site.py <pasta com as páginas no ar>
"""
import json
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
HOJE_ISO, HOJE = "2026-10-28", "28 de outubro de 2026"
LIC = "blog/stf-licenca-maternidade-180-dias-o-que-mudou-de-verdade.html"

PAGINAS = {
    LIC: [
        {"de": "<p>Não sabe se a sua empresa é do Empresa Cidadã? Pergunte ao RH antes do parto: o pedido tem prazo.</p>",
         "para": """<p>Não sabe se a sua empresa é do Empresa Cidadã? Pergunte ao RH antes do parto: o pedido tem prazo.</p>

<h2>120 ou 180 dias: quem tem cada um</h2>

<table class="prova-table">
<tr><th>Situação</th><th>Licença</th></tr>
<tr><td>CLT em empresa que não participa do Empresa Cidadã</td><td>120 dias</td></tr>
<tr><td>CLT em empresa do Empresa Cidadã, com pedido no prazo</td><td>180 dias</td></tr>
<tr><td>Servidora pública federal</td><td>180 dias</td></tr>
<tr><td>Servidora estadual ou municipal</td><td>Depende da lei do seu órgão</td></tr>
<tr><td>MEI, autônoma ou desempregada (salário-maternidade pelo INSS)</td><td>120 dias</td></tr>
<tr><td>Mãe adotante</td><td>O mesmo período da mãe biológica em cada caso</td></tr>
</table>

<h2>Como pedir a licença-maternidade de 180 dias (passo a passo)</h2>

<ol>
<li><strong>Confirme com o RH, ainda na gravidez,</strong> se a empresa participa do Programa Empresa Cidadã, e peça a resposta por escrito. Não há uma lista pública simples para consultar: quem informa é a própria empresa.</li>
<li><strong>Faça o pedido por escrito</strong>, por e-mail ou carta com protocolo, dizendo que quer a prorrogação de 60 dias da Lei 11.770/2008.</li>
<li><strong>Respeite o prazo:</strong> o pedido precisa ser feito <strong>até o fim do primeiro mês depois do parto</strong> (Lei 11.770/2008, art. 1º, § 1º). Dá para pedir antes, ainda grávida.</li>
<li><strong>Guarde o comprovante</strong> do pedido e a resposta da empresa.</li>
<li>A prorrogação começa <strong>logo depois dos 120 dias</strong>, sem intervalo.</li>
</ol>

<div class="callout-box">
<h4>Ponto decisivo</h4>
<p>Perdeu o prazo de um mês depois do parto, a empresa pode negar os 60 dias, mesmo participando do programa. E durante a prorrogação você não pode trabalhar em outro lugar, e o bebê não pode ir para a creche, sob pena de perder o direito (Lei 11.770/2008, art. 4º).</p>
</div>

<h2>Quem paga os 60 dias a mais</h2>

<p>Os 120 dias são o salário-maternidade: para quem tem carteira assinada, a empresa paga junto com o salário e depois compensa com o INSS. Os <strong>60 dias da prorrogação são pagos pela empresa</strong>, com salário integral (art. 3º), e ela pode abater esse valor do imposto de renda, se for tributada pelo lucro real (art. 5º). Por isso o benefício depende da adesão da empresa ao programa.</p>

<p>Para ver todos os direitos da gravidez à volta ao trabalho, leia o <a href="direitos-da-gestante-clt-guia-completo.html">guia completo dos direitos da gestante CLT</a>.</p>"""},
        {"de": "<h3>Casais podem dividir a licença entre si livremente agora?</h3>",
         "para": "<h3>Até quando posso pedir os 180 dias?</h3>\n<p>Até o fim do primeiro mês depois do parto, por escrito, se a empresa participar do Programa Empresa Cidadã (Lei 11.770/2008, art. 1º, § 1º).</p>\n\n<h3>Casais podem dividir a licença entre si livremente agora?</h3>"},
        {"de": '    {"@type": "Question", "name": "Quem tem direito a 180 dias de licença-maternidade?"',
         "para": '    {"@type": "Question", "name": "Até quando posso pedir os 180 dias de licença-maternidade?", "acceptedAnswer": {"@type": "Answer", "text": "Até o fim do primeiro mês depois do parto, por escrito, se a empresa participar do Programa Empresa Cidadã (Lei 11.770/2008, art. 1º, § 1º)."}},\n'
                 '    {"@type": "Question", "name": "Quem tem direito a 180 dias de licença-maternidade?"'},
        {"de": '<a href="guarda-compartilhada-de-pet-como-funciona-a-lei-no-divorcio.html" class="related-card">\n                <span class="cat">Família</span>\n                <h4>Guarda compartilhada de pet: como funciona a nova lei no divórcio</h4>',
         "para": '<a href="direitos-da-gestante-clt-guia-completo.html" class="related-card">\n                <span class="cat">Trabalhista</span>\n                <h4>Direitos da gestante CLT: o guia completo de 2026</h4>'},
        {"de": '<a href="violencia-de-genero-fora-de-casa-o-que-mudou-com-o-stf.html" class="related-card">\n                <span class="cat">Família</span>\n                <h4>Violência de gênero fora de casa: o que mudou com o STF</h4>',
         "para": '<a href="licenca-maternidade-mae-adotante-mesmos-direitos-stf.html" class="related-card">\n                <span class="cat">Trabalhista</span>\n                <h4>Licença-maternidade da mãe adotante: os mesmos direitos</h4>'},
        {"de": '<a href="pix-pensao-alimenticia-como-funciona-nova-lei-e-quando-comeca-a-valer.html" class="related-card">\n                <span class="cat">Família</span>\n                <h4>Pix Pensão Alimentícia: como funciona a nova lei sancionada e quando ela começa a valer</h4>',
         "para": '<a href="licenca-paternidade-10-dias-2027-lei-15371.html" class="related-card">\n                <span class="cat">Trabalhista</span>\n                <h4>Licença-paternidade de 10 dias em 2027: Lei 15.371/2026</h4>'},
        {"de": "Atualizado em 22 de outubro de 2026", "para": f"Atualizado em {HOJE}"},
        {"de": '"dateModified": "2026-10-22"', "para": f'"dateModified": "{HOJE_ISO}"'},
    ],
    "blog/empresa-pode-obrigar-limpar-banheiro.html": [
        {"de": "<h2>Um exemplo que chega ao escritório</h2>",
         "para": """<h2>O que a Justiça já decidiu</h2>

<p>Dois casos públicos ajudam a entender como os tribunais olham para isso:</p>

<ul>
<li><strong>Garçom que limpava banheiros (TRT de Santa Catarina, 5ª Câmara, 2016):</strong> o tribunal reconheceu o desvio de função, por considerar a limpeza de banheiros incompatível com quem lida com alimentos e louças, e também o adicional de insalubridade em grau máximo.</li>
<li><strong>Atendente de fast-food em Belo Horizonte (TRT de Minas Gerais, 1ª Turma, 2023):</strong> ela atendia, ficava no caixa, ajudava na chapa e limpava em rodízio banheiros usados por centenas de clientes por dia. O tribunal reconheceu o adicional de insalubridade em grau máximo durante todo o contrato, porque essa limpeza não se compara à de uma casa ou de um escritório.</li>
</ul>

<p>São decisões de casos concretos de outros processos: mostram o caminho, mas cada situação depende das provas e da perícia.</p>

<h2>Um exemplo que chega ao escritório</h2>"""},
        {"de": "Atualizado em 27 de outubro de 2026", "para": f"Atualizado em {HOJE}"},
        {"de": '"dateModified": "2026-10-27"', "para": f'"dateModified": "{HOJE_ISO}"'},
    ],
}


def conferir_e_gravar(pasta: Path) -> None:
    saida = {"paginas": []}
    problemas = 0
    for caminho, trocas in PAGINAS.items():
        texto = (pasta / caminho).read_bytes().decode("utf-8-sig")  # sem normalizar as quebras de linha
        crlf = "\r\n" in texto
        prontas = []
        for t in trocas:
            de, para = t["de"], t["para"]
            if crlf:
                de, para = de.replace("\n", "\r\n"), para.replace("\n", "\r\n")
            n = texto.count(de)
            if n == 0 or (n > 1 and not t.get("todas")):
                print(f"{caminho}: {n}x {de[:70]!r}")
                problemas += 1
            prontas.append({"de": de, "para": para, **({"todas": True} if t.get("todas") else {})})
        saida["paginas"].append({"caminho": caminho, "trocas": prontas})
    if problemas:
        sys.exit(f"{problemas} trecho(s) não conferem; JSON não gravado")
    destino = AQUI / "2026-10-28-trocas-site.json"
    destino.write_text(json.dumps(saida, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"ok: {sum(len(p['trocas']) for p in saida['paginas'])} trocas em {len(saida['paginas'])} páginas -> {destino}")


if __name__ == "__main__":
    conferir_e_gravar(Path(sys.argv[1]))
