function loadComponent(selector, url) {
    const element = document.querySelector(selector);
    if (!element) return;
    fetch(url)
        .then(response => response.text())
        .then(html => {
            element.innerHTML = html;
        })
        .catch(err => {
            console.error('Error loading', url, err);
        });
}

document.addEventListener('DOMContentLoaded', () => {
    loadComponent('#navbar-placeholder', 'navbar.html');
    loadComponent('#footer-placeholder', 'footer.html');
});
