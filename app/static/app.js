const form = document.getElementById("login-form");
const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");
const togglePassword = document.getElementById("toggle-password");
const submitButton = document.getElementById("submit");
const statusText = document.getElementById("form-status");
const resultsTable = document.querySelector(".table table");

const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function updateFormState() {
  const isEmailValid = emailRegex.test(emailInput.value.trim());
  passwordInput.disabled = !isEmailValid;
  togglePassword.disabled = !isEmailValid;
  const isPasswordValid = passwordInput.value.trim().length > 0;
  submitButton.disabled = !(isEmailValid && isPasswordValid);
}

if (form) {
  emailInput.addEventListener("input", () => {
    updateFormState();
    statusText.textContent = emailRegex.test(emailInput.value.trim())
      ? ""
      : "Veuillez saisir un email valide pour déverrouiller le mot de passe.";
  });

  passwordInput.addEventListener("input", updateFormState);

  togglePassword.addEventListener("click", () => {
    const isHidden = passwordInput.type === "password";
    passwordInput.type = isHidden ? "text" : "password";
    togglePassword.textContent = isHidden ? "Masquer" : "Afficher";
  });

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    statusText.textContent = "";
    submitButton.classList.add("loading");
    submitButton.disabled = true;

    const payload = {
      email: emailInput.value.trim(),
      password: passwordInput.value.trim(),
    };

    try {
      const response = await fetch("/api/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.message || "Erreur lors de l'envoi.");
      }

    } catch (error) {
      statusText.textContent = error.message;
    } finally {
      submitButton.classList.remove("loading");
      updateFormState();
    }
  });
}

function toggleMaskedValue(target, button) {
  const isHidden = target.dataset.state !== "visible";
  target.textContent = isHidden ? target.dataset.value : "••••••••••";
  target.dataset.state = isHidden ? "visible" : "hidden";
  button.textContent = isHidden ? "Masquer" : button.dataset.label;
}

if (resultsTable) {
  resultsTable.addEventListener("click", (event) => {
    const button = event.target.closest("[data-toggle]");
    if (!button) {
      return;
    }
    const toggleType = button.dataset.toggle;
    const row = button.closest("tr");
    const cells = row ? row.querySelectorAll(".maskable") : null;
    if (!cells || cells.length < 2) {
      return;
    }
    if (toggleType === "email") {
      toggleMaskedValue(cells[0], button);
    }
    if (toggleType === "password") {
      toggleMaskedValue(cells[1], button);
    }
  });

  resultsTable.querySelectorAll("[data-toggle]").forEach((button) => {
    const label =
      button.dataset.toggle === "email"
        ? "Afficher email"
        : "Afficher mot de passe";
    button.dataset.label = label;
  });
}

if (form) {
  updateFormState();
}
