(function () {
    var header = document.getElementById('header');
    var hero = document.querySelector('.freight-hero');
    if (!header || !hero) return;
    function updateHeader() {
        header.classList.toggle('alt', window.scrollY < hero.offsetHeight - header.offsetHeight);
    }
    window.addEventListener('scroll', updateHeader, { passive: true });
    updateHeader();
})();
