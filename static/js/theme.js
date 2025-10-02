// theme.js

document.addEventListener("DOMContentLoaded", function () {
  const body = document.body;
  const toggle = document.getElementById("toggle-theme");
  const logo = document.getElementById("logo");

  // ==== Carrega tema salvo ====
  const savedTheme = localStorage.getItem("theme") || "light";
  if (savedTheme === "dark") {
    body.classList.add("dark");
    if (toggle) toggle.checked = true;
    if (logo) logo.src = "/static/img/novatra_logo_white.png";
  } else {
    if (logo) logo.src = "/static/img/novatra_logo_black.png";
  }

  // ==== Alterna tema ====
  if (toggle) {
    toggle.addEventListener("change", () => {
      if (toggle.checked) {
        body.classList.add("dark");
        localStorage.setItem("theme", "dark");
        if (logo) logo.src = "/static/img/novatra_logo_white.png";
      } else {
        body.classList.remove("dark");
        localStorage.setItem("theme", "light");
        if (logo) logo.src = "/static/img/novatra_logo_black.png";
      }
    });
  }
});

