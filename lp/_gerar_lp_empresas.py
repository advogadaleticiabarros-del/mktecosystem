"""Gera lp/empresas-adequacao-trabalhista-2026.html a partir do design da LP assessoria-empresarial (15/10/2026).

Página para empresas: assessoria trabalhista e previdenciária preventiva com o calendário de mudanças 2026-2027
(fim da 6x1, NR-1, Lei 15.377, licença-paternidade, Tema 215 do TST, Tema 1.389 do STF).
Uso: py lp/_gerar_lp_empresas.py <assessoria-empresarial.html baixada do site>
"""
import json
import sys
from pathlib import Path

B = "https://advogadaleticiabarros.com.br/blog/"
URL = "https://advogadaleticiabarros.com.br/lp/empresas-adequacao-trabalhista-2026.html"

EXTRA_CSS = """
    .linha{margin-top:28px;position:relative;padding-left:26px;border-left:2px solid rgba(201,169,98,.35)}
    .marco{position:relative;margin-bottom:18px;background:var(--fundo-alt);border:1px solid rgba(201,169,98,.14);border-radius:var(--r-sm);padding:14px 18px}
    .marco::before{content:'';position:absolute;left:-34px;top:20px;width:12px;height:12px;border-radius:50%;background:var(--grad);box-shadow:0 0 0 4px var(--fundo-escuro)}
    .marco .q{font-size:11px;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;color:var(--dourado)}
    .marco h3{font-size:15.5px;color:var(--branco);margin:4px 0 4px}
    .marco p{font-size:14px;font-weight:300;opacity:.85}
    .leia{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px;margin-top:24px}
    .leia a{display:block;background:var(--fundo-alt);border:1px solid rgba(201,169,98,.14);border-radius:var(--r-sm);padding:16px 18px;color:var(--branco);text-decoration:none;font-size:14.5px;transition:var(--tr)}
    .leia a:hover{border-color:var(--dourado)}
    .leia a span{display:block;font-size:11px;letter-spacing:1.5px;text-transform:uppercase;color:var(--dourado);margin-bottom:6px}
  </style>"""

FAQ = [
    ("A escala 6x1 já acabou?", "Ainda não. A PEC 221/2019 foi aprovada pelo Senado em 14/10/2026 e segue para promulgação. Depois da publicação, a empresa tem dois meses para garantir dois dias de descanso semanal e jornada de até 42 horas, e mais um ano para chegar a 40 horas, sem redução de salário."),
    ("Minha empresa é pequena. Muda alguma coisa?", "O texto aprovado prevê que uma lei complementar defina regras de transição para MEI, microempresas e empresas de pequeno porte, condicionadas à manutenção dos empregos. Até lá, vale a regra geral, e o planejamento das escalas já pode começar."),
    ("A NR-1 sobre saúde mental foi suspensa?", "Não. Desde 26/05/2026 os riscos psicossociais devem constar no Programa de Gerenciamento de Riscos. O STF suspendeu temporariamente as multas ligadas a esses itens (ADPF 1.316), mas a obrigação de gerenciar os riscos continua."),
    ("Posso contratar prestadores como PJ?", "O STF ainda vai decidir os limites no Tema 1.389. Enquanto isso, a Justiça analisa a realidade do trabalho: com pessoalidade, habitualidade, pagamento e subordinação, há risco de reconhecimento de vínculo de emprego."),
    ("O atendimento é só em Vitória?", "O escritório fica em Vitória-ES e atende empresas de toda a Grande Vitória e do interior do Espírito Santo, com reuniões online ou presenciais."),
    ("Quanto custa a assessoria?", "Os honorários são apresentados em proposta individual, conforme o porte e a demanda da empresa, observada a tabela da OAB/ES."),
]

MARCOS = [
    ("Desde 06/04/2026", "Lei 15.377/2026: dever de informação em saúde", "A empresa deve divulgar campanhas de vacinação e de prevenção do HPV e dos cânceres de mama, colo do útero e próstata, e avisar os empregados do direito de faltar para exames preventivos sem desconto (CLT, arts. 169-A e 473)."),
    ("Desde 26/05/2026", "NR-1: riscos psicossociais no PGR", "Sobrecarga, metas abusivas e assédio entram no gerenciamento de riscos. As multas desses itens estão suspensas pelo STF (ADPF 1.316) até o fim de 2026, mas a obrigação continua."),
    ("Desde 19/08/2026", "TST, Tema 215: ação no domicílio do trabalhador", "Em casos excepcionais, a reclamação pode correr onde o empregado mora, mesmo contra empresa pequena. Documentos digitais e audiências por meio eletrônico ganham peso."),
    ("Promulgação + 2 meses", "Fim da 6x1: dois dias de descanso e até 42 horas", "Aprovada pelo Senado em 14/10/2026 (PEC 221/2019). Sem redução de salário. Cláusulas coletivas incompatíveis perdem a validade."),
    ("01/01/2027", "Licença-paternidade de 10 dias e salário-paternidade", "Lei 15.371/2026: a empresa paga e é reembolsada pelo INSS; o pai tem estabilidade até um mês depois da licença. 15 dias em 2028 e 20 em 2029."),
    ("1 ano depois da 1ª etapa", "Jornada máxima de 40 horas semanais", "Segunda etapa da PEC 221/2019, cerca de 14 meses depois da publicação da emenda."),
    ("Sem data", "STF, Tema 1.389: pejotização", "O Supremo vai decidir a licitude dos contratos PJ, a competência e o ônus da prova. As Varas e os TRTs voltaram a julgar desde junho de 2026."),
]

CHECKS = ["Empregados em escala 6x1", "Jornada acima de 42 horas semanais", "Riscos psicossociais fora do PGR",
          "Prestadores PJ com rotina de empregado", "Sem política para a licença-paternidade de 2027",
          "Afastamentos pelo INSS sem acompanhamento", "Já recebi reclamação trabalhista ou fiscalização"]

SERVICOS = [
    ("Jornada e escalas", "diagnóstico das escalas atuais, plano de transição da 6x1 para a 5x2, banco de horas e controle de ponto."),
    ("Contratos e terceirização", "revisão de contratos PJ, autônomos e terceirizados à luz da CLT e do Tema 1.389."),
    ("Saúde e segurança", "apoio jurídico à adequação da NR-1 e às novas obrigações de informação, junto com a equipe de SST da empresa."),
    ("Políticas de RH", "licença-paternidade, exames preventivos, prevenção ao assédio e regras de conduta."),
    ("Previdenciário da empresa", "afastamentos e retornos pelo INSS, salário-maternidade e salário-paternidade."),
    ("Treinamento de lideranças", "o que muda na prática para quem faz escala, cobra meta e demite."),
    ("Defesa", "atuação em reclamações trabalhistas e fiscalizações já em curso."),
]

LEIA = [
    ("Jornada", "fim-da-escala-6x1-o-que-muda-e-quando-comeca", "Fim da escala 6x1: o que muda e quando começa"),
    ("Saúde no trabalho", "saude-no-trabalho-2026-lei-15377-nr-1", "Lei 15.377 e a nova NR-1"),
    ("2027", "licenca-paternidade-10-dias-2027-lei-15371", "Licença-paternidade de 10 dias e salário-paternidade"),
    ("Contratos", "pejotizacao-stf-tema-1389-o-que-fazer", "Pejotização no STF: o que está em jogo"),
    ("Processo", "acao-trabalhista-na-cidade-onde-moro-tst-tema-215", "Ação no domicílio do trabalhador (TST)"),
]


def gerar(base: str) -> str:
    css = base[base.index("<style>"):base.index("</style>") + 8].replace("  </style>", EXTRA_CSS)
    cauda = base[base.index('  <a class="wa-float"'):]
    cauda = (cauda.replace("[LP-v3 assessoria-empresarial]", "[LP empresas-adequacao-2026]")
             .replace("Confirme a ciência de que a advogada entrará em contato para enviar.",
                      "Confirme a ciência de que o escritório entrará em contato para enviar.")
             .replace("btn.textContent = 'Enviar para análise';", "btn.textContent = 'Solicitar contato';"))
    schema = {"@context": "https://schema.org", "@graph": [
        {"@type": "LegalService", "name": "Letícia Barros Advocacia", "url": URL, "areaServed": "Espírito Santo",
         "address": {"@type": "PostalAddress", "addressLocality": "Vitória", "addressRegion": "ES", "addressCountry": "BR"},
         "knowsAbout": ["Direito do Trabalho", "Direito Previdenciário", "Assessoria jurídica preventiva para empresas", "NR-1", "Jornada de trabalho"]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}]}
    marcos = "\n".join(f'      <div class="marco"><div class="q">{q}</div><h3>{h}</h3><p>{p}</p></div>' for q, h, p in MARCOS)
    checks = "\n".join(f'      <div class="chk" data-txt="{c}"><span class="bx"></span>{c}</div>' for c in CHECKS)
    servicos = "\n".join(f"      <div><strong>{t}</strong>: {d}</div>" for t, d in SERVICOS)
    leia = "\n".join(f'      <a href="{B}{s}.html"><span>{k}</span>{t}</a>' for k, s, t in LEIA)
    faq = "\n".join(f"      <details><summary>{q}</summary><p>{a}</p></details>" for q, a in FAQ)
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Advocacia trabalhista para empresas em Vitória-ES | Adequação 2026-2027 | Letícia Barros</title>
  <meta name="description" content="Fim da escala 6x1, NR-1, licença-paternidade de 2027 e contratos PJ: assessoria trabalhista e previdenciária preventiva para empresas do Espírito Santo.">
  <link rel="canonical" href="{URL}">
  <meta property="og:title" content="Sua empresa pronta para o fim da 6x1 e para as regras trabalhistas de 2026 e 2027">
  <meta property="og:description" content="Assessoria trabalhista e previdenciária preventiva para empresas do Espírito Santo.">
  <meta property="og:image" content="https://advogadaleticiabarros.com.br/assets/images/lp/lp-assessoria.jpg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400&family=Inter:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&display=swap" rel="stylesheet">
  <script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>
  {css}
</head>
<body>
  <div class="topo">
    <a class="marca" href="https://www.advogadaleticiabarros.com.br" style="display:flex;align-items:center;gap:10px">
      <img src="../assets/logo/logo-sem-fundo.png" alt="Letícia Barros Advocacia" style="height:40px;width:auto">Letícia Barros
    </a>
    <a class="mini" href="#form">Solicitar contato</a>
  </div>

  <div class="hero">
    <div class="bg" role="img" aria-label="Assessoria trabalhista e previdenciária para empresas"></div>
    <div class="veu"></div>
    <div class="inner">
      <h1>Sua empresa pronta para o fim da 6x1 <em>e para as regras trabalhistas de 2026 e 2027</em></h1>
      <p class="sub">Jornada e escalas, NR-1 e saúde mental, licença-paternidade, contratos PJ e afastamentos pelo INSS. Assessoria trabalhista e previdenciária preventiva para empresas do Espírito Santo, com orientação clara e sem juridiquês.</p>
      <a class="cta-hero" href="#calendario">Ver o calendário de mudanças</a>
      <div class="selo"><span>OAB/ES 39.948</span><span>Vitória e todo o ES</span><span>Online ou presencial</span></div>
    </div>
  </div>

  <div class="form-sec">
    <div class="card" id="form">
      <h2>Fale com o escritório</h2>
      <p class="fs">Deixe o contato da empresa. O escritório retorna para entender a demanda.</p>
      <form id="lead-form" novalidate>
        <label for="f-name">Seu nome completo *</label>
        <input id="f-name" name="name" required autocomplete="name" placeholder="Nome e cargo na empresa">
        <label for="f-phone">WhatsApp *</label>
        <input id="f-phone" name="phone" required inputmode="tel" autocomplete="tel" placeholder="(27) 90000-0000">
        <label for="f-qualif">Quantos empregados a empresa tem?</label>
        <select name="qualif" id="f-qualif">
          <option value="">Selecione</option>
          <option value="1 a 9 empregados">1 a 9</option>
          <option value="10 a 49 empregados">10 a 49</option>
          <option value="50 a 199 empregados">50 a 199</option>
          <option value="200 ou mais empregados">200 ou mais</option>
        </select>
        <label for="f-msg">Qual é a demanda?</label>
        <textarea name="message" id="f-msg" placeholder="Ex.: adequar as escalas ao fim da 6x1, revisar contratos PJ, NR-1."></textarea>
        <input class="hp" type="text" name="website" tabindex="-1" autocomplete="off">
        <label style="display:flex;gap:10px;align-items:flex-start;text-transform:none;letter-spacing:0;font-weight:400;font-size:13px;color:var(--areia);cursor:pointer;margin-top:20px">
          <input type="checkbox" id="f-ciente" required style="width:auto;margin-top:3px">
          <span>Estou ciente de que, ao enviar este formulário, <strong style="color:var(--dourado-light)">o escritório entrará em contato</strong> para entender a demanda da empresa.</span>
        </label>
        <button type="submit" class="enviar" id="f-btn">Solicitar contato</button>
        <div class="err" id="f-err"></div>
        <p class="nota">Dados usados apenas para o retorno do contato (LGPD).</p>
      </form>
      <div class="ok" id="f-ok">
        <div class="ck">✓</div>
        <h3>Recebemos o seu contato!</h3>
        <p>O escritório da Dra. Letícia Barros vai retornar pelo WhatsApp informado.</p>
      </div>
    </div>
  </div>

  <section id="calendario">
    <h2>O calendário trabalhista que já começou</h2>
    <div class="linha">
{marcos}
    </div>
  </section>

  <section>
    <h2>Identifique o que acontece na sua empresa hoje</h2>
    <div class="checks">
{checks}
    </div>
    <p class="aviso-chk" id="aviso-chk">Os itens marcados foram adicionados ao formulário. <a href="#form">Solicitar contato ↑</a></p>
  </section>

  <section>
    <div class="oque">
      <div class="oque-foto"><img src="../assets/images/leticia-estudiosa-removebg-preview.png" alt="Dra. Letícia Barros"></div>
      <div class="oque-txt">
        <h2>Prevenção trabalhista e previdenciária</h2>
        <p>É ter uma advogada acompanhando as decisões da empresa antes que elas virem processo: escalas que respeitam a lei nova, contratos que refletem a realidade do trabalho, afastamentos pelo INSS bem conduzidos e lideranças que sabem o que podem e o que não podem fazer. A empresa decide com segurança, e o passivo não se acumula em silêncio.</p>
      </div>
    </div>
  </section>

  <section>
    <h2>O que a assessoria contempla</h2>
    <div class="lei">
{servicos}
    </div>
  </section>

  <section>
    <h2>Leia antes de decidir</h2>
    <div class="leia">
{leia}
    </div>
  </section>

  <section>
    <h2>Como funciona o atendimento</h2>
    <div class="passos">
      <div class="passo"><div class="n">1</div><h3>Contato</h3><p>Pelo formulário ou WhatsApp, no seu tempo.</p></div>
      <div class="passo"><div class="n">2</div><h3>Diagnóstico</h3><p>Levantamento de escalas, contratos e rotinas de RH.</p></div>
      <div class="passo"><div class="n">3</div><h3>Plano de adequação</h3><p>Prioridades, prazos e documentos, com acompanhamento.</p></div>
    </div>
    <div class="sobre">
      <div class="foto"><img src="../assets/images/leticia-sorrindo_2-removebg-preview.png" alt="Dra. Letícia Barros"></div>
      <div>
        <h3>Dra. Letícia Barros</h3>
        <p>Advogada inscrita na OAB/ES 39.948, com escritório em Vitória-ES e atuação em Direito do Trabalho e Previdenciário. Atende empresas em toda a Grande Vitória (Vila Velha, Serra, Cariacica, Viana e Guarapari) e no interior do Espírito Santo, explicando cada etapa com informação clara, sem juridiquês.</p>
      </div>
    </div>
  </section>

  <section>
    <h2>Perguntas frequentes</h2>
    <div style="margin-top:22px">
{faq}
    </div>
  </section>

  <div class="final">
    <p>As mudanças têm data. Planejar agora custa menos do que corrigir depois.</p>
    <a class="btn-final" href="#form">Solicitar contato do escritório</a>
  </div>

{cauda}"""


if __name__ == "__main__":
    html = gerar(Path(sys.argv[1]).read_text(encoding="utf-8"))
    destino = Path(__file__).resolve().parent / "empresas-adequacao-trabalhista-2026.html"
    destino.write_text(html, encoding="utf-8")
    print(len(html), "bytes ->", destino.name)
    for w in ["especialista", "gratuit", "sem compromisso", "envie o seu caso", "análise"]:
        print(w, html.lower().count(w))
