// form.js

document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("form-imc") || document.getElementById("imcForm");
  if (!form) return;

  const submitBtn = form.querySelector("button[type=submit]");
  const inputTel = document.querySelector("#telefone");

  // ===== Telefone com intl-tel-input =====
  const iti = window.intlTelInput(inputTel, {
    initialCountry: "br",
    preferredCountries: ["br", "us", "pt"],
    separateDialCode: true,
    utilsScript:
      "https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/17.0.19/js/utils.js",
  });

  // ===== Máscara para telefone =====
  let maskTel;
  function aplicarMascaraTel() {
    if (maskTel) maskTel.destroy();
    if (iti.getSelectedCountryData().iso2 === "br") {
      maskTel = IMask(inputTel, { mask: "(00) 00000-0000" });
    }
  }
  inputTel.addEventListener("countrychange", aplicarMascaraTel);
  aplicarMascaraTel();

  // ===== Altura (X,XX) =====
  const inputAltura = document.getElementById("altura");
  if (inputAltura) {
    inputAltura.setAttribute("inputmode", "numeric");
    inputAltura.setAttribute("pattern", "[0-9,]*");

    inputAltura.addEventListener("input", () => {
      let valor = inputAltura.value.replace(/\D/g, "");
      if (valor.length > 3) valor = valor.slice(0, 3);
      if (valor.length >= 2) {
        valor = valor[0] + "," + valor.slice(1, 3);
      } else if (valor.length === 1) {
        valor = valor[0] + ",";
      }
      inputAltura.value = valor;
    });
  }

  // ===== Peso (XXX,XX) =====
  const inputPeso = document.getElementById("peso");
  if (inputPeso) {
    inputPeso.setAttribute("inputmode", "numeric");
    inputPeso.setAttribute("pattern", "[0-9,]*");

    inputPeso.addEventListener("input", () => {
      let valor = inputPeso.value.replace(/\D/g, "");
      if (valor.length > 5) valor = valor.slice(0, 5);
      if (valor.length > 2) {
        valor = valor.slice(0, valor.length - 2) + "," + valor.slice(-2);
      }
      inputPeso.value = valor;
    });
  }

  // ===== Envio do formulário =====
  form.addEventListener("submit", async function (e) {
    e.preventDefault();

    // 🧩 Captura o token do reCAPTCHA gerado automaticamente
    const recaptchaField = document.querySelector("#g-recaptcha-response");
    const recaptchaToken = recaptchaField ? recaptchaField.value.trim() : "";

    if (!recaptchaToken) {
      alert("⚠️ Por favor, confirme que você não é um robô antes de enviar.");
      return;
    }

    // Validação de altura e peso
    const alturaVal = parseFloat((form.altura.value || "0").replace(",", "."));
    const pesoVal = parseFloat((form.peso.value || "0").replace(",", "."));

    if (isNaN(alturaVal) || alturaVal < 1.0) {
      alert("⚠️ Altura inválida! Insira um valor a partir de 1,00 m.");
      return;
    }

    if (isNaN(pesoVal) || pesoVal < 20.0) {
      alert("⚠️ Peso inválido! Insira um valor a partir de 20 kg.");
      return;
    }

    // ===== Envio =====
    submitBtn.disabled = true;
    const originalText = submitBtn.textContent;
    submitBtn.textContent = "Enviando...";

    try {
      const data = {
        nome: form.nome.value.trim(),
        sobrenome: form.sobrenome.value.trim(),
        cidade: form.cidade.value.trim(),
        email: form.email.value.trim(),
        numero: iti ? iti.getNumber() : form.numero.value.trim(),
        altura: form.altura.value.trim().replace(",", "."),
        peso: form.peso.value.trim().replace(",", "."),
        "g-recaptcha-response": recaptchaToken, // ✅ token enviado ao backend
      };

      const res = await fetch(form.action || "/calculo", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });

      const contentType = res.headers.get("content-type");

      if (contentType && contentType.includes("text/html")) {
        const html = await res.text();
        document.open();
        document.write(html);
        document.close();
        return;
      }

      if (res.redirected) {
        window.location.href = res.url;
      } else if (res.ok) {
        window.location.href = "/sucesso";
      } else {
        const err = await res.json().catch(() => ({}));
        alert("Erro ao enviar: " + (err.mensagem || res.status));
      }
    } catch (err) {
      console.error("Erro ao enviar:", err);
      alert("Erro ao enviar o formulário.");
    } finally {
      submitBtn.disabled = false;
      submitBtn.textContent = originalText;
    }
  });
});
