function send_message() {
    let answers = {
        q1: document.querySelector('input[name="q1"]:checked')?.value,
        q2: document.querySelector('input[name="q2"]:checked')?.value,
        q3: document.querySelector('input[name="q3"]:checked')?.value,
        q4: document.querySelector('input[name="q4"]:checked')?.value,
        q5: document.querySelector('input[name="q5"]:checked')?.value,
        q6: document.querySelector('input[name="q6"]:checked')?.value,
        q7: document.querySelector('input[name="q7"]:checked')?.value,
        q8: document.querySelector('input[name="q8"]:checked')?.value,
        q9: document.querySelector('input[name="q9"]:checked')?.value,
        q10: document.querySelector('input[name="q10"]:checked')?.value
    };

    console.log("Sending:", answers);

    fetch("http://localhost:5000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(answers)
    })
    .then(response => response.json())
    .then(data => {
        console.log("Model output:", data);
        // احفظي النتيجة أو حوّلي المستخدم لصفحة نتائج
        localStorage.setItem("model_output", JSON.stringify(data));
        window.location.href = "/results";
    })
    .catch(err => console.error("Error:", err));
}
