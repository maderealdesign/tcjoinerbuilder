document.addEventListener('DOMContentLoaded', () => {
    fetch('menu.html')
        .then(response => response.text())
        .then(data => {
            document.getElementById('menu-placeholder').innerHTML = data;
            
            // Highlight active link logic
            const currentPath = window.location.pathname.split('/').pop() || 'index.html';
            const navLinks = document.querySelectorAll('.nav-link');
            
            navLinks.forEach(link => {
                const href = link.getAttribute('href');
                if (href && currentPath.includes(href) && href !== '#') {
                    link.classList.add('text-brand-accent');
                    link.classList.remove('text-white');
                }
            });

            // Mobile Menu Toggle Logic
            const btn = document.getElementById('mobile-menu-btn');
            const menu = document.getElementById('mobile-menu');

            if (btn && menu) {
                btn.addEventListener('click', () => {
                    if (menu.style.maxHeight) {
                        menu.style.maxHeight = null;
                    } else {
                        menu.style.maxHeight = menu.scrollHeight + "px";
                    }
                });
            }
        })
        .catch(error => console.error('Error loading navigation:', error));
});