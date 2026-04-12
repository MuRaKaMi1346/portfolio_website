document.addEventListener("DOMContentLoaded", () => {

    // 1. Typing effect for hero h1 (index page only)
    const heroTitle = document.getElementById('hero-title');
    if (heroTitle) {
        heroTitle.style.removeProperty('--hide-cursor'); // let CSS handle cursor
        const text = "PASSAWEE\nKAEWDUK";
        let i = 0;

        function typeWriter() {
            if (i < text.length) {
                const ch = text.charAt(i);
                if (ch === '\n') {
                    heroTitle.innerHTML += '<br>';
                } else {
                    heroTitle.innerHTML += ch;
                }
                i++;
                setTimeout(typeWriter, 80);
            }
        }

        // Hide the CSS cursor while typing since h1::after already adds one
        heroTitle.parentElement.querySelector('h1')?.style.setProperty('--done', '0');
        setTimeout(typeWriter, 400);
    }

    // 2. Scroll reveal for .content children
    const observerOptions = {
        threshold: 0.08,
        rootMargin: "0px 0px -40px 0px"
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('show');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Reveal the main content card
    document.querySelectorAll('.content').forEach(el => {
        observer.observe(el);
    });

    // Staggered reveal for inner elements
    const revealTargets = document.querySelectorAll(
        '.content h2, .content p, .content .hero-links, .content .info-grid, ' +
        '.content .timeline-item, .content .skills-section, .content .project-card, ' +
        '.content .contact-info, .content .form-group, .content button, ' +
        '.content .table-wrap, .content .empty-state'
    );

    revealTargets.forEach((el, i) => {
        el.classList.add('hidden');
        el.style.transitionDelay = `${i * 60}ms`;
        observer.observe(el);
    });

    // 3. Mouse particle trail
    document.addEventListener('mousemove', function(e) {
        const particle = document.createElement('div');
        particle.className = 'mouse-particle';
        const colors = ['#00e5ff', '#d400ff', '#f0f4ff'];
        const color = colors[Math.floor(Math.random() * colors.length)];
        particle.style.cssText = `left:${e.clientX - 3}px; top:${e.clientY - 3}px; background:${color}; box-shadow:0 0 8px ${color};`;
        document.body.appendChild(particle);

        setTimeout(() => {
            particle.style.opacity = '0';
            particle.style.transform = 'scale(0)';
        }, 60);

        setTimeout(() => particle.remove(), 600);
    });
});
