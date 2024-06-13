window.addEventListener("DOMContentLoaded", e => {
    const input = document.querySelector('input[type="password"]');
    const label = document.querySelector('label[for="password"]');
    const passwordBox = document.querySelector('.password-elements');
    const button = document.querySelector('.toggle-password');

    input.addEventListener("focus", e => {
        let formElement = input.closest('.form-element');
        if (!formElement.classList.contains('error')) {
            label.style.color = "#555555";
            button.style.color = "#555555";
            passwordBox.style.borderColor = "#555555";
        }
    });

    input.addEventListener("blur", e => {
        let formElement = input.closest('.form-element');
        if (!formElement.classList.contains('error')) {
            label.style.color = "";
            button.style.color = "";
            passwordBox.style.borderColor = "";
        }
    });

    document.addEventListener("click", e => {
        const isShowButton = e.target.matches(".toggle-password");
        if (isShowButton) {
            if (input.type === "password") {
                input.type = "text";
                button.innerText = "ukryj";
            } else {
                input.type = "password";
                button.innerText = "pokaż";
            }
        }
    });
});