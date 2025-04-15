
def predict_trend(text):
    sentiment = text.lower().count("moon") - text.lower().count("rug")
    return "up" if sentiment > 0 else "down"
