/* Page-specific behaviour. Bootstrap handles tabs, navigation and the FAQ. */

// Show every category together, or return to Bootstrap’s regular tab view.
const menuPanels = document.querySelector('#menu-panels');
const menuTabs = [...document.querySelectorAll('#menu-tabs [data-bs-toggle="pill"]')];
const allMenuButton = document.querySelector('#all-menu');

function leaveAllMenu() {
  menuPanels.classList.remove('all-menu-open');
  allMenuButton.innerHTML = 'Afficher tout le menu <span>+</span>';
  allMenuButton.setAttribute('aria-expanded', 'false');
}

menuTabs.forEach(tab => tab.addEventListener('show.bs.tab', leaveAllMenu));
allMenuButton.setAttribute('aria-expanded', 'false');
allMenuButton.addEventListener('click', () => {
  if (menuPanels.classList.contains('all-menu-open')) {
    leaveAllMenu();
    bootstrap.Tab.getOrCreateInstance(menuTabs[0]).show();
    return;
  }
  menuPanels.classList.add('all-menu-open');
  menuTabs.forEach(tab => {
    tab.classList.remove('active');
    tab.setAttribute('aria-selected', 'false');
  });
  menuPanels.querySelectorAll('.tab-pane').forEach(panel => panel.classList.remove('active', 'show'));
  allMenuButton.innerHTML = 'Revenir aux catégories <span>−</span>';
  allMenuButton.setAttribute('aria-expanded', 'true');
});

// Close Bootstrap’s mobile navigation after selecting an anchor link.
const mainNav = document.querySelector('#main-nav');
mainNav.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {
  const collapse = bootstrap.Collapse.getOrCreateInstance(mainNav, { toggle: false });
  if (mainNav.classList.contains('show')) {
    collapse.hide();
  } else if (mainNav.classList.contains('collapsing') &&
             document.querySelector('.navbar-toggler').getAttribute('aria-expanded') === 'true') {
    // A quick tap may arrive before Bootstrap finishes opening the menu.
    mainNav.addEventListener('shown.bs.collapse', () => collapse.hide(), { once: true });
  }
}));

// Automatic animation preference; no floating animation control.
const chefImages = [...document.querySelectorAll('[data-chef-animated]')];
const motionPreference = matchMedia('(prefers-reduced-motion: reduce)');
function updateChefMotion() {
  chefImages.forEach(img => img.src = motionPreference.matches
    ? img.dataset.chefStill : img.dataset.chefAnimated);
}
motionPreference.addEventListener('change', updateChefMotion);
updateChefMotion();

document.querySelector('#year').textContent = new Date().getFullYear();

// Fast, once-only reveals. Content stays visible without JavaScript or animation support.
const revealElements = [];
function prepareReveal(selector, type = '', stagger = false) {
  document.querySelectorAll(selector).forEach((element, index) => {
    if (revealElements.includes(element)) return;
    revealElements.push(element);
    element.classList.add('reveal-ready');
    if (type) element.classList.add(type);
    if (stagger) element.style.setProperty('--reveal-delay', `${(index % 3) * 55}ms`);
  });
}

if ('IntersectionObserver' in window && !motionPreference.matches) {
  prepareReveal('h1, h2, h3, .closing p', 'reveal-heading');
  prepareReveal('.award', 'reveal-seal', true);
  prepareReveal('.photo-frame, .story-photo, .video-card, .visit-photo, .visit-details');
  prepareReveal('.menu-item', '', true);
  const revealObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('is-revealed');
      revealObserver.unobserve(entry.target);
    });
  }, { threshold: .08, rootMargin: '0px 0px -20px 0px' });
  revealElements.forEach(element => revealObserver.observe(element));

  // Keyboard focus must never land on a visually hidden card or link.
  document.addEventListener('focusin', event => {
    const element = event.target.closest('.reveal-ready');
    if (element) {
      element.classList.add('is-revealed');
      revealObserver.unobserve(element);
    }
  });
  motionPreference.addEventListener('change', event => {
    if (event.matches) {
      revealElements.forEach(element => element.classList.add('is-revealed'));
      revealObserver.disconnect();
    }
  });
}
