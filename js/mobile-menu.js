/**
 * Mobile Menu Toggle
 * Simple vanilla JavaScript for mobile navigation
 */

(function() {
    'use strict';

    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    function init() {
        const burger = document.querySelector('.header-burger');
        const mobileOverlay = document.querySelector('.header-menu');
        const body = document.body;

        if (!burger || !mobileOverlay) {
            console.log('Mobile menu elements not found');
            return;
        }

        // Toggle menu on burger click
        burger.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            toggleMenu();
        });

        // Close menu when clicking outside
        document.addEventListener('click', function(e) {
            if (mobileOverlay.classList.contains('header-menu--active')) {
                if (!mobileOverlay.contains(e.target) && !burger.contains(e.target)) {
                    closeMenu();
                }
            }
        });

        // Close menu on escape key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && mobileOverlay.classList.contains('header-menu--active')) {
                closeMenu();
            }
        });

        // Handle window resize - close menu if switching to desktop
        let resizeTimer;
        window.addEventListener('resize', function() {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(function() {
                if (window.innerWidth > 768 && mobileOverlay.classList.contains('header-menu--active')) {
                    closeMenu();
                }
            }, 250);
        });
    }

    function toggleMenu() {
        const mobileOverlay = document.querySelector('.header-menu');
        const body = document.body;

        if (mobileOverlay.classList.contains('header-menu--active')) {
            closeMenu();
        } else {
            openMenu();
        }
    }

    function openMenu() {
        const mobileOverlay = document.querySelector('.header-menu');
        const body = document.body;

        mobileOverlay.classList.add('header-menu--active');
        body.classList.add('header-menu-open');
    }

    function closeMenu() {
        const mobileOverlay = document.querySelector('.header-menu');
        const body = document.body;

        mobileOverlay.classList.remove('header-menu--active');
        body.classList.remove('header-menu-open');
    }

})();
