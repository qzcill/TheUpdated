document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector("form");

  form.addEventListener("submit", function (e) {
    e.preventDefault(); // نوقف الإرسال مؤقتًا

    const fname = document.querySelector('input[placeholder="First Name"]').value.trim();
    const lname = document.querySelector('input[placeholder="Last Name"]').value.trim();
    const email = document.querySelector('input[placeholder="Email"]').value.trim();
    const password = document.querySelector('input[placeholder="Password"]').value;
    const confirm = document.querySelector('input[placeholder="Confirm Password"]').value;

    const namePattern = /^[A-Za-z]+$/;
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!namePattern.test(fname) || !namePattern.test(lname)) {
      alert("❌ Name should contain only letters (no numbers or symbols).");
      return;
    }

    if (!emailPattern.test(email)) {
      alert("❌ Please enter a valid email (e.g., user@gmail.com).");
      return;
    }

    if (password.length < 8) {
      alert("❌ Password must be at least 8 characters long.");
      return;
    }

    if (password !== confirm) {
      alert("❌ Passwords do not match!");
      return;
    }

    alert(" Account created successfully!");
    form.submit(); // بعد التحقق يرسل النموذج
  });
});
