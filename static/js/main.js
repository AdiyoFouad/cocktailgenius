function showText(element, text, interval) {
    var characters = text.split("");
    var i = 0;
    var timer = setInterval(function () {
        if (i < characters.length) {
            element.innerHTML += characters[i];
            i++;
        } else {
            clearInterval(timer);
        }
    }, interval);
}

// Récupérer l'élément de message de bienvenue
var welcomeMessage = document.getElementById("welcome-message-span");
showText(welcomeMessage, "CocktailGenius", 100);
// Définir une fonction pour afficher le texte lettre par lettre
function displayWelcomeMessage() {
    document.getElementById("welcome-message-span").innerText="";
    showText(welcomeMessage, "CocktailGenius", 100);
}
// Appeler displayWelcomeMessage toutes les 5 secondes
setInterval(displayWelcomeMessage, 3500);