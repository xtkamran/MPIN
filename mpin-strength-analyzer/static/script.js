document.addEventListener("DOMContentLoaded", function () {
  // Theme switcher
  const themeSwitch = document.getElementById("checkbox");
  themeSwitch.addEventListener("change", function () {
    document.documentElement.setAttribute(
      "data-theme",
      this.checked ? "dark" : "light"
    );
  });

  // Tab switching
  const tabButtons = document.querySelectorAll(".tab-btn");
  tabButtons.forEach((button) => {
    button.addEventListener("click", function () {
      // Remove active class from all buttons and content
      tabButtons.forEach((btn) => btn.classList.remove("active"));
      document.querySelectorAll(".tab-content").forEach((content) => {
        content.classList.remove("active");
      });

      // Add active class to clicked button and corresponding content
      this.classList.add("active");
      const tabId = this.getAttribute("data-tab");
      document.getElementById(`${tabId}-tab`).classList.add("active");
    });
  });

  // Analyze buttons
  document.getElementById("analyze-4").addEventListener("click", function () {
    analyzeMPIN(4);
  });

  document.getElementById("analyze-6").addEventListener("click", function () {
    analyzeMPIN(6);
  });

  // Generate buttons
  document.getElementById("generate-4").addEventListener("click", function () {
    generateMPIN(4);
  });

  document.getElementById("generate-6").addEventListener("click", function () {
    generateMPIN(6);
  });

  function analyzeMPIN(length) {
    const mpinInput = document.getElementById(`mpin-${length}`);
    const mpin = mpinInput.value.trim();

    if (
      !mpin ||
      (length === 4 && mpin.length !== 4) ||
      (length === 6 && mpin.length !== 6)
    ) {
      showResult("INVALID", ["INVALID_LENGTH"]);
      return;
    }

    // Collect demographic data
    const demographics = {};
    const userDobInput = document.getElementById(
      length === 4 ? "user-dob" : "user-dob-6"
    );
    const spouseDobInput = document.getElementById(
      length === 4 ? "spouse-dob" : "spouse-dob-6"
    );
    const anniversaryInput = document.getElementById(
      length === 4 ? "anniversary" : "anniversary-6"
    );

    if (userDobInput.value) demographics.user_dob = userDobInput.value;
    if (spouseDobInput.value) demographics.spouse_dob = spouseDobInput.value;
    if (anniversaryInput.value)
      demographics.anniversary = anniversaryInput.value;

    // Send to server for analysis
    fetch("/analyze", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        mpin,
        demographics,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        showResult(data.strength, data.reasons);
      })
      .catch((error) => {
        console.error("Error:", error);
        showResult("ERROR", ["ANALYSIS_FAILED"]);
      });
  }

  function generateMPIN(length) {
    fetch("/generate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        pin_length: length,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        const mpinInput = document.getElementById(`mpin-${length}`);
        mpinInput.value = data.pin;
        mpinInput.type = "text";

        // Show the generated PIN for a few seconds, then hide it
        setTimeout(() => {
          mpinInput.type = "password";
        }, 3000);
      })
      .catch((error) => {
        console.error("Error:", error);
        alert("Failed to generate MPIN. Please try again.");
      });
  }

  function showResult(strength, reasons) {
    const strengthElement = document.getElementById("strength");
    strengthElement.textContent = strength;
    strengthElement.className = "value";
    strengthElement.classList.add(strength);

    const reasonsList = document.getElementById("reasons");
    reasonsList.innerHTML = "";

    if (reasons && reasons.length > 0) {
      reasons.forEach((reason) => {
        const li = document.createElement("li");
        li.textContent = formatReason(reason);
        reasonsList.appendChild(li);
      });
    } else if (strength === "STRONG") {
      const li = document.createElement("li");
      li.textContent = "No vulnerabilities detected";
      li.style.color = "#00b894";
      reasonsList.appendChild(li);
    }
  }

  function formatReason(reason) {
    const reasonMap = {
      COMMONLY_USED: "Commonly used MPIN",
      DEMOGRAPHIC_DOB_SELF: "Based on your date of birth",
      DEMOGRAPHIC_DOB_SPOUSE: "Based on spouse's date of birth",
      DEMOGRAPHIC_ANNIVERSARY: "Based on wedding anniversary date",
      INVALID_LENGTH: "Invalid MPIN length",
      NON_DIGIT: "MPIN contains non-digit characters",
    };

    return reasonMap[reason] || reason;
  }

  // Input validation for date fields
  const dateInputs = document.querySelectorAll('input[placeholder*="DD/MM"]');
  dateInputs.forEach((input) => {
    input.addEventListener("input", function (e) {
      // Allow only numbers and slashes
      this.value = this.value.replace(/[^0-9/]/g, "");

      // Auto-insert slashes
      if (this.value.length === 2 || this.value.length === 5) {
        this.value += "/";
      }
    });
  });
});
