
// Herstelde en volledige werkende script.js met demo, fallback, sparkline voorbereiding
const mockVerified = [
  { coin: "MOCK1", mentions: 12, avg_sentiment: 0.65, price: 0.00012, change_24h: 5.3, sparkline: [0.0001, 0.00011, 0.00012, 0.00013, 0.00014] },
  { coin: "MOCK2", mentions: 8, avg_sentiment: 0.4, price: 0.0056, change_24h: -1.2, sparkline: [0.0055, 0.0056, 0.0057, 0.0056, 0.0054] }
];

const mockUpcoming = [
  { coin: "WAGMI", mentions: 15, avg_sentiment: 0.8, sparkline: [] },
  { coin: "CHAD", mentions: 7, avg_sentiment: 0.6, sparkline: [] }
];

const getSentimentLabel = (score) => {
  if (score > 0.5) return { label: "🟢 Bullish", class: "sentiment-positive" };
  if (score < 0) return { label: "🔴 Bearish", class: "sentiment-negative" };
  return { label: "🟡 Neutraal", class: "sentiment-neutral" };
};

function renderSparkline(data) {
  if (!Array.isArray(data) || data.length < 2) return "";
  const min = Math.min(...data);
  const max = Math.max(...data);
  const points = data.map((v, i) => {
    const x = (i / (data.length - 1)) * 100;
    const y = 100 - ((v - min) / (max - min)) * 100;
    return `${x},${y.toFixed(2)}`;
  }).join(" ");
  return `<svg viewBox="0 0 100 100" preserveAspectRatio="none" class="sparkline"><polyline points="${points}" /></svg>`;
}

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
    const priceText = item.price ? `$${item.price.toFixed(4)}` : "<span class='warn'>Niet beschikbaar</span>";
    const changeText = item.change_24h !== null && item.change_24h !== undefined
      ? `${item.change_24h}%`
      : "<span class='warn'>Niet beschikbaar</span>";
    const sparklineSVG = item.sparkline && item.sparkline.length ? renderSparkline(item.sparkline) : "";

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
      <p><strong>Price:</strong> ${priceText}</p>
      <p><strong>Change 24h:</strong> ${changeText}</p>
      <p><strong>🔥 Trending Score:</strong> ${item.trendScore}</p>
      <div class="scorebar">
        <div class="bar" style="width: ${Math.min(item.trendScore, 100)}%"></div>
      </div>
      ${sparklineSVG}
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
