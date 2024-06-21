const allStars = document.querySelectorAll(".fa-star");
const rating = document.querySelector('.rating');

console.log("allstars", allStars);

init();

function init() {
    allStars.forEach(star => {
        star.addEventListener("click", saveRating);
        star.addEventListener("mouseover", addCSS);
        star.addEventListener("mouseout", removeCSS);
    });
}

function saveRating(e) {
    // console.log(e, e.target);
    // console.dir(e.target);
    // console.log(e.target.dataset, e.target.nodeName, e.target.nodeType);
    removeEventListenerToAllStars();
    rating.textContent = e.target.dataset.star;
}

function removeEventListenerToAllStars() {
    allStars.forEach(star => {
        star.removeEventListener('click', saveRating);
        star.removeEventListener('mouseover', addCSS);
        star.removeEventListener('mouseout', removeCSS);
    })
}

function addCSS(e, css = "star-checked") {
    // e.target.classList.add(css);
    const overedStar = e.target;
    overedStar.classList.add(css);
    const previousSiblings = getPreviousSliblings(overedStar);
    console.log("previousSiblings", previousSiblings);
    previousSiblings.forEach((elem) => elem.classList.add(css));
}

function removeCSS(e, css = "star-checked") {
    // e.target.classList.remove(css);
    const overedStar = e.target;
    overedStar.classList.remove(css);
    const previousSiblings = getPreviousSliblings((overedStar));
    previousSiblings.forEach((elem) => elem.classList.remove(css));
}

function getPreviousSliblings(elem) {
    console.log("elem.previousSibling", elem.previousSibling);
    let siblings = [];
    const iNodeType = 1;
    while (elem = elem.previousSibling) {
        if (elem.nodeType === iNodeType) {
            siblings = [elem, ...siblings];
        }
    }
    return siblings;
}