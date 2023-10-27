// Get the current URL or page name
const currentPage = window.location.pathname;

// Find the corresponding breadcrumb link and highlight it
document.querySelectorAll('.breadcrumbs a').forEach(link => {
    if (link.getAttribute('href') === currentPage) {
        link.classList.add('current-page');
    }
});
