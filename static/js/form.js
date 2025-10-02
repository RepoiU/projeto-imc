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

  // Máscara para telefone no Brasil
  let maskTel;
  function aplicarMascaraTel() {
    if (maskTel) maskTel.destroy();
    if (iti.getSelectedCountryData().iso2 === "br") {
      maskTel = IMask(inputTel, { mask: "(00) 00000-0000" });
    }
  }
  inputTel.addEventListener("countrychange", aplicarMascaraTel);
  aplicarMascaraTel();

  // ===== Altura =====
  const inputAltura = document.getElementById("altura");
  if (inputAltura) {
    inputAltura.addEventListener("blur", () => {
      let valor = inputAltura.value.replace(/\D/g, ""); // só dígitos
      if (valor.length === 3) {
        valor = valor[0] + "," + valor.slice(1); // 173 -> 1,73
      } else if (valor.length === 4) {
        valor = valor[0] + "," + valor.slice(1, 3); // 1850 -> 1,85
      }
      inputAltura.value = valor;
    });
  }

  // ===== Peso =====
  const inputPeso = document.getElementById("peso");
  if (inputPeso) {
    inputPeso.addEventListener("blur", () => {
      let valor = inputPeso.value.replace(",", ".");
      valor = parseFloat(valor);
      if (!isNaN(valor)) {
        inputPeso.value = valor.toFixed(2).replace(".", ","); // sempre vírgula
      }
    });
  }

  // ===== Envio do formulário =====
  form.addEventListener("submit", async function (e) {
    e.preventDefault();

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
      };

      const res = await fetch(form.action || "/calculo", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });

      // Se o back já retorna HTML direto
      const contentType = res.headers.get("content-type");
      if (contentType && contentType.includes("text/html")) {
        const html = await res.text();
        document.open();
        document.write(html);
        document.close();
        return;
      }

      // Se é JSON e o back manda status
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
