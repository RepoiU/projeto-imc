// ===== Captura do formulário =====
const form = document.getElementById("imcForm");
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
      // exemplo: 173 -> 1,73
      valor = valor[0] + "," + valor.slice(1);
    } else if (valor.length === 4) {
      // exemplo: 1850 -> 1,85 (desconsidera zero extra)
      valor = valor[0] + "," + valor.slice(1, 3);
    }
    inputAltura.value = valor;
  });
}

// ===== Peso =====
const inputPeso = document.getElementById("peso");
if (inputPeso) {
  inputPeso.addEventListener("blur", () => {
    let valor = inputPeso.value.replace(",", "."); // troca vírgula por ponto para número
    valor = parseFloat(valor);
    if (!isNaN(valor)) {
      inputPeso.value = valor.toFixed(2).replace(".", ","); // sempre 2 casas decimais com vírgula
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

    const res = await fetch(form.action, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    // >>> Correção do 302 Redirect <<<
    if (res.redirected) {
      window.location.href = res.url; // segue o redirecionamento do backend
    } else if (res.ok) {
      window.location.href = "/sucesso"; // fallback
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
