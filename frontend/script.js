fetch("http://localhost:8000/analyze")
  .then(res => res.json())
  .then(data => {
    const div = document.getElementById("results");
    data.results.forEach(item => {
      div.innerHTML += `<p><b>Text:</b> ${item.text}<br><b>Sentiment:</b> ${item.sentiment}<br><b>Prediction:</b> ${item.prediction}</p>`;
    });
  });
