
const getSentimentLabel = (score) => {
  if (score > 0.5) return { label: "🟢 Bullish", class: "sentiment-positive" };
  if (score < 0) return { label: "🔴 Bearish", class: "sentiment-negative" };
  return { label: "🟡 Neutraal", class: "sentiment-neutral" };
};

function renderDashboard(data, mode = "live") {
  const verifiedContainer = document.getElementById("verifiedCoins");
  const upcomingContainer = document.getElementById("upcomingCoins");
  const viewToggle = document.getElementById("viewToggle");

  const verifiedData = (mode === "demo" ? mockVerified : (data.verified || [])).map(item => {
    item.trendScore = Math.round(
      (item.mentions * 2) +
      (item.avg_sentiment * 50) +
      ((item.change_24h ?? 0) * 2)
    );
    item.isDemo = mode === "demo";
    return item;
  }).sort((a, b) => b.trendScore - a.trendScore);

  const upcomingData = (mode === "demo" ? mockUpcoming : (data.upcoming || [])).map(item => ({
    ...item,
    isDemo: mode === "demo"
  }));

  const view = viewToggle?.value || "grid";
  verifiedContainer.className = "coin-list " + (view === "list" ? "list-view" : "grid-view");
  upcomingContainer.className = "coin-list " + (view === "list" ? "list-view" : "grid-view");

  verifiedContainer.innerHTML = "";
  upcomingContainer.innerHTML = "";

  verifiedData.forEach(item => {
    const sentiment = getSentimentLabel(item.avg_sentiment);
    const isHot = item.trendScore > 80;
    const div = document.createElement("div");
    div.className = `card verified ${item.isDemo ? "demo" : ""}`;
    div.innerHTML = `
      <h3>$${item.coin} 
        ${item.isDemo ? "<span class='demo-label'>DEMO</span>" : ""}
        ${isHot ? "<span class='hot-label'>🔥 HOT</span>" : ""}
      </h3>
      <p><strong>Status:</strong> ✅ Verified</p>
      <p><strong>Mentions:</strong> ${item.mentions}</p>
      <p class="${sentiment.class}"><strong>Sentiment:</strong> ${item.avg_sentiment} (${sentiment.label})</p>
      <p><strong>Price:</strong> $${item.price?.toFixed(4) ?? "?"}</p>
      <p><strong>Change 24h:</strong> ${item.change_24h ?? "?"}%</p>
      <p><strong>🔥 Trending Score:</strong> ${item.trendScore}</p>
      <div class="scorebar">
        <div class="bar" style="width: ${Math.min(item.trendScore, 100)}%"></div>
      </div>
    `;
    verifiedContainer.appendChild(div);
  });

  upcomingData.forEach(item => {
    const sentiment = getSentimentLabel(item.avg_sentiment);
    const div = document.createElement("div");
    div.className = `card upcoming ${item.isDemo ? "demo" : ""}`;
    div.innerHTML = `
      <h3>$${item.coin} ${item.isDemo ? "<span class='demo-label'>DEMO</span>" : ""}</h3>
      <p><strong>Status:</strong> 🚀 Upcoming</p>
      <p><strong>Mentions:</strong> ${item.mentions}</p>
      <p class="${sentiment.class}"><strong>Sentiment:</strong> ${item.avg_sentiment} (${sentiment.label})</p>
    `;
    upcomingContainer.appendChild(div);
  });

  if (!verifiedData.length && !upcomingData.length) {
    verifiedContainer.innerHTML = "<p>⚠️ Geen resultaten gevonden. Probeer later opnieuw.</p>";
  }
}
