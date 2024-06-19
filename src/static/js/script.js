// data - produit = "{{ produit.id }}
let link_cat = document.getElementsByClassName('link-cat');
let text_cat = document.getElementsByClassName('text-cat');

for (let i = 0; i < produitBtn.length; i++) {
    produitBtn[i].addEventListener('click', function () {
        //On récupère l'id du produit de chaque ligne et l'action liée au bouton
        let produitId = this.dataset.produit;
        let action = this.dataset.action;

        //Si l'utilisateur n'est pas connecté on effectue une opération dans le cas contraire,
        //on appelle la fonction de mise à jour du produit.
        if (user == 'AnonymousUser') {
            addCookieArticle(produitId, action);
        } else {
            updateUserCommande(produitId, action);
        }
    })
}

link_cat.addEventListener('mouseon', () => {
    // link_cat.style.display = 'none';
    text_cat.style.color = 'red';
})