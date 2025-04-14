def predict_trend(text):
    # Simpele regelgebaseerde voorspelling voor demo
    sentiment = text.lower().count("moon") - text.lower().count("rug")
    return "up" if sentiment > 0 else "down"
