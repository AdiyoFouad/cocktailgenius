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


function validateSignupForm() {
    var password = document.getElementById("password").value;
    var confirm_password = document.getElementById("confirm_password").value;
    var uppercaseRegex = /[A-Z]/;
    var numberRegex = /[0-9]/;
    
    // Check if passwords match
    if (password != confirm_password) {
        document.getElementById("password_match_error").style.display = "block";
        return false;
    }

    // Check password length
    if (password.length < 8) {
        alert("Password must be at least 8 characters long.");
        return false;
    }

    // Check for at least one uppercase letter
    if (!uppercaseRegex.test(password)) {
        alert("Password must contain at least one uppercase letter.");
        return false;
    }

    // Check for at least one digit
    if (!numberRegex.test(password)) {
        alert("Password must contain at least one digit.");
        return false;
    }

    return true;
}
