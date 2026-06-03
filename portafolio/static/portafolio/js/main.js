// Interacciones pequeñas del sistema. No consume la API de GitHub todavía.
document.addEventListener("DOMContentLoaded", () => {
    const navbar = document.querySelector(".os-navbar");
    const clock = document.querySelector("#system-clock");
    const links = document.querySelectorAll(".nav-link");
    const previewModalElement = document.getElementById("imagePreviewModal");
    const previewImage = document.getElementById("imagePreviewModalImg");
    const previewTitle = document.getElementById("imagePreviewModalTitle");
    const carouselImages = document.querySelectorAll(".project-carousel-img");

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

            if (menu && menu.classList.contains("show") && window.bootstrap) {
                window.bootstrap.Collapse.getOrCreateInstance(menu).hide();
            }
        });
    });

    if (previewModalElement && previewImage && previewTitle && window.bootstrap) {
        const previewModal = new window.bootstrap.Modal(previewModalElement);

        carouselImages.forEach((image) => {
            image.addEventListener("click", () => {
                const fullImage = image.dataset.fullImage;
                const imageTitle = image.dataset.imageTitle || "Vista previa del proyecto";

                if (!fullImage) {
                    return;
                }

                previewImage.src = fullImage;
                previewImage.alt = imageTitle;
                previewTitle.textContent = imageTitle;
                previewModal.show();
            });
        });

        previewModalElement.addEventListener("hidden.bs.modal", () => {
            previewImage.src = "";
            previewImage.alt = "Vista ampliada del proyecto";
        });
    }

    updateNavbar();
    updateClock();
    window.addEventListener("scroll", updateNavbar, { passive: true });
    window.setInterval(updateClock, 1000);
});
