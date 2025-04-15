
const mockVerified = [
  { coin: "MOCK1", mentions: 12, avg_sentiment: 0.65, price: 0.00012, change_24h: 5.3 },
  { coin: "MOCK2", mentions: 8, avg_sentiment: 0.4, price: 0.0056, change_24h: -1.2 }
];

const mockUpcoming = [
  { coin: "WAGMI", mentions: 15, avg_sentiment: 0.8 },
  { coin: "CHAD", mentions: 7, avg_sentiment: 0.6 }
];

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
    const div = document.createElement("div");
    div.className = "card verified" + (item.isDemo ? " demo" : "");
    div.innerHTML = `
      <h3>$${item.coin} ${item.isDemo ? "<span class='demo-label'>DEMO</span>" : ""}</h3>
      <p><strong>Status:</strong> ✅ Verified</p>
      <p><strong>Mentions:</strong> ${item.mentions}</p>
      <p><strong>Sentiment:</strong> ${item.avg_sentiment}</p>
      <p><strong>Price:</strong> $${item.price?.toFixed(4) ?? "?"}</p>
      <p><strong>Change 24h:</strong> ${item.change_24h ?? "?"}%</p>
      <p><strong>🔥 Trending Score:</strong> ${item.trendScore}</p>
    `;
    verifiedContainer.appendChild(div);
  });

  upcomingData.forEach(item => {
    const div = document.createElement("div");
    div.className = "card upcoming" + (item.isDemo ? " demo" : "");
    div.innerHTML = `
      <h3>$${item.coin} ${item.isDemo ? "<span class='demo-label'>DEMO</span>" : ""}</h3>
      <p><strong>Status:</strong> 🚀 Upcoming</p>
      <p><strong>Mentions:</strong> ${item.mentions}</p>
      <p><strong>Sentiment:</strong> ${item.avg_sentiment}</p>
    `;
    upcomingContainer.appendChild(div);
  });

  if (!verifiedData.length && !upcomingData.length) {
    verifiedContainer.innerHTML = "<p>⚠️ Geen resultaten gevonden. Probeer later opnieuw.</p>";
  }
}

fetch("/analyze")
  .then(res => {
    if (!res.ok) throw new Error("API error: " + res.status);
    return res.json();
  })
  .then(data => {
    const dataToggle = document.getElementById("dataToggle");
    const viewToggle = document.getElementById("viewToggle");

    const render = () => renderDashboard(data, dataToggle?.value || "live");

    viewToggle?.addEventListener("change", render);
    dataToggle?.addEventListener("change", render);
    render();
  })
  .catch(err => {
    console.error("Fout bij ophalen data:", err);
    document.body.innerHTML = "<p>❌ Kan geen data ophalen van de backend. Controleer of deze draait.</p>";
  });
