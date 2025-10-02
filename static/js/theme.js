document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.getElementById('toggle-theme');
  const body = document.body;
  const logo = document.getElementById('logo');

  // Carrega tema salvo
  if (localStorage.getItem('theme') === 'dark') {
    body.classList.add('dark-mode');
    logo.src = "/static/img/novatra_logo_white.png";
    toggle.checked = true;
  } else {
    logo.src = "/static/img/novatra_logo_black.png";
  }

  // Alterna entre claro/escuro
  toggle.addEventListener('change', () => {
    if (toggle.checked) {
      body.classList.add('dark-mode');
      logo.src = "/static/img/novatra_logo_white.png";
      localStorage.setItem('theme', 'dark');
    } else {
      body.classList.remove('dark-mode');
      logo.src = "/static/img/novatra_logo_black.png";
      localStorage.setItem('theme', 'light');
    }
  });
});
