// ================= DOM READY =================
document.addEventListener("DOMContentLoaded", () => {

    console.log("JS LOADED ✅");

    // ================= MOBILE MENU =================
    const btn = document.getElementById("menuBtn");
    const menu = document.getElementById("mobileMenu");

    if (btn && menu) {
        btn.addEventListener("click", () => {
            menu.classList.toggle("hidden");
        });
    }

    // ================= SCROLL ANIMATION =================
    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("show");
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.2
    });

    document.querySelectorAll('.fade-up, .stagger').forEach(el => {
        observer.observe(el);
    });

});


// ================= PARALLAX =================
window.addEventListener("scroll", () => {
    const elements = document.querySelectorAll(".parallax");

    elements.forEach(el => {
        const speed = el.getAttribute("data-speed") || 0.3;
        const y = window.scrollY * speed;

        el.style.transform = `translateY(${y}px)`;
    });
});
