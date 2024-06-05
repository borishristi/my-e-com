//On récupère tous les éléments qui ont la classe updtate-panier
let produitBtn = document.getElementsByClassName('update-panier');

//Cette fonction permet de mettre à jour les éléments de la page
function updateUserCommande(produit, action) {
    let url = "/update_article/"

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({'produit_id': produit, 'action': action})
    })
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            console.log('data', data)
            // Pour recharger la page
            location.reload()
        })
}

//On parcourt la variable produitBtn et on applique un évènement à chaque parcours
for (let i = 0; i < produitBtn.length; i++) {
    produitBtn[i].addEventListener('click', function () {
        //On récupère l'id du produit de chaque ligne et l'action liée au bouton
        let produitId = this.dataset.produit;
        let action = this.dataset.action;

        //Si l'utilisateur n'est pas connecté on effectue une opération dans le cas contraire,
        //on appelle la fonction de mise à jour du produit.
        if (user == 'AnonymousUser') {
            console.log('utilisateur anonyme');
        } else {
            updateUserCommande(produitId, action);
        }
    })
}

