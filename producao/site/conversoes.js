/*
 * Medição de contatos e atalhos de contato do site (Orbit, 22/10/2026).
 *
 * - Evento no Google Analytics e no pixel da Meta a cada contato:
 *     contato_whatsapp  (clique em qualquer link wa.me)          -> pixel "Contact"
 *     contato_ligacao   (clique em link tel:)                    -> pixel "Contact"
 *     generate_lead     (formulário aceito pelo CRM jurídico)    -> pixel "Lead"
 * - A mensagem do WhatsApp sai com a página de origem, para quem atende saber de onde veio.
 * - Botão "Ligar" nos blocos de contato e botão flutuante de ligar no celular.
 * - Bloco de contato no meio dos artigos do blog, depois de "Como provar" / "O que fazer".
 * Textos de chamada impessoais (regra da OAB): nada de "fale comigo" nem promessa.
 */
(function () {
  'use strict';
  var TEL = '+5527995151402';
  var TEL_TEXTO = '(27) 99515-1402';
  var WHATS = 'https://wa.me/5527995151402';
  var ICONE_TEL = '<svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1z"/></svg>';

  var PIXEL_META = '858690737244687';

  // Páginas sem o pixel da Meta (artigos novos do blog, algumas LPs) passam a ter, carregado na primeira
  // interação ou em 2 s, como na home. Onde a página já traz o pixel, nada é carregado de novo.
  function carregarPixelSeFaltar() {
    if (typeof window.fbq === 'function' || document.documentElement.innerHTML.indexOf('fbevents.js') !== -1) return;
    var feito = false;
    function carregar() {
      if (feito || typeof window.fbq === 'function') return;
      feito = true;
      /* eslint-disable */
      !function (f, b, e, v, n, t, s) {
        if (f.fbq) return; n = f.fbq = function () { n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments); };
        if (!f._fbq) f._fbq = n; n.push = n; n.loaded = !0; n.version = '2.0'; n.queue = [];
        t = b.createElement(e); t.async = !0; t.src = v; s = b.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t, s);
      }(window, document, 'script', 'https://connect.facebook.net/en_US/fbevents.js');
      /* eslint-enable */
      window.fbq('init', PIXEL_META);
      window.fbq('track', 'PageView');
    }
    ['scroll', 'mousemove', 'touchstart', 'keydown', 'click'].forEach(function (ev) {
      window.addEventListener(ev, carregar, { once: true, passive: true, capture: true });
    });
    setTimeout(carregar, 2000);
  }
  carregarPixelSeFaltar();

  function tituloDaPagina() {
    return (document.title || '').split(' | ')[0].trim();
  }

  // O Analytics da home e das LPs carrega na primeira interação; garante a fila antes do evento.
  function garantirAnalytics() {
    if (typeof window.carregarRastreadores === 'function') {
      try { window.carregarRastreadores(); } catch (e) { /* segue */ }
    }
    window.dataLayer = window.dataLayer || [];
    if (typeof window.gtag !== 'function') {
      window.gtag = function () { window.dataLayer.push(arguments); };
    }
  }

  function registrar(nome, extra) {
    garantirAnalytics();
    var dados = { pagina: location.pathname, titulo_pagina: tituloDaPagina() };
    for (var k in (extra || {})) { dados[k] = extra[k]; }
    try { window.gtag('event', nome, dados); } catch (e) { /* segue */ }
    if (typeof window.fbq === 'function') {
      try { window.fbq('track', nome === 'generate_lead' ? 'Lead' : 'Contact', { content_name: nome }); } catch (e) { /* segue */ }
    }
  }

  function whatsComOrigem(href) {
    try {
      var url = new URL(href, location.href);
      var texto = url.searchParams.get('text') || 'Olá, gostaria de orientação jurídica.';
      if (texto.indexOf('vim pela página') !== -1 || texto.indexOf('li o artigo') !== -1) return href;
      // %20 (e não "+") para os espaços: alguns aplicativos mostram o "+" na mensagem.
      return url.origin + url.pathname + '?text=' +
        encodeURIComponent(texto + ' (vim pela página: ' + tituloDaPagina() + ')');
    } catch (e) {
      return href;
    }
  }

  // Cliques em WhatsApp e telefone, em qualquer lugar da página (inclusive botões criados depois).
  document.addEventListener('click', function (e) {
    var alvo = e.target && e.target.closest ? e.target.closest('a[href]') : null;
    if (!alvo) return;
    var href = alvo.getAttribute('href') || '';
    if (/wa\.me|api\.whatsapp\.com/.test(href)) {
      alvo.setAttribute('href', whatsComOrigem(alvo.href));
      registrar('contato_whatsapp', { link_texto: (alvo.textContent || '').trim().slice(0, 60) });
    } else if (/^tel:/.test(href)) {
      registrar('contato_ligacao', {});
    }
  }, true);

  // Formulário: conta só quando o CRM responde OK (o envio é feito por fetch no pages.js e nas LPs).
  if (typeof window.fetch === 'function') {
    var fetchOriginal = window.fetch;
    window.fetch = function (entrada) {
      var url = typeof entrada === 'string' ? entrada : (entrada && entrada.url) || '';
      var promessa = fetchOriginal.apply(this, arguments);
      if (url.indexOf('/api/public/lead') !== -1) {
        promessa.then(function (resp) {
          if (resp && resp.ok) registrar('generate_lead', {});
        }).catch(function () { /* erro já tratado pela página */ });
      }
      return promessa;
    };
  }

  function botaoLigar(texto) {
    var a = document.createElement('a');
    a.href = 'tel:' + TEL;
    a.innerHTML = ICONE_TEL + (texto ? ' <span>' + texto + '</span>' : '');
    return a;
  }

  function estilizarBotaoLigar(a) {
    a.style.cssText = 'display:inline-flex;align-items:center;gap:8px;margin:12px 0 0 12px;padding:12px 22px;' +
      'border:1px solid #c9a962;border-radius:999px;color:#c9a962;text-decoration:none;font-weight:600;';
  }

  // WhatsApp que já abre a conversa dizendo de qual artigo a pessoa veio.
  function botaoWhatsArtigo() {
    var whats = document.createElement('a');
    var texto = /\/blog\//.test(location.pathname)
      ? 'Olá, li o artigo "' + tituloDaPagina() + '" e gostaria de orientação.'
      : 'Olá, gostaria de orientação jurídica.';
    whats.href = WHATS + '?text=' + encodeURIComponent(texto);
    whats.target = '_blank';
    whats.rel = 'noopener';
    whats.textContent = 'Orientação pelo WhatsApp';
    whats.style.cssText = 'display:inline-flex;align-items:center;margin:12px 0 0;padding:12px 22px;border-radius:999px;' +
      'background:#c9a962;color:#111;text-decoration:none;font-weight:600;';
    return whats;
  }

  // Seção depois da qual entra o bloco: a de "Como provar" / "O que fazer"; sem ela, a do meio do artigo,
  // desde que o texto ainda não tenha nenhum bloco de contato (27/10: os artigos mais lidos ficavam sem).
  function secaoDoBloco(corpo) {
    var titulos = corpo.querySelectorAll('h2');
    for (var i = 0; i < titulos.length; i++) {
      if (/como provar|o que (voc[eê] pode )?fazer|o que acontece/i.test(titulos[i].textContent)) return titulos[i];
    }
    if (corpo.querySelector('.article-cta')) return null;
    var conteudo = [];
    for (var j = 0; j < titulos.length; j++) {
      if (!/perguntas frequentes|leia tamb[eé]m/i.test(titulos[j].textContent)) conteudo.push(titulos[j]);
    }
    return conteudo.length >= 3 ? conteudo[Math.floor((conteudo.length - 1) / 2)] : null;
  }

  function blocoNoMeioDoArtigo(corpo) {
    if (corpo.querySelector('.contato-meio')) return;
    var gatilho = secaoDoBloco(corpo);
    if (!gatilho) return;
    // fim da seção = próximo h2 (ou nada, se for a última)
    var proximo = gatilho.nextElementSibling;
    while (proximo && proximo.tagName !== 'H2') { proximo = proximo.nextElementSibling; }
    if (!proximo) return;

    var bloco = document.createElement('div');
    bloco.className = 'callout-box contato-meio';
    var whats = botaoWhatsArtigo();
    var ligar = botaoLigar('Ligar: ' + TEL_TEXTO);
    estilizarBotaoLigar(ligar);
    bloco.innerHTML = '<h4>Está passando por isso?</h4><p>Se essa é a sua situação, busque orientação jurídica antes de tomar qualquer decisão.</p>';
    bloco.appendChild(whats);
    bloco.appendChild(ligar);
    proximo.parentNode.insertBefore(bloco, proximo);
  }

  function prepararPagina() {
    // WhatsApp e "Ligar" nos blocos de contato dos artigos. Antes eles só levavam à página de contato
    // (um passo a mais); em 23-27/10 nenhuma visita virou contato.
    var ctas = document.querySelectorAll('.article-cta');
    for (var i = 0; i < ctas.length; i++) {
      if (!ctas[i].querySelector('a[href*="wa.me"]')) {
        var paraContato = ctas[i].querySelector('a[href*="contato.html"]');
        var w = botaoWhatsArtigo();
        if (paraContato) {
          // O botão do bloco ("Busque orientação jurídica") passa a abrir o WhatsApp direto.
          paraContato.href = w.href;
          paraContato.target = '_blank';
          paraContato.rel = 'noopener';
        } else {
          w.style.marginRight = '12px';
          ctas[i].appendChild(w);
        }
      }
      if (ctas[i].querySelector('a[href^="tel:"]')) continue;
      var b = botaoLigar('Ligar: ' + TEL_TEXTO);
      estilizarBotaoLigar(b);
      b.style.marginLeft = '0';
      ctas[i].appendChild(b);
    }
    // Bloco de contato no meio dos artigos do blog.
    var corpo = document.querySelector('.article-body');
    if (corpo && /\/blog\//.test(location.pathname)) blocoNoMeioDoArtigo(corpo);
    // Botão flutuante de ligar no celular (à esquerda; o do WhatsApp fica à direita).
    if (window.matchMedia && window.matchMedia('(max-width: 768px)').matches && !document.querySelector('.ligar-float')) {
      var f = botaoLigar('');
      f.className = 'ligar-float';
      f.setAttribute('aria-label', 'Ligar para o escritório');
      f.style.cssText = 'position:fixed;left:16px;bottom:20px;z-index:999;width:56px;height:56px;border-radius:50%;' +
        'background:#c9a962;color:#111;display:flex;align-items:center;justify-content:center;' +
        'box-shadow:0 4px 14px rgba(0,0,0,.3);text-decoration:none;';
      document.body.appendChild(f);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', prepararPagina);
  } else {
    prepararPagina();
  }
})();
