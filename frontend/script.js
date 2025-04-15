
fetch("/analyze")
  .then(res => res.json())
  .then(data => {
    const coins = data.results.map(item => item.coin || "Unknown");
    const mentions = data.results.map(item => item.mentions || 0);
    const sentiments = data.results.map(item => item.avg_sentiment || 0);
    const prices = data.results.map(item => item.price || 0);

    // Chart.js chart
    new Chart(document.getElementById("mentionChart"), {
      type: "bar",
      data: {
        labels: coins,
        datasets: [{
          label: "Mentions per Coin",
          data: mentions,
          backgroundColor: "#4b9cd3"
        }]
      }
    });

    // Vul de tabel
    const tbody = document.getElementById("coinTableBody");
    data.results.forEach(item => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${item.coin || "-"}</td>
        <td>${item.mentions || 0}</td>
        <td>${item.avg_sentiment?.toFixed(2) || 0}</td>
        <td>${item.price !== null ? "$" + item.price : "n/a"}</td>
      `;
      tbody.appendChild(row);
    });
  })
  .catch(err => {
    console.error("Error fetching data:", err);
    document.body.innerHTML = "<p>Fout bij laden van het dashboard.</p>";
  });
