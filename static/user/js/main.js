/*=============== SHOW MENU ===============*/
const navMenu = document.getElementById('nav-menu'),
    navToggle = document.getElementById('nav-toggle'),
    navClose = document.getElementById('nav-close');

/*===== Menu Show =====*/
/* Validate if constant exists */
if (navToggle) {
    navToggle.addEventListener('click', () => {
        navMenu.classList.add('show-menu');
    })
}

/*===== Hide Show =====*/
/* Validate if constant exists */
if (navClose) {
    navClose.addEventListener('click', () => {
        navMenu.classList.remove('show-menu')
    })
}

/*=============== IMAGE GALLERY ===============*/
function imgGallery() {
    const mainImg = document.querySelector('.details__img'),
        smallImg = document.querySelectorAll('.details__small-img');

    smallImg.forEach((img) => {
        img.addEventListener('click', function () {
            mainImg.src = this.src;
        })
    })
}

imgGallery();

/*=============== SWIPER CATEGORIES ===============*/

var swiperCategories = new Swiper('.categories__container', {
    spaceBetween: 24,

    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
    },
    breakpoints: {
        350: {
            slidesPerView: 2,
            spaceBetween: 24,
        },
        768: {
            slidesPerView: 3,
            spaceBetween: 24,
        },
        992: {
            slidesPerView: 4,
            spaceBetween: 24,
        },
        1200: {
            slidesPerView: 5,
            spaceBetween: 24,
        },
        1400: {
            slidesPerView: 6,
            spaceBetween: 24,
        }
    }
})

var swiper = new Swiper('.home-slider', {
    loop: true,
    spaceBetween: 24,
})

/*=============== SWIPER PRODUCTS ===============*/

var swiperProducts = new Swiper('.new__container', {
    spaceBetween: 24,
    loop: true,

    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
    },
    breakpoints: {
        768: {
            slidesPerView: 2,
            spaceBetween: 24,
        },
        992: {
            slidesPerView: 3,
            spaceBetween: 24,
        },
        1400: {
            slidesPerView: 4,
            spaceBetween: 24,
        }
    }
})

/*=============== PRODUCTS TABS ===============*/
const tabs = document.querySelectorAll('[data-target]'),
    tabContents = document.querySelectorAll('[content]');

tabs.forEach((tab) => {
    tab.addEventListener('click', () => {
        const target = document.querySelector(tab.dataset.target);
        tabContents.forEach((tabContent) => {
            tabContent.classList.remove('active-tab')
        });

        target.classList.add('active-tab');

        tabs.forEach((tab) => {
            tab.classList.remove('active-tab')
        });

        tab.classList.add('active-tab')
    })
})

/* =============== STICKY SCROLL ===============*/

document.addEventListener("DOMContentLoaded", () => {
    const headerTop = document.querySelector(".header__top");
    const nav = document.querySelector(".nav")
    let lastScrollY = window.scrollY;

    window.addEventListener("scroll", () => {
        if (window.scrollY > lastScrollY) {
            headerTop.classList.add("hidden"); // Hide header__top on scroll down
            nav.classList.add("shadow");
        } else {
            headerTop.classList.remove("hidden"); // Show header__top on scroll up
            nav.classList.remove("shadow");
        }
        lastScrollY = window.scrollY;
    });
});

/* =============== SCROLL TO TOP ===============*/
// Scroll event listener
window.addEventListener('scroll', function () {
    const scrollToTopButton = document.getElementById('scrollToTop');
    if (window.scrollY > 300) {
        scrollToTopButton.style.display = 'block';
    } else {
        scrollToTopButton.style.display = 'none';
    }
});

// Scroll-to-top action
document.getElementById('scrollToTop').addEventListener('click', function (e) {
    e.preventDefault();
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});

/* =============== ACCOUNT TAB ===============*/
document.addEventListener('DOMContentLoaded', () => {
    const tabs = document.querySelectorAll('.account__tab');
    const contents = document.querySelectorAll('.tab__content');

    // Get the saved active tab from localStorage
    const savedTab = localStorage.getItem('activeTab');
    if (savedTab) {
        // Activate the saved tab
        tabs.forEach(tab => {
            if (tab.dataset.target === savedTab) {
                tab.classList.add('active-tab');
            } else {
                tab.classList.remove('active-tab');
            }
        });

        // Show the corresponding content
        contents.forEach(content => {
            if (content.id === savedTab.substring(1)) {
                content.classList.add('active-tab');
            } else {
                content.classList.remove('active-tab');
            }
        });
    }

    // Add click event listeners to tabs
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // Remove active class from all tabs and contents
            tabs.forEach(tab => tab.classList.remove('active-tab'));
            contents.forEach(content => content.classList.remove('active-tab'));

            // Add active class to clicked tab and corresponding content
            tab.classList.add('active-tab');
            const target = tab.dataset.target;
            document.querySelector(target).classList.add('active-tab');

            // Save the active tab in localStorage
            localStorage.setItem('activeTab', target);
        });
    });
});
/* =============== COMPARE ===============*/

/* =============== COMPARE ===============*/

/* =============== COMPARE ===============*/

/* =============== COMPARE ===============*/

/* =============== COMPARE ===============*/

/* =============== COMPARE ===============*/

/* =============== COMPARE ===============*/

/* =============== COMPARE ===============*/

/* =============== COMPARE ===============*/
