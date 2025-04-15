
const backendUrl = window.location.hostname.includes("onrender.com")
  ? "https://" + window.location.hostname + "/analyze"
  : "http://localhost:8000/analyze";

fetch(backendUrl)
  .then(res => res.json())
  .then(data => {
    const div = document.getElementById("results");
    if (!data.results) {
      div.innerHTML = "<p>No data received.</p>";
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
