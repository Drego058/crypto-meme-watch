
fetch("/analyze")
  .then(res => res.json())
  .then(data => {
    const verifiedContainer = document.getElementById("verifiedCoins");
    const upcomingContainer = document.getElementById("upcomingCoins");
    const viewToggle = document.getElementById("viewToggle");

    const sortedVerified = data.verified
      .map(item => {
        item.trendScore = Math.round(
          (item.mentions * 2) +
          (item.avg_sentiment * 50) +
          ((item.change_24h ?? 0) * 2)
        );
        return item;
      })
      .sort((a, b) => b.trendScore - a.trendScore);

    function renderCards() {
      const view = viewToggle.value;
      verifiedContainer.className = "coin-list " + (view === "list" ? "list-view" : "grid-view");
      upcomingContainer.className = "coin-list " + (view === "list" ? "list-view" : "grid-view");

      verifiedContainer.innerHTML = "";
      upcomingContainer.innerHTML = "";

      sortedVerified.forEach(item => {
        const div = document.createElement("div");
        div.className = "card verified";
        div.innerHTML = `
          <h3>$${item.coin}</h3>
          <p><strong>Status:</strong> ✅ Verified</p>
          <p><strong>Mentions:</strong> ${item.mentions}</p>
          <p><strong>Sentiment:</strong> ${item.avg_sentiment}</p>
          <p><strong>Price:</strong> $${item.price?.toFixed(4) ?? "?"}</p>
          <p><strong>Change 24h:</strong> ${item.change_24h ?? "?"}%</p>
          <p><strong>🔥 Trending Score:</strong> ${item.trendScore}</p>
        `;
        verifiedContainer.appendChild(div);
      });

      data.upcoming.forEach(item => {
        const div = document.createElement("div");
        div.className = "card upcoming";
        div.innerHTML = `
          <h3>$${item.coin}</h3>
          <p><strong>Status:</strong> 🚀 Upcoming</p>
          <p><strong>Mentions:</strong> ${item.mentions}</p>
          <p><strong>Sentiment:</strong> ${item.avg_sentiment}</p>
        `;
        upcomingContainer.appendChild(div);
      });
    }

    viewToggle.addEventListener("change", renderCards);
    renderCards();
  })
  .catch(err => {
    console.error("Fout bij ophalen data:", err);
    document.body.innerHTML = "<p>Kon geen data laden van de backend.</p>";
  });
