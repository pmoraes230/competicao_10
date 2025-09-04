document.getElementById("textInput").addEventListener("input", function() {
    let textInput = this.value.toLowerCase()
    let cards = document.querySelectorAll(".cards")

    cards.forEach(card => {
        let nome = card.getAttribute("data-name")
        let cpf = card.getAttribute("data-cpf")

        if(nome.includes(textInput) || cpf.includes(textInput)) {
            card.style.display = "block"
        } else [
            card.style.display = "none"
        ]
    })
})