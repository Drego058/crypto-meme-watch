
const backendUrl = window.location.hostname.includes("onrender.com")
  ? "https://" + window.location.hostname + "/analyze"
  : "http://localhost:8000/analyze";

fetch(backendUrl)
  .then(res => res.json())
  .then(data => {
    const div = document.getElementById("results");
    if (!data.results) {
      div.innerHTML = "<p>No data received from backend.</p>";
      return;
    }
    data.results.forEach(item => {
      div.innerHTML += `<div class="card">
        <p><strong>Text:</strong> ${item.text}</p>
        <p><strong>Sentiment:</strong> ${item.sentiment}</p>
        <p><strong>Prediction:</strong> ${item.prediction}</p>
      </div>`;
    });
  })
  .catch(err => {
    console.error("Fout bij ophalen data:", err);
    document.getElementById("results").innerHTML = "<p>Kan geen data laden van de backend.</p>";
  });
