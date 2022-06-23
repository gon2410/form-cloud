// campo de la contraseña
const passwd = document.querySelector("#passwordField")

// boton de descarga
const excelSubmit = document.querySelector("#excel-download")

excelSubmit.disabled = true;
passwd.addEventListener("keyup", (e) => {
    const passwordVal = e.target.value;

    passwd.classList.remove("is-invalid");
    passwd.classList.remove("is-valid");
    

    if (passwordVal.length > 0) {
        fetch("/validate-password", {
            body: JSON.stringify({ password: passwordVal }),
            method: "POST",
        })
            .then((res) => res.json())
            .then((data) => {
                if (data.password_error) {
                    passwd.classList.add("is-invalid");
                    excelSubmit.disabled = true;
                } else {
                    passwd.classList.remove("is-invalid")
                    passwd.classList.add("is-valid")
                    excelSubmit.removeAttribute("disabled");
                }
            })
    } else {
        excelSubmit.disabled = true;
    }
});