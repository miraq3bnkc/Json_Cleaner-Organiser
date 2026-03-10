import os
import json
from remove_posts import de_duplicate,delete_tweets
from remove_fields import clean_tweet
from datetime import datetime

path = r"../apify/digital_ids" #path that includes the .json files (only) 

#function for accessing the datetime string existing in "createdAt" field
def parse_date(tweet):
    return datetime.strptime(tweet["createdAt"], "%a %b %d %H:%M:%S %z %Y")

all_tweets=[]

#Loop through all files in folder and clean them
for file in os.scandir(path):
    if file.is_file():
        data=[] # initialization of the data in the .json file 

        with open(file.path, "r",encoding="utf-8") as f:
            print("Cleaning ", file.name, ":")
            data = json.load(f) # Load .json file for clean up
        
        #De-duplicate json data (remove duplicate tweets by id)
        unique_data = de_duplicate(data)

        #Delete noise (non-greek or non-greeklish tweets)
        denoised_data=delete_tweets(unique_data)

        #removing unnecessary fields in tweet data
        cleaned_tweets=[clean_tweet(tweet, False) for tweet in denoised_data]

        all_tweets.extend(cleaned_tweets) #merging all the tweets together via extend


# sort tweets by createdAt
tweets_sorted = sorted(all_tweets, key=parse_date,reverse=True)


# save merged file
with open("merged.json", "w", encoding="utf-8") as f:
    json.dump(tweets_sorted, f, ensure_ascii=False, indent=2)

