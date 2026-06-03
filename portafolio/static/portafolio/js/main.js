// Interacciones pequeñas del sistema. No consume la API de GitHub todavía.
document.addEventListener("DOMContentLoaded", () => {
    const navbar = document.querySelector(".os-navbar");
    const clock = document.querySelector("#system-clock");
    const links = document.querySelectorAll(".nav-link");

    const updateNavbar = () => {
        navbar.classList.toggle("is-scrolled", window.scrollY > 24);
    };

    const updateClock = () => {
        const time = new Intl.DateTimeFormat("es-BO", {
            timeZone: "America/La_Paz",
            hour: "2-digit",
            minute: "2-digit",
            second: "2-digit",
            hour12: false,
        }).format(new Date());

        clock.textContent = `${time} BOT`;
    };

    // Cierra el menú móvil después de seleccionar una sección.
    links.forEach((link) => {
        link.addEventListener("click", () => {
            const menu = document.querySelector("#navbarPortfolio");

            if (menu.classList.contains("show")) {
                bootstrap.Collapse.getOrCreateInstance(menu).hide();
            }
        });
    });

    updateNavbar();
    updateClock();
    window.addEventListener("scroll", updateNavbar, { passive: true });
    window.setInterval(updateClock, 1000);
});
