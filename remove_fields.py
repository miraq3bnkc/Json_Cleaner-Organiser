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

def get_author_entities(entities):
     description_urls=[]
     linked_urls=[]

     #get description urls
     description= entities.get("description")
     if description.get("urls")!=[]:
        for url in description.get("urls"):
            description_urls.append(url.get("expanded_url"))

     linked=entities.get("url")
     if linked:
          for url in linked.get("urls"):
               linked_urls.append(url.get("expanded_url"))

     return [description_urls, linked_urls]

def extract_author(author):
    profession= get_profession(author.get("professional"))
    entities= get_author_entities(author.get("entities"))

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
        "description_urls": entities[0],
        "linked_urls": entities[1],
        "favouritesCount": author.get("favouritesCount"),
        "mediaCount": author.get("mediaCount"),
        "statusesCount": author.get("statusesCount"),
        "professional_category": profession[0],
        "professional_type": profession[1]
    }        

    return cleaned_author

#Extract string values with key: description, domain or title from card/legacy/binding_values
def extract_card(card):
    if card!={}:
        binding_values=card["legacy"]["binding_values"]
        for b_value in binding_values:
            key=b_value.get("key")
            if key=="description":
                article_description=b_value["value"]["string_value"]
            elif key=="domain":
                article_domain=b_value["value"]["string_value"]
            elif key=="title":
                article_title=b_value["value"]["string_value"]
    else:
        article_description=None
        article_domain=None
        article_title=None

    return {"article_description":article_description,
             "article_domain":article_domain, 
             "article_title":article_title}

def get_media(entities):
    media=[]

    if entities.get("media"):
        for post_media in entities.get("media"):
            media.append(post_media.get("type"))
    return media

def extract_entities(entities, tweet):
    hashtags=[]
    urls=[]
    user_mentions=[]

    #Get the hashtags used in text of the post 
    if entities["hashtags"]!=[]:
        for hashtag in entities["hashtags"]:
            hashtags.append(hashtag.get("text"))

    #Get the type and number of media used in the post
    if tweet.get("extendedEntities"):
        #only quotes in tweet data have the field of extendedEntities in our dataset
        media=get_media(tweet.get("extendedEntities"))
    else:
        media=get_media(entities)

    #Get the URLs in the text of the post
    if entities["urls"]:
        for url in entities["urls"]:
            urls.append(url.get("expanded_url"))

    #Get the user mentions written in the tweeter post
    if entities["user_mentions"]:
        for mention in entities["user_mentions"]:
            user_mentions.append(mention.get("screen_name"))

    return [hashtags, media, urls, user_mentions]


def clean_tweet(tweet):  
    entities=extract_entities(tweet.get("entities"), tweet)

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
        "isConversationControlled": tweet.get("isConversationControlled"),
        "author" : extract_author(tweet.get("author")),
        "linked_article_values": extract_card(tweet.get("card")),
        "hashtags": entities[0],
        "media": entities[1],
        "urls": entities[2],
        "user_mentions": entities[3]
    }

    return cleaned_tweet



with open("test.json", "r", encoding="utf-8") as f:
    tweets = json.load(f) # Load .json file for clean up

cleaned_tweets=[clean_tweet(tweet) for tweet in tweets]

with open("test_output.json", "w", encoding="utf-8") as f:
        json.dump(cleaned_tweets, f, indent=2, ensure_ascii=False)