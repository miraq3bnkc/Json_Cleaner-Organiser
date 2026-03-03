import os
import json
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

path = r"../apify/digital_ids" #path that includes the .json files (only) 

#Loop through all files in folder and clean them
for file in os.scandir(path):
    if file.is_file():
        data=[] # initialization of the data in the .json file 

        with open(file.path, "r") as f:
            print("Cleaning ", file.name, ":")
            data = json.load(f) # Load .json file for clean up
        
        #De-duplicate json data (remove duplicate tweets by id)
        unique_data = de_duplicate(data)

        #Delete noise (non-greek or non-greeklish tweets)
        denoised_data=delete_tweets(unique_data)

        # Overwrite file with cleaned data
        with open(file.path, "w", encoding="utf-8") as f:
            json.dump(denoised_data, f, indent=4)

