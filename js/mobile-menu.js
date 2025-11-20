/**
 * Mobile Menu Toggle
 */
(function() {
    'use strict';

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    function init() {
        const burger = document.querySelector('.header-burger');
        const mobileOverlay = document.querySelector('.header-menu');

        if (!burger || !mobileOverlay) return;

        burger.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            mobileOverlay.classList.toggle('header-menu--active');
            document.body.classList.toggle('header-menu-open');
        });

        document.addEventListener('click', function(e) {
            if (mobileOverlay.classList.contains('header-menu--active')) {
                if (!mobileOverlay.contains(e.target) && !burger.contains(e.target)) {
                    mobileOverlay.classList.remove('header-menu--active');
                    document.body.classList.remove('header-menu-open');
                }
            }
        });

        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && mobileOverlay.classList.contains('header-menu--active')) {
                mobileOverlay.classList.remove('header-menu--active');
                document.body.classList.remove('header-menu-open');
            }
        });
    }
})();
