
// frontend script: simplified fallback demo version
const mockVerified = [
  { coin: "MOON", mentions: 14, avg_sentiment: 0.73, price: 0.0012, change_24h: 6.1 },
  { coin: "DOGE", mentions: 9, avg_sentiment: 0.42, price: 0.082, change_24h: -1.3 }
];

const mockUpcoming = [
  { coin: "WAGMI", mentions: 11, avg_sentiment: 0.65 },
  { coin: "CHAD", mentions: 7, avg_sentiment: 0.2 }
];

const getSentimentLabel = (score) => {
  if (score > 0.5) return { label: "🟢 Bullish", class: "sentiment-positive" };
  if (score < 0) return { label: "🔴 Bearish", class: "sentiment-negative" };
  return { label: "🟡 Neutraal", class: "sentiment-neutral" };
};

function renderDashboard(view = "grid") {
  const verifiedContainer = document.getElementById("verifiedCoins");
  const upcomingContainer = document.getElementById("upcomingCoins");

  verifiedContainer.className = "coin-list " + (view === "list" ? "list-view" : "grid-view");
  upcomingContainer.className = "coin-list " + (view === "list" ? "list-view" : "grid-view");

  verifiedContainer.innerHTML = "";
  upcomingContainer.innerHTML = "";

  mockVerified.forEach(item => {
    const sentiment = getSentimentLabel(item.avg_sentiment);
    const div = document.createElement("div");
    div.className = "card verified";
    div.innerHTML = `
      <h3>$${item.coin}</h3>
      <p><strong>Status:</strong> ✅ Verified</p>
      <p><strong>Mentions:</strong> ${item.mentions}</p>
      <p class="${sentiment.class}"><strong>Sentiment:</strong> ${item.avg_sentiment} (${sentiment.label})</p>
      <p><strong>Price:</strong> $${item.price}</p>
      <p><strong>Change 24h:</strong> ${item.change_24h}%</p>
    `;
    verifiedContainer.appendChild(div);
  });

  mockUpcoming.forEach(item => {
    const sentiment = getSentimentLabel(item.avg_sentiment);
    const div = document.createElement("div");
    div.className = "card upcoming";
    div.innerHTML = `
      <h3>$${item.coin}</h3>
      <p><strong>Status:</strong> 🚀 Upcoming</p>
      <p><strong>Mentions:</strong> ${item.mentions}</p>
      <p class="${sentiment.class}"><strong>Sentiment:</strong> ${item.avg_sentiment} (${sentiment.label})</p>
    `;
    upcomingContainer.appendChild(div);
  });
}

document.getElementById("viewToggle")?.addEventListener("change", e => {
  renderDashboard(e.target.value);
});

renderDashboard();
