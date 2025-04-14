from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

nltk.download("vader_lexicon")

def analyze_text(text: str):
    sid = SentimentIntensityAnalyzer()
    scores = sid.polarity_scores(text)
    sentiment = "neutral"
    if scores["compound"] >= 0.05:
        sentiment = "positive"
    elif scores["compound"] <= -0.05:
        sentiment = "negative"
    confidence = round(abs(scores["compound"]) * 100, 2)
    return {"sentiment": sentiment, "confidence": confidence}