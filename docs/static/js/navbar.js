/**
 * Função que deixa colorido o link da página ativa
 */
function activateLink() {
    let path = window.location.pathname;
    let page = path.split("/").pop();
    if (page.includes(".")) {
        page = page.substring(0, page.indexOf('.'));
    }
    let element = null;
    if (page.length === 0) {
        element = document.getElementById('nav-link-index');
    } else {
        element = document.getElementById('nav-link-' + page);
    }
    if (element != null) {
        element.classList.add('active');
        // element.style.color = 'var(--cor-principal)';
        // element.style.opacity = 0.9;
    }
}

activateLink();  // chama a função