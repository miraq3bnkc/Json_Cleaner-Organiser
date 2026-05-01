"""Transforming the raw data extracted from the raw tweet response"""

import hashlib
import json

#Keep only the mentions that are not the default mention by replying to a post
def transform_mentions(reply_username, mentions):
    new_mentions=[]

    for i in range(len(mentions)):
        if mentions[i]!=reply_username:
            new_mentions.append(mentions[i])
    
    return new_mentions

#Change urls to their article domain if they are linked through a redirecting link
def transform_urls(article_domain,urls):
    redirectors=[
        "dlvr.it",
        "ift.tt",
        "ow.ly",
        "share.google",
        "search.app",
        "bit.ly",
        "disq.us",
        "tinyurl.com"
    ]
    
    for i, url in enumerate(urls):
        for redirector in redirectors:
            if url.find(redirector)!=-1:
                urls[i] = article_domain
                break

    return urls

def get_user_list(tweet,users):

    potential_user = {
        "id": tweet.get("author").get("user_id"),
        "userName": tweet.get("author").get("userName") 
    }

    users.append(potential_user)

def anonymize_username(username):
    return hashlib.sha256(username.encode()).hexdigest()


irrelevant_users=[]
#Replace usernames with user ids
def replace_username_id(user_mentions,users):

    for i,mention in enumerate(user_mentions):
        found=0
        for user in users:
            if mention==user["userName"]:
                user_mentions[i]=user["id"]
                found=1
                break  #go to the next mention
    
        if found==0:
            #the mentioned user is not in our user list 
            for ir_user in irrelevant_users:
                if mention==ir_user["userName"]:
                    user_mentions[i]=ir_user["id"]
                    found=1
                    break
            
            if found==0:
                #if the user is not in our irrelevant list either, add them 
                irrelevant_user={
                    "id": anonymize_username(mention),
                    "userName": mention
                }
                user_mentions[i]=irrelevant_user["id"]
                irrelevant_users.append(irrelevant_user)

    return user_mentions