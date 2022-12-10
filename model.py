import spacy
import re

nlp = spacy.load("output/model-best")

def clean_tweet(tweet_text):
    return re.sub("(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-&?=%.]+", "", tweet_text).strip()

def clickbait_checker(tweet_text):
    cleaned_text = clean_tweet(tweet_text)
    cats = nlp(cleaned_text).cats
    if max(cats, key=cats.get) == "clickbait":
        return (1, cats["clickbait"])
    return (0, cats["not_clickbait"])
