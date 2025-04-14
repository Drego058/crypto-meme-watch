const backendUrl = window.location.hostname.includes("onrender.com")
  ? "https://" + window.location.hostname + "/analyze"
  : "http://localhost:8000/analyze";

fetch(backendUrl)
  .then(res => {
    if (!res.ok) throw new Error("Server returned " + res.status);
    return res.json();
  })
  .then(data => {
    const div = document.getElementById("results");
    if (data.error) {
      div.innerHTML = `<p><b>Fout van backend:</b> ${data.error}</p>`;
      return;
    }
    data.results.forEach(item => {
      div.innerHTML += `<p><b>Text:</b> ${item.text}<br><b>Sentiment:</b> ${item.sentiment}<br><b>Prediction:</b> ${item.prediction}</p>`;
    });
  })
  .catch(err => {
    console.error("Fout bij ophalen data:", err);
    document.getElementById("results").innerHTML = "<p>Kan geen data laden van de backend.</p>";
  });
