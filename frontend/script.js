
fetch("/analyze")
  .then(res => res.json())
  .then(data => {
    const div = document.getElementById("results");
    if (!data.results) {
      div.innerHTML = "<p>No results.</p>";
      return;
    }
    data.results.forEach(item => {
      div.innerHTML += `
        <div class="card">
          <p><strong>Text:</strong> ${item.text}</p>
          <p><strong>Sentiment:</strong> ${item.sentiment}</p>
          <p><strong>Prediction:</strong> ${item.prediction}</p>
          <p><strong>Bitcoin Price:</strong> $${item.price_btc}</p>
        </div>
      `;
    });
  })
  .catch(err => {
    console.error("Error fetching data:", err);
    document.getElementById("results").innerHTML = "<p>Could not load data from backend.</p>";
  });
