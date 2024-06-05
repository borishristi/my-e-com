let produitBtn = document.getElementsByClassName('update-panier');

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
        })
}

for (let i = 0; i < produitBtn.length; i++) {
    produitBtn[i].addEventListener('click', function () {
        let produitId = this.dataset.produit;
        let action = this.dataset.action;

        if (user == 'AnonymousUser') {
            console.log('utilisateur anonyme');
        } else {
            updateUserCommande(produitId, action);
        }
    })
}

