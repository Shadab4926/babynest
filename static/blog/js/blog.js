document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle functionality
    const mobileMenuToggle = document.createElement('button');
    mobileMenuToggle.className = 'mobile-menu-toggle';
    mobileMenuToggle.innerHTML = '<i class="fas fa-bars"></i>';
    
    const header = document.querySelector('.blog-header .container');
    if (header) {
        header.prepend(mobileMenuToggle);
        
        const nav = document.querySelector('.blog-header nav');
        mobileMenuToggle.addEventListener('click', function() {
            nav.style.display = nav.style.display === 'flex' ? 'none' : 'flex';
        });
        
        // Close menu when clicking on a link
        document.querySelectorAll('.blog-header nav a').forEach(link => {
            link.addEventListener('click', function() {
                if (window.innerWidth <= 768) {
                    nav.style.display = 'none';
                }
            });
        });
        
        // Check screen size on resize
        window.addEventListener('resize', function() {
            if (window.innerWidth > 768) {
                nav.style.display = 'flex';
            } else {
                nav.style.display = 'none';
            }
        });
        
        // Initial check
        if (window.innerWidth <= 768) {
            nav.style.display = 'none';
        }
    }
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                window.scrollTo({
                    top: target.offsetTop - 80,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Newsletter form submission
    const newsletterForm = document.querySelector('.newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const emailInput = this.querySelector('input[type="email"]');
            if (emailInput.value) {
                alert('Thank you for subscribing to our newsletter!');
                emailInput.value = '';
            }
        });
    }
    
    // Add animation to post cards when they come into view
    const observerOptions = {
        threshold: 0.1
    };
    
    const observerCallback = (entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                observer.unobserve(entry.target);
            }
        });
    };
    
    const observer = new IntersectionObserver(observerCallback, observerOptions);
    
    document.querySelectorAll('.post-card, .featured-post').forEach(post => {
        post.style.opacity = '0';
        post.style.transform = 'translateY(20px)';
        post.style.transition = 'all 0.6s ease-out';
        observer.observe(post);
    });
    
    // Add this to your CSS:
    const style = document.createElement('style');
    style.textContent = `
        .animate-in {
            opacity: 1 !important;
            transform: translateY(0) !important;
        }
        
        .mobile-menu-toggle {
            display: none;
            background: none;
            border: none;
            font-size: 24px;
            color: var(--royal-purple);
            cursor: pointer;
            padding: 5px;
        }
        
        @media (max-width: 768px) {
            .mobile-menu-toggle {
                display: block;
                align-self: flex-start;
            }
            
            .blog-header nav {
                display: none;
                flex-direction: column;
                width: 100%;
                padding: 20px 0;
            }
        }
    `;
    document.head.appendChild(style);
});