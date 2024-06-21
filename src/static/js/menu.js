let logo_div = document.getElementById('logo_div');
// let search_div = document.getElementById('search_div');
let search_div = document.querySelector('#search_div')
let menu_div = document.getElementById('menu_div');
let logo_user = document.getElementById('logo_user');
let logo_user_link = document.getElementById('logo_user_link');
let mon_panier = document.getElementById('mon_panier');
let btn_sidebar = document.querySelector('.btn-sidebar');


// search_div.className = 'd-none';

if (user == 'AnonymousUser') {
    logo_user.className = 'fa-solid fa-right-to-bracket fa-xl pb-0 mt-3';
    mon_panier.innerText = 'Connexion';
    mon_panier.style.float = 'center';
    mon_panier.style.marginLeft = '7px';
    logo_user_link.className = 'px-0 pt-2 px-lg-4 position-relative';
    logo_user_link.style.textDecoration = 'none';
} else {
    logo_user.className = 'fa-solid fa-user-check fa-xl pb-0 mt-3';
    logo_user_link.className = 'px-2 pt-2 px-lg-4 position-relative';
}

btn_sidebar.addEventListener("mouseover", () => {
    btn_sidebar.style.color = "black";
})