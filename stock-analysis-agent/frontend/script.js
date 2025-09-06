async function analyze() {
    const ticker = document.getElementById("ticker").value;
    const resultDiv = document.getElementById("result");
    resultDiv.innerHTML = "Analyzing...";

    const response = await fetch("/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ticker }),
    });

    const result = await response.json();
    resultDiv.innerHTML = result.analysis;
