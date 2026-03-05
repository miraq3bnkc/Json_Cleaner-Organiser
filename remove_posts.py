"""This python script is created for the purpose of the removal
   of noisy tweets. More specifically we remove:
    1. Duplicate posts that exist in the .json files
       according to their id
    2. Posts that are not in the Greek language, with 
       Greek language we include Greeklish too  """

import re
from urllib.parse import urlparse

def de_duplicate(data):
    #Keep only the last instance with the same "id"
    unique_data = {tweet["id"]: tweet for tweet in data}.values()
    # Convert back to list and return result
    return list(unique_data)

# Detect any Greek character
def contains_greek(text):
    return bool(re.search(r'[α-ωΑ-Ω]', text))

#For posts with no-text but only a URL link check if it has a greek domain
def is_greek_domain(url):
    if not url:
        return False
    domain = urlparse(url).netloc
    return domain.endswith(".gr")

def extract_expanded_url(tweet):
    urls = tweet.get("entities", {}).get("urls", [])
    if urls:
        return urls[0].get("expanded_url")
    return None

#Delete unrelated tweets according to the language
def delete_tweets(tweets):

    cleaned_tweets = []

    for tweet in tweets:
        text = tweet.get("text", "")
        url = tweet.get("url", "No URL available")
        expanded_url = extract_expanded_url(tweet)

        # Rule 1: Contains text in Greek language
        if contains_greek(text):
            cleaned_tweets.append(tweet)
            continue

        # Rule 2: URL from Greek domain
        if is_greek_domain(expanded_url):
            cleaned_tweets.append(tweet)
            continue
        
        # Rule 3: Ask user permission for deletion 
        print("\n--- POSSIBLE NON-GREEK TWEET ---")
        print("Text:", text)
        print("Tweet URL:", url)
        print("Referenced URL:",expanded_url)

        choice = input("Delete this tweet? (y/n): ").strip().lower()

        if choice == "n":
            cleaned_tweets.append(tweet)
        else:
            print("Deleted.")

    return cleaned_tweets