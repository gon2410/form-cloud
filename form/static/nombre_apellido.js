// nombre
const usernameField = document.querySelector("#usernameField");
const usernameSuccessOutput = document.querySelector(".usernameSuccessOutput");
const feedBackArea = document.querySelector(".invalid_feedback");

// apellido
const lastnameField = document.querySelector("#lastnameField");
const lastnameSuccessOutput = document.querySelector(".lastnameSuccessOutput");
const lastfeedBackArea = document.querySelector(".last_invalid_feedback");

// boton de confirmacion
const submitBtn = document.querySelector("#boton_de_confirmacion");

usernameField.addEventListener("keyup", (e) => {
    e.preventDefault();

    const usernameVal = e.target.value;

    usernameField.classList.remove("is-invalid");
    submitBtn.removeAttribute("disabled");
    if (usernameVal.length > 0) {
        fetch("/validate-username", {
            body: JSON.stringify({ first_name: usernameVal }),
            method: "POST",
        })
            .then((res) => res.json())
            .then((data) => {
                // console.log("data", data)
                if (data.username_error) {
                    usernameField.classList.add("is-invalid");
                    submitBtn.disabled = true;
                }            
            });
    }
});

lastnameField.addEventListener("keyup", (e) => {
    e.preventDefault();

    const lastnameVal = e.target.value;

    lastnameField.classList.remove("is-invalid");
    submitBtn.removeAttribute("disabled");
    if (lastnameVal.length > 0) {
        fetch("/validate-lastname", {
            body: JSON.stringify({ last_name: lastnameVal }),
            method: "POST",
        })
            .then((res) => res.json())
            .then((data) => {
                // console.log("data", data)
                if (data.lastname_error) {
                    lastnameField.classList.add("is-invalid");
                    submitBtn.disabled = true;
                }
        
            });
    }
});

