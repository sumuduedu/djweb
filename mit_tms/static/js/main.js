// ================= FLASH MESSAGE HELPER =================
function autoRemoveFlashMessages() {
    document.querySelectorAll(".flash-message").forEach(el => {
        // avoid double-registering
        if (el.dataset.timerSet) return;
        el.dataset.timerSet = "true";

        setTimeout(() => {
            el.style.transition = "opacity 0.5s ease, transform 0.5s ease";
            el.style.opacity = "0";
            el.style.transform = "translateY(-8px)";
            setTimeout(() => el.remove(), 500);
        }, 5000);
    });
}

// ================= USER DROPDOWN =================
function initUserDropdown() {
    const userBtn  = document.getElementById("userButton");
    const userMenu = document.getElementById("userMenu");
    if (!userBtn || !userMenu) return;

    userBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        userMenu.classList.toggle("hidden");
    });

    document.addEventListener("click", (e) => {
        if (
            !e.target.closest("#userMenu") &&
            !e.target.closest("#userButton")
        ) {
            userMenu.classList.add("hidden");
        }
    });
}

// ================= SCROLL ANIMATION =================
function initScrollAnimation() {
    if (!('IntersectionObserver' in window)) return;

    const observer = new IntersectionObserver((entries, obs) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("show");
                obs.unobserve(entry.target);
            }
        });
    }, { threshold: 0.2 });

    document.querySelectorAll(".fade-up, .stagger").forEach(el => {
        observer.observe(el);
    });
}

// ================= PARALLAX =================
function initParallax() {
    const prefersReducedMotion = window.matchMedia(
        "(prefers-reduced-motion: reduce)"
    ).matches;
    const parallaxElements = document.querySelectorAll(".parallax");

    if (prefersReducedMotion || !parallaxElements.length) return;

    let ticking = false;

    window.addEventListener("scroll", () => {
        if (ticking) return;
        ticking = true;

        window.requestAnimationFrame(() => {
            parallaxElements.forEach(el => {
                const speed = parseFloat(el.dataset.speed) || 0.3;
                el.style.transform = `translateY(${window.scrollY * speed}px)`;
            });
            ticking = false;
        });
    });
}

// ================= SIDEBAR COLLAPSE SYNC =================
function initSidebarCollapse() {
    const sidebar = document.querySelector(".sidebar");
    if (!sidebar) return;

    // sync on Alpine store change
    document.addEventListener("alpine:initialized", () => {
        if (typeof Alpine === "undefined") return;

        // apply saved state immediately
        const saved = localStorage.getItem("sidebarCollapsed") === "true";
        sidebar.classList.toggle("sidebar-collapsed", saved);

        // watch for store changes
        Alpine.effect(() => {
            const collapsed = Alpine.store("sidebar")?.collapsed;
            if (typeof collapsed === "boolean") {
                sidebar.classList.toggle("sidebar-collapsed", collapsed);
            }
        });
    });
}

// ================= HTMX: re-run flash on swap =================
function initHtmxListeners() {
    document.addEventListener("htmx:afterSwap", () => {
        autoRemoveFlashMessages();
    });
}

// ================= ACTIVE NAV LINK =================
function initActiveNavLink() {
    const currentPath = window.location.pathname;
    document.querySelectorAll(".nav-link").forEach(link => {
        const href = link.getAttribute("href");
        if (href && currentPath.startsWith(href) && href !== "/") {
            link.classList.add("active");
        } else if (href === "/" && currentPath === "/") {
            link.classList.add("active");
        }
    });
}

// ================= TOOLTIP POSITION FIX =================
function initTooltips() {
    document.querySelectorAll(".nav-link").forEach(link => {
        const tooltip = link.querySelector(".sidebar-tooltip");
        if (!tooltip) return;

        link.addEventListener("mouseenter", () => {
            const rect = link.getBoundingClientRect();
            // if tooltip would go off screen bottom, flip it up
            if (rect.bottom + 40 > window.innerHeight) {
                tooltip.style.top = "auto";
                tooltip.style.bottom = "0";
                tooltip.style.transform = "translateY(0)";
            } else {
                tooltip.style.top = "50%";
                tooltip.style.bottom = "auto";
                tooltip.style.transform = "translateY(-50%)";
            }
        });
    });
}

// ================= INIT ALL =================
document.addEventListener("DOMContentLoaded", () => {
    console.log("MAIN JS LOADED ✅");

    initUserDropdown();
    initScrollAnimation();
    initParallax();
    initSidebarCollapse();
    initHtmxListeners();
    initActiveNavLink();
    initTooltips();
    autoRemoveFlashMessages();
});
