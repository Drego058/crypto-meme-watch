
fetch("/analyze")
  .then(res => res.json())
  .then(data => {
    const div = document.getElementById("results");
    data.results.forEach(item => {
      div.innerHTML += `
        <div class="card">
          <h3>$${item.coin}</h3>
          <p><strong>Mentions:</strong> ${item.mentions}</p>
          <p><strong>Avg. Sentiment:</strong> ${item.avg_sentiment.toFixed(2)}</p>
          <p><strong>Price (USD):</strong> ${item.price !== null ? '$' + item.price : 'n/a'}</p>
        </div>
      `;
    });
  })
  .catch(err => {
    document.getElementById("results").innerHTML = "<p>Error fetching data.</p>";
    console.error("Fout bij ophalen data:", err);
  });
