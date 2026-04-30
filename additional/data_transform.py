"""Transforming the raw data extracted from the raw tweet response"""

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

#Delete usernames and keep user ids only
def map_id_delete_name(users):
    #work for later
    return 