// Loader animation: fade out when page is fully loaded
window.addEventListener('load', function () {
    var loader = document.getElementById('loader');
    if (loader) {
        loader.style.opacity = 0;
        setTimeout(function () {
            loader.style.display = 'none';
        }, 500);
    }
});

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener('click', function (e) {
        var targetId = this.getAttribute('href').substring(1);
        var targetEl = document.getElementById(targetId);
        if (targetEl) {
            e.preventDefault();
            window.scrollTo({
                top: targetEl.offsetTop - 60,
                behavior: 'smooth'
            });
        }
    });
});

// Portfolio filter functionality
window.addEventListener('DOMContentLoaded', function () {
    var filterBtns = document.querySelectorAll('.filter-btn');
    var cards = document.querySelectorAll('.project-card');
    filterBtns.forEach(function(btn){
        btn.addEventListener('click', function(){
            // Remove active from all
            filterBtns.forEach(function(b){ b.classList.remove('active'); });
            btn.classList.add('active');
            var category = btn.getAttribute('data-category');
            cards.forEach(function(card){
                if (category === "All" || card.getAttribute('data-category') === category) {
                    card.style.display = 'flex';
                    card.classList.add('fade-in');
                } else {
                    card.style.display = 'none';
                    card.classList.remove('fade-in');
                }
            });
        });
    });
    // Trigger default "All" filter
    var allBtn = document.querySelector('.filter-btn[data-category="All"]');
    if (allBtn) allBtn.click();
});

// Subtle fade for portfolio cards
var style = document.createElement('style');
style.innerHTML = `
.project-card.fade-in { 
    animation: fadeInMoveUp 0.7s cubic-bezier(.52,.7,.22,.89);
}
`;
document.head.appendChild(style);


