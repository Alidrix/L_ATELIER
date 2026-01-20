const form = document.getElementById("login-form");
const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");
const togglePassword = document.getElementById("toggle-password");
const submitButton = document.getElementById("submit");
const statusText = document.getElementById("form-status");
const confirmation = document.getElementById("confirmation");
const backHome = document.getElementById("back-home");

const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function updateFormState() {
  const isEmailValid = emailRegex.test(emailInput.value.trim());
  passwordInput.disabled = !isEmailValid;
  togglePassword.disabled = !isEmailValid;
  const isPasswordValid = passwordInput.value.trim().length > 0;
  submitButton.disabled = !(isEmailValid && isPasswordValid);
}

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

    confirmation.hidden = false;
    backHome.hidden = true;

    setTimeout(() => {
      backHome.hidden = false;
    }, 2000);
  } catch (error) {
    statusText.textContent = error.message;
  } finally {
    submitButton.classList.remove("loading");
    updateFormState();
  }
});

backHome.addEventListener("click", () => {
  confirmation.hidden = true;
  form.reset();
  passwordInput.type = "password";
  togglePassword.textContent = "Afficher";
  statusText.textContent = "";
  updateFormState();
});

updateFormState();
