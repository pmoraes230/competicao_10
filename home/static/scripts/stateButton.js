const campInput = document.getElementById("id_ticket")
const btn = document.getElementById("btn")

function stateButton() {
    if(campInput.value.trim() !== "") {
        btn.removeAttribute("disabled")
    } else {
        btn.setAttribute("disabled", "true")
    }
}

stateButton()
campInput.addEventListener("input", stateButton)