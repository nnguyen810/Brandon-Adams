(function () {
  const contactForm = document.getElementById("contact-form");
  const formStatus = document.getElementById("form-status");
  const CONTACT_API_URL = window.CONTACT_API_URL || "";
  const EMAILJS_PUBLIC_KEY = window.EMAILJS_PUBLIC_KEY || "";
  const EMAILJS_SERVICE_ID = window.EMAILJS_SERVICE_ID || "";
  const EMAILJS_TEMPLATE_ID = window.EMAILJS_TEMPLATE_ID || "";

  if (EMAILJS_PUBLIC_KEY) {
    emailjs.init({ publicKey: EMAILJS_PUBLIC_KEY });
  }

  contactForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const payload = {
      name: contactForm.name.value.trim(),
      email: contactForm.email.value.trim(),
      message: contactForm.message.value.trim(),
    };

    if (!payload.name || !payload.email || !payload.message) {
      formStatus.textContent = "Please fill out all fields.";
      formStatus.dataset.state = "error";
      return;
    }

    formStatus.textContent = "Sending...";
    formStatus.dataset.state = "idle";

    try {
      if (CONTACT_API_URL) {
        const response = await fetch(CONTACT_API_URL, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });

        const result = await response.json();
        if (!response.ok) {
          throw new Error(result.detail || "Unable to send right now.");
        }

        formStatus.textContent = result.message || "Message sent.";
        formStatus.dataset.state = "success";
        contactForm.reset();
        return;
      }

      if (EMAILJS_PUBLIC_KEY && EMAILJS_SERVICE_ID && EMAILJS_TEMPLATE_ID) {
        await emailjs.send(EMAILJS_SERVICE_ID, EMAILJS_TEMPLATE_ID, {
          from_name: payload.name,
          from_email: payload.email,
          message: payload.message,
        });

        formStatus.textContent = "Message sent.";
        formStatus.dataset.state = "success";
        contactForm.reset();
        return;
      }

      throw new Error(
        "Contact is not configured yet. Fill in EMAILJS_PUBLIC_KEY, EMAILJS_SERVICE_ID, and EMAILJS_TEMPLATE_ID in static/site-config.js.",
      );
    } catch (error) {
      formStatus.textContent =
        (error && error.text) || error.message || "Something went wrong.";
      formStatus.dataset.state = "error";
    }
  });
})();
