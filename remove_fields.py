"""This python script is created for the purposes of "cleaning" the .json data
   that contain information about X.com posts. 
   Specifically it will remove unnecessary fields and change/rename some other fields.
   This will all be according to the example.txt file were you can see the changes
   to be made. 

   This "clean up" is part of a bigger analysis of X posts that were obtained from 
   an Apify actor: https://apify.com/apidojo/tweet-scraper.
   The changes are curated for the specific analysis. 
"""

import json 

def get_profession(professional):
    #initialization
    professional_category=None
    professional_type=None

    #change values only if they exist in .json 
    if professional:
        professional_type = professional.get("professional_type")
        if professional.get("category"):
             professional_category = professional["category"][0]["name"]

    return [
        professional_category,
        professional_type  
            ]

def extract_author(author):
    profession= get_profession(author.get("professional"))

    cleaned_author={
        "userName": author.get("userName"),
        "profile_url": author.get("url"),
        "user_id": author.get("id"),
        "isBlueVerified":author.get("isBlueVerified"),
        "description": author.get("description"),
        "followers": author.get("followers"),
        "following": author.get("following"),
        "canDm": author.get("canDm"),
        "canMediaTag": author.get("canMediaTag"),
        "createdAt": author.get("createdAt"),
        "favouritesCount": author.get("favouritesCount"),
        "mediaCount": author.get("mediaCount"),
        "statusesCount": author.get("statusesCount"),
        "professional_category": profession[0],
        "professional_type": profession[1]
    }        

    return cleaned_author

def clean_tweet(tweet):  
    
    cleaned_tweet={
        "id": tweet.get("id"),
        "url":tweet.get("url"),
        "text":tweet.get("text"),
        "retweetCount":tweet.get("retweetCount"),
        "replyCount": tweet.get("replyCount"),
        "likeCount": tweet.get("likeCount"),
        "quoteCount": tweet.get("quoteCount"),
        "viewCount": tweet.get("viewCount"),
        "createdAt": tweet.get("createdAt"),
        "bookmarkCount": tweet.get("bookmarkCount"),
        "isReply": tweet.get("isReply"),
        "isQuote": tweet.get("isQuote"),
        "isConversationControlled": tweet.get("isConversationControlled")
    }

    cleaned_tweet["author"] = extract_author(tweet.get("author"))

    return cleaned_tweet



with open("test.json", "r", encoding="utf-8") as f:
    tweets = json.load(f) # Load .json file for clean up

cleaned_tweets=[clean_tweet(tweet) for tweet in tweets]

with open("test_output.json", "w", encoding="utf-8") as f:
        json.dump(cleaned_tweets, f, indent=2, ensure_ascii=False)