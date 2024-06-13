window.addEventListener("DOMContentLoaded", e => {
    document.addEventListener("click", e => {
        const isDropdownButton = e.target.matches("[data-dropdown-button]");
        const isMenuButton = e.target.matches(".menu");
        const isOutsideNav = !e.target.closest('.bottom-nav-elements') &&
            document.querySelector('.bottom-nav').classList.contains('open');
        const overlay = document.querySelector('.overlay');

        let currentDropdown;
        if (isDropdownButton) {
            currentDropdown = e.target.closest('[data-dropdown-menu]');
            currentDropdown.classList.toggle('active');

            if (window.matchMedia("(max-width: 960px)").matches) {
                let dropdownMenu = currentDropdown.querySelector('.dropdown-menu');
                let switchIcon = currentDropdown.querySelector('.switch-icon')
                switchIcon.classList.toggle('active');

                if (currentDropdown.classList.contains('active')) {
                    let dropdownMenuHeight = dropdownMenu.offsetHeight + 18;
                    currentDropdown.style.marginBottom = dropdownMenuHeight + 'px';
                } else {
                    currentDropdown.style.marginBottom = '0px';
                }

                currentDropdown.style.transition = "margin-bottom 150ms ease-in-out";
            }
        }

        if (window.matchMedia("(max-width: 960px)").matches) {
            if (isMenuButton) {
                document.querySelector('.bottom-nav').classList.toggle('open');
                overlay.style.display = document.querySelector('.bottom-nav').classList.contains('open') ? 'block' : 'none';
            }

            if (isOutsideNav) {
                document.querySelector('.bottom-nav').classList.remove('open');
                overlay.style.display = 'none';
            }
        }

        if (window.matchMedia("(min-width: 960px)").matches) {
            document.querySelectorAll("[data-dropdown-menu].active").forEach(dropdown => {
                if (dropdown === currentDropdown) return;
                dropdown.classList.remove('active')
            })
        }
    })
});