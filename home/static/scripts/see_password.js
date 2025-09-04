const campInput = document.getElementById("senha")
const btnEye = document.getElementById("btn_eye")
const imgEye = document.getElementById("eye")

btnEye.addEventListener("click", function() {
    if(campInput.type == "password") {
        campInput.type = "text"
        imgEye.src = "/static/icons/eye-slash.svg"
    } else {
        campInput.type = "password"
        imgEye.src = "/static/icons/eye.svg"
    }
})