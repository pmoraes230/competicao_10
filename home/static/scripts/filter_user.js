document.getElementById("textInput").addEventListener("input", function() {
    let textInput = this.value.toLowerCase()
    let cards = document.querySelectorAll(".cards")

    cards.forEach(card => {
        let nome = card.getAttribute("data-name")
        let email = card.getAttribute("data-email")

        if(nome.includes(textInput) || email.includes(textInput)) {
            card.style.display = "block"
        } else [
            card.style.display = "none"
        ]
    })
})