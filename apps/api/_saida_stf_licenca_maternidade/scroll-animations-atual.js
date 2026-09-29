/* =====================================================
   SCROLL ANIMATIONS & INTERSECTION OBSERVER
   Letícia Barros | Advocacia e Consultoria Jurídica
   ===================================================== */

document.addEventListener('DOMContentLoaded', function() {
    // Intersection Observer para animações ao scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Adicionar classe para ativar animação
                entry.target.classList.add('in-view');

                // Se tiver números, animar contagem
                if (entry.target.dataset.target) {
                    animateCounter(entry.target);
                }
            }
        });
    }, observerOptions);

    // Seletores de elementos para animar automaticamente
    const elementsToAnimate = [
        '.scroll-animate',
        '.stat-number',
        '[data-target]',
        '.value-card',
        '.right-card',
        '.check-item',
        '.blog-card',
        '.process-step',
        '.faq-item',
        '.section-header .reveal',
        '.reveal-left',
        '.reveal-right'
    ];

    // Observar todos os elementos
    document.querySelectorAll(elementsToAnimate.join(', ')).forEach(el => {
        observer.observe(el);
    });

    // Animar também grids inteiras
    document.querySelectorAll('.values-grid, .rights-grid, .checklist-grid, .blog-grid, .process-grid').forEach(grid => {
        observer.observe(grid);
    });

    // Rede de segurança: em alguns navegadores mobile o IntersectionObserver
    // não dispara de forma confiável, e o conteúdo (ex: cards do blog) fica
    // com opacity:0 pra sempre por causa do CSS de animação. Depois de um
    // tempo, força a classe 'in-view' em tudo que ainda não animou, pra
    // garantir que o conteúdo real sempre apareça.
    setTimeout(() => {
        document.querySelectorAll(elementsToAnimate.join(', ')).forEach(el => {
            el.classList.add('in-view');
        });
        document.querySelectorAll('.values-grid, .rights-grid, .checklist-grid, .blog-grid, .process-grid').forEach(grid => {
            grid.classList.add('in-view');
        });
    }, 1200);

    // Animar contadores numéricos
    function animateCounter(element) {
        const target = parseInt(element.dataset.target);
        if (isNaN(target) || element.dataset.animated) return;

        element.dataset.animated = 'true';
        const duration = 1.5; // segundos
        const steps = 60;
        const increment = target / steps;
        let current = 0;

        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                element.textContent = target.toLocaleString('pt-BR');
                clearInterval(timer);
            } else {
                element.textContent = Math.floor(current).toLocaleString('pt-BR');
            }
        }, (duration * 1000) / steps);
    }

    // Observador para hero stats (se tiverem números)
    const heroStats = document.querySelectorAll('.hero-stat, .stat-value, .trust-text strong');
    heroStats.forEach(stat => {
        observer.observe(stat);
    });
});

// Função auxiliar para adicionar classe ao scroll
window.addEventListener('scroll', function() {
    const scrolled = window.scrollY > 100;
    const header = document.querySelector('.header, .lp-header');

    if (header) {
        if (scrolled && !header.classList.contains('scrolled')) {
            header.classList.add('scrolled');
        } else if (!scrolled && header.classList.contains('scrolled')) {
            header.classList.remove('scrolled');
        }
    }
}, { passive: true });

// Parallax suave no hero image (opcional)
window.addEventListener('scroll', function() {
    const heroImg = document.querySelector('.lp-hero-img img, .hero-image img');
    if (heroImg && window.innerWidth > 768) {
        const scrollY = window.scrollY;
        heroImg.style.transform = `translateY(${scrollY * 0.05}px)`;
    }
}, { passive: true });
