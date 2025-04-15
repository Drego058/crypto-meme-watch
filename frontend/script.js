
fetch("/analyze")
  .then(res => res.json())
  .then(data => {
    const verifiedContainer = document.getElementById("verifiedCoins");
    const upcomingContainer = document.getElementById("upcomingCoins");

    // Toon upcoming coins
    data.upcoming.forEach(item => {
      const div = document.createElement("div");
      div.className = "card";
      div.innerHTML = `
        <h3>$${item.coin}</h3>
        <p><strong>Status:</strong> 🚀 Upcoming</p>
        <p><strong>Mentions:</strong> ${item.mentions}</p>
        <p><strong>Sentiment:</strong> ${item.avg_sentiment}</p>
      `;
      upcomingContainer.appendChild(div);
    });

    // Toon verified coins
    data.verified.forEach(item => {
      const div = document.createElement("div");
      div.className = "card";
      div.innerHTML = `
        <h3>$${item.coin}</h3>
        <p><strong>Status:</strong> ✅ Verified</p>
        <p><strong>Mentions:</strong> ${item.mentions}</p>
        <p><strong>Sentiment:</strong> ${item.avg_sentiment}</p>
        <p><strong>Price:</strong> $${item.price ?? "?"}</p>
        <p><strong>Change 24h:</strong> ${item.change_24h ?? "?"}%</p>
      `;
      verifiedContainer.appendChild(div);
    });
  })
  .catch(err => {
    console.error("Fout bij ophalen data:", err);
    document.body.innerHTML = "<p>Kon geen data laden van de backend.</p>";
  });
