const usernameField = document.querySelector('#usernameField')
const feedBackArea = document.querySelector('.invalid_feedback')
const showPasswordToggle = document.querySelector('.showPasswordToggle')
const passwordField = document.querySelector('#passwordField')
const submitBtn = document.querySelector('.submit-btn')

const handleToggleInput = (e) => {
    if(showPasswordToggle.textContent === "MOSTRAR") {
        showPasswordToggle.textContent = "OCULTAR";
        passwordField.setAttribute('type', 'text');
    } else {
        showPasswordToggle.textContent = "MOSTRAR";
        passwordField.setAttribute('type', 'password');
    }
};

showPasswordToggle.addEventListener('click', handleToggleInput)

usernameField.addEventListener('keyup', (e) => {
    const usernameVal = e.target.value;

    usernameField.classList.remove("is-invalid");
    feedBackArea.style.display = 'none';

    if (usernameVal.length > 0) {
        fetch("/authentication/validate-username", {
            body: JSON.stringify({ username: usernameVal }), 
            method: "POST"
        })
            .then((res) => res.json())
            .then((data) => {
                if (data.username_error) {
                    submitBtn.disabled = true;
                    usernameField.classList.add("is-invalid");
                    feedBackArea.style.display = 'block';
                    feedBackArea.innerHTML=`<p>${data.username_error}</p>`
                } else {
                    submitBtn.removeAttribute('disabled');
                }
            });
    }
});
