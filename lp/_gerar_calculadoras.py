"""Gera as páginas das calculadoras de rescisão e de licença-maternidade.

Reaproveita o <style> da calculadora do 13º (lp/calculadora-13-salario.html), para que as três
tenham o mesmo visual. Rodar de novo depois de mudar este arquivo ou o estilo do 13º:

    py lp/_gerar_calculadoras.py

O cálculo fica em lp/js/calculo-rescisao.js e lp/js/calculo-licenca.js (testados com node).
Na prévia local (file://) o formulário de contato não envia nada ao CRM e o Pixel não carrega.
"""
import json
import re
from pathlib import Path

LP = Path(__file__).resolve().parent
SITE = "https://advogadaleticiabarros.com.br"
WA = "5527995151402"

base13 = (LP / "calculadora-13-salario.html").read_text(encoding="utf-8")
ESTILO = re.search(r"<style>(.*?)</style>", base13, re.S).group(1)
ESTILO_EXTRA = """
    .datas{margin-top:6px;list-style:none}
    .datas li{display:flex;justify-content:space-between;align-items:baseline;gap:14px;padding:12px 0;border-bottom:1px dashed var(--linha-forte)}
    .datas li:last-child{border-bottom:0}
    .datas li>span{font-size:14.5px;color:var(--cafe-2)}
    .datas b{font-family:var(--serif);font-size:21px;font-weight:500;white-space:nowrap;font-variant-numeric:lining-nums;text-align:right}
    .datas li.destaque .d{background:linear-gradient(transparent 62%,var(--ouro-claro) 62%);padding:0 2px}
    .datas b small{font-family:var(--sans);font-size:12px;font-weight:400;color:var(--cafe-3);text-align:right}
    #r-prazo{margin-top:14px}
    .datas small{display:block;font-size:12.5px;color:var(--cafe-3)}
    .fgts{margin-top:16px;border:1px solid var(--linha);background:var(--branco);padding:16px 18px}
    .fgts h3{font-family:var(--serif);font-weight:500;font-size:20px;margin-bottom:4px}
    .fgts table{width:100%;border-collapse:collapse;font-size:14.5px;font-variant-numeric:tabular-nums}
    .fgts td{padding:7px 0}.fgts td:last-child{text-align:right}
    .fgts tr.forte td{font-weight:600;border-top:1px dashed var(--linha-forte)}
    .previa{background:#2B231D;color:#E9D9B4;font-size:13px;text-align:center;padding:8px 12px}
    .recibo tr.desc td:last-child{color:var(--erro)}
    .recibo tr.titulo td{font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--cafe-3);padding-top:14px}
"""

ICONE_WA = '<svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2A10 10 0 0 0 2 12a9.9 9.9 0 0 0 1.5 5.3L2 22l4.9-1.4A10 10 0 1 0 12 2m0 1.8a8.2 8.2 0 1 1-4.2 15.3l-.3-.2-2.9.8.8-2.8-.2-.3A8.2 8.2 0 0 1 12 3.8"/></svg>'
ICONE_WA_GRANDE = ICONE_WA.replace('width="18" height="18"', 'width="20" height="20"')

# Captura do contato e envio ao CRM, igual à calculadora do 13º. Cada página define:
#   window.CALC = { tag, area, campanha, montarEntrada(), calcular(entrada), mostrar(resultado, nome), resumo(entrada, resultado), textoWa(resultado) }
SCRIPT_COMUM = r"""
  <script>
    (function () {
      var PREVIA = location.protocol === 'file:';
      var params = new URLSearchParams(window.location.search);
      var UTMS = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'];
      var utmTags = UTMS.map(function (k) { return params.get(k) ? k + '=' + params.get(k) : null; }).filter(Boolean);
      var origem = utmTags.length ? ' [Origem: ' + utmTags.join(', ') + ']' : ' [Origem: direta/sem UTM]';
      var $ = function (id) { return document.getElementById(id); };
      var f1 = $('etapa1'), f2 = $('etapa2'), f3 = $('etapa3');
      var entrada = null, resultado = null, C = window.CALC;
      if (PREVIA) document.body.insertAdjacentHTML('afterbegin', '<div class="previa">Prévia local: o contato não é enviado ao CRM.</div>');

      function etapa(n) {
        [f1, f2, f3].forEach(function (el, i) { el.classList.toggle('oculto', i !== n - 1); });
        ['p1', 'p2', 'p3'].forEach(function (id, i) { $(id).classList.toggle('on', i < n); });
        if (window.innerWidth < 900 || n > 1) $('calcular').scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
      window.CALC_ERRO = function (form, el, msg) { var err = form.querySelector('.err'); if (el) { el.classList.add('campo-erro'); el.focus(); } err.textContent = msg; err.style.display = 'block'; return false; };
      function limpar(form) { form.querySelector('.err').style.display = 'none'; form.querySelectorAll('.campo-erro').forEach(function (el) { el.classList.remove('campo-erro'); }); }

      var bt = $('bt-mais');
      if (bt) bt.addEventListener('click', function () {
        var aberto = this.getAttribute('aria-expanded') === 'true';
        this.setAttribute('aria-expanded', String(!aberto));
        $('mais').classList.toggle('oculto', aberto);
        this.style.borderRadius = aberto ? '' : 'var(--r) var(--r) 0 0';
      });
      if ('IntersectionObserver' in window && window.innerWidth < 900) {
        new IntersectionObserver(function (it) { document.body.classList.toggle('calc-na-tela', it[0].isIntersecting); }).observe($('calcular'));
      }

      f1.addEventListener('submit', function (e) {
        e.preventDefault(); limpar(f1);
        entrada = C.montarEntrada(f1);
        if (!entrada) return;
        resultado = C.calcular(entrada);
        etapa(2);
        $('l-nome').focus({ preventScroll: true });
      });
      $('voltar').addEventListener('click', function () { etapa(1); });
      $('refazer').addEventListener('click', function () { etapa(1); });

      function revelar() {
        var nome = $('l-nome').value.trim().split(' ')[0];
        C.mostrar(resultado, nome, entrada);
        $('r-wa').href = 'https://wa.me/__WA__?text=' + encodeURIComponent(C.textoWa(resultado, entrada));
        etapa(3);
      }

      f2.addEventListener('submit', async function (e) {
        e.preventDefault(); limpar(f2);
        var nomeEl = $('l-nome'), telEl = $('l-tel'), emailEl = $('l-email');
        if (nomeEl.value.trim().length < 3) return CALC_ERRO(f2, nomeEl, 'Informe o seu nome.');
        if (telEl.value.replace(/\D/g, '').length < 10) return CALC_ERRO(f2, telEl, 'Informe um WhatsApp válido, com DDD.');
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(emailEl.value.trim())) return CALC_ERRO(f2, emailEl, 'Informe um e-mail válido.');
        if (!f2.querySelector('[name=ciente]').checked) return CALC_ERRO(f2, null, 'Marque a concordância com o uso dos dados para ver o resultado.');
        if (PREVIA) return revelar();
        var btn = f2.querySelector('button.enviar');
        btn.disabled = true; btn.textContent = 'Enviando…';
        var corpo = {
          name: nomeEl.value.trim(), phone: telEl.value, email: emailEl.value.trim(), area: C.area,
          message: '[LP ' + C.tag + ']' + origem + C.resumo(entrada, resultado),
          landing_page: window.location.href,
          website: f2.querySelector('[name=website]').value
        };
        UTMS.forEach(function (k) { if (params.get(k)) corpo[k] = params.get(k); });
        if (!corpo.utm_campaign) corpo.utm_campaign = C.campanha;
        try {
          var resp = await fetch('https://crm.advogadaleticiabarros.com.br/api/public/lead', {
            method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(corpo)
          });
          if (!resp.ok) throw new Error('Não foi possível enviar agora. Tente de novo em instantes ou chame no WhatsApp.');
          // generate_lead e o pixel "Lead" saem do /js/conversoes.js quando o CRM responde OK.
          revelar();
        } catch (ex) {
          CALC_ERRO(f2, null, ex.message);
        }
        btn.disabled = false; btn.textContent = 'Ver meu resultado';
      });
    })();
  </script>
""".replace("__WA__", WA)

UTIL_JS = r"""
    function reais(v) { return v.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }); }
    function numero(s) { s = String(s || '').replace(/[^\d,.-]/g, ''); if (s.indexOf(',') >= 0) s = s.replace(/\./g, '').replace(',', '.'); return parseFloat(s) || 0; }
    function dataBR(iso, semana) {
      var p = iso.split('-'), d = new Date(Date.UTC(+p[0], +p[1] - 1, +p[2]));
      var txt = p[2] + '/' + p[1] + '/' + p[0];
      return semana ? '<span class="d">' + txt + '</span>' + '<small>' + d.toLocaleDateString('pt-BR', { weekday: 'long', timeZone: 'UTC' }) + '</small>' : txt;
    }
    function $(id) { return document.getElementById(id); }
"""


def bloco_contato():
    return """
      <form id="etapa2" class="oculto" novalidate>
        <h2>Seu cálculo está pronto</h2>
        <p class="fs">Diga para quem é o resultado. Ele aparece aqui na tela assim que você enviar.</p>
        <div class="campo"><label for="l-nome">Nome</label><input id="l-nome" name="name" autocomplete="name" required></div>
        <div class="campo"><label for="l-tel">WhatsApp com DDD</label><input id="l-tel" name="phone" type="tel" inputmode="tel" autocomplete="tel" placeholder="(27) 99999-9999" required></div>
        <div class="campo"><label for="l-email">E-mail</label><input id="l-email" name="email" type="email" autocomplete="email" required></div>
        <input class="hp" type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">
        <label class="check"><input type="checkbox" name="ciente" required><span>Concordo que meus dados sejam usados só para este resultado e para o retorno do escritório. Posso pedir a remoção quando quiser.</span></label>
        <button type="submit" class="enviar">Ver meu resultado</button>
        <div class="err" role="alert"></div>
        <p class="nota">Envio protegido. Seus dados não são compartilhados (LGPD).</p>
        <button type="button" class="voltar" id="voltar">Voltar e corrigir os dados</button>
      </form>"""


def pagina(cfg):
    faq_ld = json.dumps({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in cfg["faq"]],
    }, ensure_ascii=False, indent=1)
    app_ld = json.dumps({
        "@context": "https://schema.org", "@type": "WebApplication", "name": cfg["nome_app"], "url": cfg["url"],
        "description": cfg["descricao_app"], "applicationCategory": "FinanceApplication", "operatingSystem": "Todos (navegador)",
        "inLanguage": "pt-BR", "isAccessibleForFree": True, "datePublished": "2026-11-16", "dateModified": "2026-11-16",
        "provider": {"@type": "LegalService", "name": "Letícia Barros Advocacia & Consultoria", "url": SITE + "/",
                     "areaServed": "BR", "address": {"@type": "PostalAddress", "addressLocality": "Vitória", "addressRegion": "ES", "addressCountry": "BR"}},
    }, ensure_ascii=False, indent=1)
    faq_html = "\n".join(f"      <details><summary>{q}</summary><p>{a}</p></details>" for q, a in cfg["faq"])
    regras_html = "\n".join(f"        <div><dt>{t}</dt><dd>{d}</dd></div>" for t, d in cfg["regras"])
    prazos_html = "\n".join(f"        <div><dt>{t}</dt><dd>{d}</dd></div>" for t, d in cfg["prazos"])
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="theme-color" content="#F7F2EA">
  <title>{cfg['title']}</title>
  <meta name="description" content="{cfg['description']}">
  <link rel="canonical" href="{cfg['url']}">
  <meta property="og:title" content="{cfg['og_title']}">
  <meta property="og:description" content="{cfg['og_description']}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{cfg['url']}">
  <meta property="og:locale" content="pt_BR">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;1,400&family=Inter:wght@400;500&display=swap" rel="stylesheet">
  <script type="application/ld+json">
{app_ld}
  </script>
  <script type="application/ld+json">
{faq_ld}
  </script>
  <script>
  if (location.protocol !== 'file:') {{
    !function(f,b,e,v,n,t,s){{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)}};
    if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
    t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');
    fbq('init', '858690737244687'); fbq('track', 'PageView');
  }}
  </script>
  <style>{ESTILO}{ESTILO_EXTRA}  </style>
</head>
<body>
  <header class="topo"><div class="in">
    <a class="marca" href="{SITE}/">Letícia Barros<small>Advocacia &amp; Consultoria · OAB/ES 39.948</small></a>
    <a class="wa-link" href="https://wa.me/{WA}" target="_blank" rel="noopener">{ICONE_WA}<span>Falar no WhatsApp</span></a>
  </div></header>

  <main class="grade">
    <div class="intro">
      <h1>{cfg['h1']}</h1>
      <p class="sub">{cfg['sub']}</p>
      <dl class="prazos">
{prazos_html}
      </dl>
      <p class="assina">Calculadora preparada pela equipe da <b>Dra. Letícia Barros</b>, advogada trabalhista em Vitória/ES.</p>
    </div>

    <div class="calc" id="calcular">
      <div class="etapas" aria-hidden="true"><span class="on" id="p1">1. Dados</span><span id="p2">2. Contato</span><span id="p3">3. Resultado</span></div>
{cfg['form']}
{bloco_contato()}

      <div id="etapa3" class="oculto" aria-live="polite">
{cfg['resultado']}
        <ul class="obs-lista" id="r-alertas"></ul>
        <a class="cta-wa" id="r-wa" href="https://wa.me/{WA}" target="_blank" rel="noopener">{ICONE_WA_GRANDE}Conferir meu caso com a equipe</a>
        <p class="nota">{cfg['nota']}</p>
        <button type="button" class="voltar" id="refazer">Fazer outro cálculo</button>
      </div>
    </div>
  </main>

  <div class="faixa">
    <section>
      <h2>{cfg['titulo_regras']}</h2>
      <dl class="regras">
{regras_html}
      </dl>
    </section>
  </div>

  <section>
    <h2>Perguntas frequentes</h2>
    <div class="faq">
{faq_html}
    </div>
  </section>

  <footer><div class="in">
    <p>Letícia Barros Advocacia &amp; Consultoria · OAB/ES 39.948 · Vitória/ES</p>
    <p>Ferramenta informativa, que não substitui a análise individual do seu caso (Provimento 205/2021 da OAB). {cfg['rodape']}</p>
    <p>Outras calculadoras: {cfg['outras']}</p>
    <p><a href="{SITE}/politica-privacidade.html">Política de Privacidade</a></p>
  </div></footer>

  <a class="wa-float" href="https://wa.me/{WA}" target="_blank" rel="noopener" aria-label="Falar no WhatsApp">
    {ICONE_WA.replace('width="18" height="18"', 'width="28" height="28" fill="#fff"')}
  </a>

{cfg['scripts']}
  <script>
{UTIL_JS}
{cfg['js']}
  </script>
{SCRIPT_COMUM}
<script src="/js/conversoes.js?v=20261027" defer></script>
</body>
</html>
"""


LINKS = {
    "13": '<a href="calculadora-13-salario.html">13º salário</a>',
    "rescisao": '<a href="calculadora-rescisao.html">rescisão</a>',
    "licenca": '<a href="calculadora-licenca-maternidade.html">licença-maternidade</a>',
}

# ---------------------------------------------------------------- rescisão
RESCISAO = {
    "url": SITE + "/lp/calculadora-rescisao.html",
    "title": "Calculadora de rescisão 2026: quanto você recebe ao sair",
    "description": "Calcule sua rescisão trabalhista: saldo de salário, aviso prévio, 13º e férias proporcionais, multa de 40% do FGTS e descontos de INSS e IR de 2026. Demissão, pedido de demissão, acordo e justa causa.",
    "og_title": "Calculadora de rescisão 2026",
    "og_description": "Veja o que você recebe ao sair da empresa: verbas, FGTS e prazo de pagamento.",
    "nome_app": "Calculadora de rescisão trabalhista 2026",
    "descricao_app": "Estima as verbas rescisórias da CLT: saldo de salário, aviso prévio proporcional, 13º e férias proporcionais com 1/3, férias vencidas, FGTS com multa de 40% ou 20%, descontos de INSS e IR de 2026, para dispensa sem justa causa, pedido de demissão, acordo e justa causa.",
    "h1": "Quanto você recebe na <i>rescisão</i>",
    "sub": "Informe o salário, as datas e como foi a saída. A conta mostra cada verba, os descontos, o FGTS e o prazo para a empresa pagar.",
    "prazos": [
        ("Prazo para pagar", "10 dias<span class=\"obs\">depois do fim do contrato</span>"),
        ("Atraso", "multa de 1 salário"),
        ("Multa do FGTS", "40%<span class=\"obs\">20% no acordo</span>"),
    ],
    "form": """
      <form id="etapa1" novalidate>
        <h2>Calculadora de rescisão</h2>
        <p class="fs">Use os valores do holerite, antes dos descontos.</p>
        <div class="campo">
          <label for="c-salario">Salário bruto por mês</label>
          <div class="moeda"><span>R$</span><input id="c-salario" inputmode="decimal" placeholder="2.500,00" autocomplete="off" required></div>
        </div>
        <div class="campo">
          <label for="c-situacao">Como foi a saída</label>
          <select id="c-situacao">
            <option value="sem_justa_causa">Fui demitido(a) sem justa causa</option>
            <option value="pediu_demissao">Pedi demissão</option>
            <option value="acordo">Saí por acordo com a empresa</option>
            <option value="justa_causa">Fui demitido(a) por justa causa</option>
          </select>
        </div>
        <div class="linha2">
          <div class="campo"><label for="c-admissao">Data de admissão</label><input id="c-admissao" type="date" min="1970-01-01" max="2027-12-31"></div>
          <div class="campo"><label for="c-saida">Último dia de trabalho</label><input id="c-saida" type="date" min="2025-01-01" max="2027-12-31"></div>
        </div>
        <div class="campo" id="bloco-aviso">
          <label for="c-aviso">Aviso prévio</label>
          <select id="c-aviso"></select>
        </div>
        <div class="campo">
          <label for="c-ferias">Férias vencidas que você não tirou</label>
          <select id="c-ferias">
            <option value="0">Nenhuma</option>
            <option value="1">1 período (1 ano)</option>
            <option value="2">2 períodos (2 anos)</option>
          </select>
        </div>
        <button type="button" class="bt-mais" id="bt-mais" aria-expanded="false" aria-controls="mais">
          <svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>
          <span>Adicionar FGTS, horas extras, adicionais e mais</span>
        </button>
        <div class="mais oculto" id="mais">
          <div class="campo">
            <label for="c-fgts">Saldo do FGTS <span class="dica">está no app FGTS; se não souber, deixe em branco</span></label>
            <div class="moeda"><span>R$</span><input id="c-fgts" inputmode="decimal" placeholder="0,00" autocomplete="off"></div>
          </div>
          <div class="campo">
            <label for="c-variaveis">Horas extras, comissões e noturno <span class="dica">média/mês</span></label>
            <div class="moeda"><span>R$</span><input id="c-variaveis" inputmode="decimal" placeholder="0,00" autocomplete="off"></div>
          </div>
          <div class="campo">
            <label for="c-adicional">Adicional de insalubridade ou periculosidade</label>
            <select id="c-adicional">
              <option value="">Não recebo</option>
              <option value="i10">Insalubridade, grau mínimo (10% do mínimo)</option>
              <option value="i20">Insalubridade, grau médio (20% do mínimo)</option>
              <option value="i40">Insalubridade, grau máximo (40% do mínimo)</option>
              <option value="p30">Periculosidade (30% do salário)</option>
            </select>
          </div>
          <div class="campo"><label for="c-dep">Dependentes no Imposto de Renda</label><input id="c-dep" type="number" min="0" max="15" value="0" inputmode="numeric"></div>
          <label class="check"><input type="checkbox" id="c-adiant"> Já recebi a 1ª parcela do 13º deste ano</label>
          <label class="check"><input type="checkbox" id="c-gestante"> Eu estava grávida quando saí</label>
        </div>
        <button type="submit" class="enviar">Calcular minha rescisão</button>
        <div class="err" role="alert"></div>
      </form>""",
    "resultado": """
        <h2 id="r-titulo">Sua rescisão</h2>
        <div class="recibo">
          <div class="cab"><span>Demonstrativo da rescisão</span><span id="r-cab"></span></div>
          <table id="r-tabela"></table>
          <div class="total"><span>Você recebe da empresa</span><b id="r-liquido"></b></div>
        </div>
        <div class="fgts"><h3>FGTS</h3><table id="r-fgts"></table></div>
        <ul class="datas" id="r-prazo"></ul>""",
    "nota": "Estimativa pelas regras gerais da CLT e pelas tabelas de 2026. Convenção coletiva, banco de horas, faltas, pensão e outros descontos podem mudar o valor.",
    "titulo_regras": "O que entra na rescisão",
    "regras": [
        ("Saldo de salário", "Os dias trabalhados no mês da saída, contados sobre um mês de 30 dias."),
        ("Aviso prévio", "30 dias mais 3 por ano completo de empresa, até 90 (Lei 12.506/2011). Indenizado, conta como tempo de serviço e soma meses no 13º e nas férias. No acordo, vale a metade."),
        ("13º proporcional", "Um doze avos por mês do ano com 15 dias ou mais de trabalho. Na justa causa, não é devido."),
        ("Férias", "Vencidas, com 1/3, em qualquer saída. Proporcionais, com 1/3, menos na justa causa, inclusive para quem pediu demissão antes de 1 ano (Súmula 261 do TST)."),
        ("FGTS", "Depósito de 8% sobre o saldo, o aviso e o 13º da rescisão. Multa de 40% na dispensa sem justa causa e de 20% no acordo; saque do saldo inteiro na dispensa e de 80% no acordo."),
        ("Descontos", "INSS e Imposto de Renda só sobre o saldo de salário e o 13º. Aviso indenizado e férias indenizadas não têm desconto."),
    ],
    "faq": [
        ("Qual o prazo para a empresa pagar a rescisão?", "Até 10 dias corridos depois do fim do contrato, em qualquer tipo de saída (CLT art. 477, § 6º). Se atrasar, a empresa deve uma multa no valor de um salário (art. 477, § 8º)."),
        ("O que recebo se for demitido sem justa causa?", "Saldo de salário, aviso prévio (trabalhado ou indenizado), 13º proporcional, férias vencidas e proporcionais com 1/3, saque do FGTS com multa de 40% e, se cumprir os requisitos, o seguro-desemprego."),
        ("O que recebo se pedir demissão?", "Saldo de salário, 13º proporcional e férias vencidas e proporcionais com 1/3. Não há multa nem saque do FGTS, nem seguro-desemprego. Se não cumprir o aviso, a empresa pode descontar 30 dias de salário, a não ser que tenha dispensado o aviso."),
        ("Como funciona a rescisão por acordo?", "No acordo (CLT art. 484-A), o aviso indenizado e a multa do FGTS caem pela metade (multa de 20%), o saque do FGTS é de até 80% e não há seguro-desemprego. As demais verbas são pagas inteiras."),
        ("O que recebo na justa causa?", "Só o saldo de salário e as férias vencidas com 1/3. A justa causa é a punição mais grave e precisa de motivo previsto em lei e de prova; quando é aplicada sem base, pode ser revertida na Justiça."),
        ("Grávida pode ser demitida?", "Sem justa causa, não: a gestante tem estabilidade desde a confirmação da gravidez até 5 meses após o parto, mesmo que a empresa não soubesse (ADCT art. 10, II, b, e STF Tema 497). Se aconteceu, cabe pedir a volta ao trabalho ou a indenização do período."),
        ("Qual o prazo para cobrar a rescisão na Justiça?", "Até 2 anos depois do fim do contrato, alcançando os últimos 5 anos de trabalho (CF art. 7º, XXIX)."),
    ],
    "rodape": "Tabelas: INSS da Portaria Interministerial MPS/MF 13/2026 e Imposto de Renda com a redução da Lei 15.270/2025.",
    "outras": LINKS["13"] + " · " + LINKS["licenca"],
    "scripts": '  <script src="js/calculo-13.js?v=20261109b"></script>\n  <script src="js/calculo-rescisao.js?v=20261116"></script>',
    "js": r"""
    var OPCOES_AVISO = {
      sem_justa_causa: [['indenizado', 'Não trabalhei o aviso (foi indenizado)'], ['trabalhado', 'Trabalhei o aviso']],
      acordo: [['indenizado', 'Não trabalhei o aviso (foi indenizado)'], ['trabalhado', 'Trabalhei o aviso']],
      pediu_demissao: [['trabalhado', 'Cumpri o aviso'], ['dispensado', 'A empresa me dispensou do aviso'], ['nao_cumprido', 'Não cumpri o aviso']],
      justa_causa: []
    };
    var NOMES = { sem_justa_causa: 'Demitido sem justa causa', pediu_demissao: 'Pediu demissão', acordo: 'Acordo', justa_causa: 'Justa causa' };
    function opcoesAviso() {
      var s = $('c-situacao').value, op = OPCOES_AVISO[s];
      $('bloco-aviso').classList.toggle('oculto', !op.length);
      $('c-aviso').innerHTML = op.map(function (o) { return '<option value="' + o[0] + '">' + o[1] + '</option>'; }).join('');
    }
    $('c-situacao').addEventListener('change', opcoesAviso); opcoesAviso();

    window.CALC = {
      tag: 'calculadora-rescisao', area: 'trabalhista', campanha: 'calculadora-rescisao-2026',
      montarEntrada: function (f) {
        var salario = numero($('c-salario').value), adm = $('c-admissao').value, saida = $('c-saida').value;
        if (salario < 100) return CALC_ERRO(f, $('c-salario'), 'Informe o salário bruto por mês.');
        if (!adm) return CALC_ERRO(f, $('c-admissao'), 'Informe a data de admissão (pode ser aproximada).');
        if (!saida) return CALC_ERRO(f, $('c-saida'), 'Informe o último dia de trabalho.');
        if (saida < adm) return CALC_ERRO(f, $('c-saida'), 'A saída não pode ser antes da admissão.');
        var adic = $('c-adicional').value;
        return {
          salario: salario, situacao: $('c-situacao').value, admissao: adm, saida: saida, aviso: $('c-aviso').value || 'trabalhado',
          feriasVencidas: +$('c-ferias').value, saldoFgts: numero($('c-fgts').value), mediaVariaveis: numero($('c-variaveis').value),
          insalubridade: adic.charAt(0) === 'i' ? +adic.slice(1) : 0, periculosidade: adic === 'p30',
          dependentes: +$('c-dep').value || 0, primeiraJaRecebida: $('c-adiant').checked, gestante: $('c-gestante').checked
        };
      },
      calcular: function (e) { return window.CalculoRescisao.calcularRescisao(e); },
      mostrar: function (r, nome) {
        function linha(a, b, c) { return '<tr' + (c ? ' class="' + c + '"' : '') + '><td>' + a + '</td><td>' + b + '</td></tr>'; }
        var h = linha('Verbas', '', 'titulo') + r.verbas.map(function (v) { return linha(v.nome, reais(v.valor)); }).join('');
        h += linha('Total bruto', reais(r.bruto), 'sep parcela');
        if (r.descontos.length) h += linha('Descontos', '', 'titulo') + r.descontos.map(function (d) { return linha(d.nome, '− ' + reais(d.valor), 'desc'); }).join('');
        $('r-tabela').innerHTML = h;
        $('r-cab').textContent = r.projecao ? 'aviso de ' + r.diasAviso + ' dias' : '';
        $('r-liquido').textContent = reais(r.liquido);
        var f = r.fgts;
        $('r-fgts').innerHTML = linha('Saldo na conta' + (f.estimado ? ' (estimado)' : ''), reais(f.saldo)) +
          linha('Depósito sobre a rescisão', reais(f.depositoRescisao)) +
          linha('Multa', f.multa ? reais(f.multa) : 'não há') +
          linha('Você pode sacar', f.saque ? reais(f.saque) : 'não há saque nesta saída', 'forte');
        $('r-prazo').innerHTML = '<li class="destaque"><span>A empresa deve pagar até</span><b>' + dataBR(r.prazoPagamento, true) + '</b></li>';
        $('r-alertas').innerHTML = r.avisos.map(function (a) { return '<li>' + a + '</li>'; }).join('');
        $('r-titulo').textContent = nome + ', esta é a sua rescisão';
      },
      resumo: function (e, r) {
        return ' [Situação: ' + NOMES[e.situacao] + '] [Salário: ' + reais(e.salario) + '] [Admissão: ' + e.admissao + '] [Saída: ' + e.saida + ']' +
          ' [Aviso: ' + e.aviso + '] [Resultado: bruto ' + reais(r.bruto) + ', líquido ' + reais(r.liquido) + ', FGTS saque ' + reais(r.fgts.saque) + ']' +
          (e.gestante ? ' [GESTANTE]' : '') + (e.feriasVencidas ? ' [Férias vencidas: ' + e.feriasVencidas + ']' : '');
      },
      textoWa: function (r, e) { return 'Olá! Fiz a calculadora de rescisão no site (' + NOMES[e.situacao] + ') e quero conferir o meu caso. Resultado: ' + reais(r.liquido) + ' líquido.'; }
    };
""",
}

# ---------------------------------------------------------------- licença-maternidade
LICENCA = {
    "url": SITE + "/lp/calculadora-licenca-maternidade.html",
    "title": "Calculadora da licença-maternidade 2026: datas e estabilidade",
    "description": "Descubra quando começa e termina a sua licença-maternidade (120 ou 180 dias), a data de volta ao trabalho, até quando vai a estabilidade da gestante e as pausas para amamentar. Vale para adoção.",
    "og_title": "Calculadora da licença-maternidade",
    "og_description": "Início, fim, volta ao trabalho e estabilidade: todas as datas da sua licença.",
    "nome_app": "Calculadora da licença-maternidade",
    "descricao_app": "Calcula as datas da licença-maternidade CLT de 120 dias ou de 180 dias na Empresa Cidadã, com início até 28 dias antes do parto, contagem a partir da alta hospitalar (STF ADI 6327), adoção, fim da estabilidade da gestante e pausas para amamentação.",
    "h1": "As datas da sua <i>licença-maternidade</i>",
    "sub": "Informe a data do parto, prevista ou já ocorrida. A conta mostra quando a licença começa e termina, quando você volta e até quando dura a estabilidade.",
    "prazos": [
        ("Licença pela CLT", "120 dias"),
        ("Empresa Cidadã", "180 dias<span class=\"obs\">pedido até 1 mês após o parto</span>"),
        ("Estabilidade", "até 5 meses<span class=\"obs\">depois do parto</span>"),
    ],
    "form": """
      <form id="etapa1" novalidate>
        <h2>Calculadora da licença</h2>
        <p class="fs">Vale para quem trabalha com carteira assinada.</p>
        <div class="campo">
          <span class="rotulo">A licença é por</span>
          <div class="opcoes">
            <label><input type="radio" name="tipo" value="parto" checked> Parto</label>
            <label><input type="radio" name="tipo" value="adocao"> Adoção ou guarda</label>
          </div>
        </div>
        <div class="campo">
          <label for="c-data" id="rotulo-data">Data do parto <span class="dica">prevista ou já ocorrida</span></label>
          <input id="c-data" type="date" min="2025-01-01" max="2027-12-31">
        </div>
        <div class="campo" id="bloco-antes">
          <label for="c-antes">Quando quer (ou precisou) começar a licença</label>
          <select id="c-antes">
            <option value="0">No dia do parto</option>
            <option value="7">1 semana antes</option>
            <option value="14">2 semanas antes</option>
            <option value="21">3 semanas antes</option>
            <option value="28">4 semanas antes (o máximo, 28 dias)</option>
          </select>
        </div>
        <div class="campo">
          <label for="c-cidada">A empresa é do programa Empresa Cidadã?</label>
          <select id="c-cidada">
            <option value="nao_sei">Não sei</option>
            <option value="sim">Sim (licença de 180 dias)</option>
            <option value="nao">Não (licença de 120 dias)</option>
          </select>
        </div>
        <label class="check" id="bloco-internacao"><input type="checkbox" id="c-internacao"> A mãe ou o bebê ficou internado mais de 2 semanas depois do parto</label>
        <div class="campo oculto" id="bloco-alta">
          <label for="c-alta">Data da alta <span class="dica">a última, da mãe ou do bebê</span></label>
          <input id="c-alta" type="date" min="2025-01-01" max="2027-12-31">
        </div>
        <button type="submit" class="enviar">Ver as datas da minha licença</button>
        <div class="err" role="alert"></div>
      </form>""",
    "resultado": """
        <h2 id="r-titulo">Sua licença-maternidade</h2>
        <div class="recibo">
          <div class="cab"><span>Calendário da licença</span><span id="r-cab"></span></div>
          <ul class="datas" id="r-datas"></ul>
        </div>""",
    "nota": "Datas pelas regras gerais da CLT. Convenção coletiva ou política da empresa podem dar mais tempo. Servidoras públicas seguem o regime próprio.",
    "titulo_regras": "Como a licença é contada",
    "regras": [
        ("120 dias pela CLT", "Licença remunerada com o salário integral, garantida pela Constituição (art. 7º, XVIII) e pela CLT (art. 392)."),
        ("180 dias na Empresa Cidadã", "Empresas do programa (Lei 11.770/2008) prorrogam por mais 60 dias. A empregada precisa pedir até o fim do primeiro mês depois do parto."),
        ("Começo da licença", "Pode começar até 28 dias antes do parto, com atestado médico (CLT art. 392, § 1º)."),
        ("Internação longa", "Se a mãe ou o bebê ficar internado mais de 2 semanas, a licença começa a contar da alta, a que vier por último (STF, ADI 6327)."),
        ("Adoção", "A mãe adotante tem a mesma licença da mãe biológica, contada da guarda ou da adoção, seja qual for a idade da criança (CLT art. 392-A e STF, ADI 7.495)."),
        ("Estabilidade", "Ninguém pode demitir a gestante sem justa causa desde a confirmação da gravidez até 5 meses após o parto (ADCT art. 10, II, b), mesmo que a empresa não soubesse. A adotante tem a mesma proteção a partir da guarda (CLT art. 391-A)."),
    ],
    "faq": [
        ("A licença-maternidade é de 120 ou 180 dias?", "A regra da CLT é de 120 dias. Os 180 dias valem para quem trabalha em empresa do programa Empresa Cidadã (Lei 11.770/2008) ou tem convenção coletiva ou política da empresa mais favorável. A decisão do STF de setembro de 2026 (ADI 7.495) garantiu a igualdade entre mães biológicas e adotantes, mas não deu 180 dias para todas."),
        ("Quando a licença começa?", "No dia do parto ou até 28 dias antes, com atestado médico. Se a mãe ou o bebê ficar internado mais de duas semanas, a contagem começa na alta hospitalar (STF, ADI 6327)."),
        ("Quem está de licença-maternidade recebe 13º?", "Sim. A licença-maternidade conta como tempo de serviço, então o 13º vem inteiro, sem desconto dos meses de licença. A empresa paga normalmente e depois compensa com o INSS a parte que corresponde ao período da licença. Veja os detalhes no artigo sobre o 13º da gestante na licença-maternidade."),
        ("Quanto recebo durante a licença?", "Quem tem carteira assinada recebe o salário integral, pago pela empresa, que depois desconta o valor do INSS. A licença conta como tempo de serviço para férias e 13º."),
        ("Posso ser demitida depois que voltar?", "A estabilidade vai até 5 meses depois do parto. Como a licença de 120 dias dura cerca de 4 meses, a proteção continua por mais ou menos um mês depois da volta. Na licença de 180 dias, ela já terminou quando você volta."),
        ("Tenho direito a pausas para amamentar?", "Sim. Até o bebê completar 6 meses, você tem direito a dois descansos de meia hora por dia durante a jornada (CLT art. 396), também na adoção. O prazo pode ser ampliado por recomendação médica."),
        ("A mãe adotante tem a mesma licença?", "Sim. Desde a decisão do STF de setembro de 2026 (ADI 7.495), a licença da adotante tem o mesmo conteúdo da licença da mãe biológica, sem variar pela idade da criança, contada a partir da guarda ou da adoção."),
    ],
    "rodape": "Fontes: Constituição art. 7º, XVIII; ADCT art. 10, II, b; CLT arts. 391-A, 392, 392-A e 396; Lei 11.770/2008; STF ADI 6327 e ADI 7.495.",
    "outras": LINKS["13"] + " · " + LINKS["rescisao"],
    "scripts": '  <script src="js/calculo-licenca.js?v=20261116"></script>',
    "js": r"""
    function tipo() { return document.querySelector('[name=tipo]:checked').value; }
    function atualizar() {
      var parto = tipo() === 'parto';
      $('rotulo-data').innerHTML = parto ? 'Data do parto <span class="dica">prevista ou já ocorrida</span>' : 'Data da guarda ou da adoção';
      $('bloco-antes').classList.toggle('oculto', !parto);
      $('bloco-internacao').classList.toggle('oculto', !parto);
      $('bloco-alta').classList.toggle('oculto', !parto || !$('c-internacao').checked);
    }
    document.querySelectorAll('[name=tipo]').forEach(function (r) { r.addEventListener('change', atualizar); });
    $('c-internacao').addEventListener('change', atualizar);

    window.CALC = {
      tag: 'calculadora-licenca', area: 'gestante', campanha: 'calculadora-licenca-maternidade',
      montarEntrada: function (f) {
        var d = $('c-data').value, parto = tipo() === 'parto';
        if (!d) return CALC_ERRO(f, $('c-data'), parto ? 'Informe a data do parto (pode ser a prevista).' : 'Informe a data da guarda ou da adoção.');
        var alta = parto && $('c-internacao').checked ? $('c-alta').value : '';
        if (parto && $('c-internacao').checked && !alta) return CALC_ERRO(f, $('c-alta'), 'Informe a data da alta.');
        if (alta && alta < d) return CALC_ERRO(f, $('c-alta'), 'A alta não pode ser antes do parto.');
        return { tipo: tipo(), data: d, diasAntes: parto ? +$('c-antes').value : 0, cidada: $('c-cidada').value, alta: alta || null };
      },
      calcular: function (e) {
        var L = window.CalculoLicenca.calcularLicenca;
        var base = { tipo: e.tipo, data: e.data, diasAntes: e.diasAntes, alta: e.alta };
        return { c120: L(Object.assign({}, base, { empresaCidada: false })), c180: L(Object.assign({}, base, { empresaCidada: true })), cidada: e.cidada };
      },
      mostrar: function (r, nome) {
        var a = r.c120, b = r.c180, sim = r.cidada === 'sim', talvez = r.cidada === 'nao_sei';
        function li(rot, val, cl, nota) { return '<li' + (cl ? ' class="' + cl + '"' : '') + '><span>' + rot + (nota ? '<small>' + nota + '</small>' : '') + '</span><b>' + val + '</b></li>'; }
        var h = li('Começo da licença', dataBR(a.inicio, true), '', a.contaDaAlta ? 'contada da alta (internação de mais de 2 semanas)' : '');
        if (!sim) h += li('Fim dos 120 dias', dataBR(a.fim, true), talvez ? '' : 'destaque') + li('Volta ao trabalho', dataBR(a.retorno, true), talvez ? '' : 'destaque');
        if (sim || talvez) {
          h += li('Fim dos 180 dias' + (talvez ? ', se a empresa for Cidadã' : ''), dataBR(b.fim, true), 'destaque') + li('Volta ao trabalho' + (talvez ? ' nesse caso' : ''), dataBR(b.retorno, true), 'destaque');
          h += li('Prazo para pedir os 60 dias a mais', dataBR(b.prazoProrrogacao, true), '', 'peça por escrito');
        }
        h += li('Estabilidade até', dataBR(a.fimEstabilidade, true), '', a.tipo === 'parto' ? '5 meses depois do parto' : '5 meses depois da guarda');
        if (a.fimAmamentacao) h += li('Pausas para amamentar até', dataBR(a.fimAmamentacao, true), '', '2 de 30 minutos por dia');
        $('r-datas').innerHTML = h;
        $('r-cab').textContent = sim ? '180 dias' : talvez ? '120 ou 180 dias' : '120 dias';
        var av = [];
        if (talvez) av.push('Pergunte ao RH se a empresa é do programa Empresa Cidadã. Se for, peça a prorrogação por escrito até ' + dataBR(b.prazoProrrogacao) + '.');
        av.push('Durante a licença você recebe o salário integral, e esse período conta para as férias e o 13º: o 13º vem inteiro. <a href="/blog/13-salario-gestante-licenca-maternidade.html">Entenda o 13º na licença</a>.');
        if (!sim) av.push('Depois que você volta, a estabilidade ainda dura até ' + dataBR(a.fimEstabilidade) + '. Demissão sem justa causa antes disso é proibida.');
        $('r-alertas').innerHTML = av.map(function (x) { return '<li>' + x + '</li>'; }).join('');
        $('r-titulo').textContent = nome + ', estas são as datas da sua licença';
      },
      resumo: function (e, r) {
        return ' [Tipo: ' + e.tipo + '] [Data: ' + e.data + '] [Empresa Cidadã: ' + e.cidada + ']' + (e.alta ? ' [Alta: ' + e.alta + ']' : '') +
          ' [Fim da estabilidade: ' + r.c120.fimEstabilidade + ']';
      },
      textoWa: function (r, e) { return 'Olá! Fiz a calculadora da licença-maternidade no site e quero tirar uma dúvida sobre os meus direitos.'; }
    };
""",
}

for nome, cfg in (("calculadora-rescisao.html", RESCISAO), ("calculadora-licenca-maternidade.html", LICENCA)):
    (LP / nome).write_text(pagina(cfg), encoding="utf-8")
    print("gerado", nome)
