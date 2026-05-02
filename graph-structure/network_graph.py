import json
import networkx as nx

def add_with_weight(source,target,Graph):
    if Graph.has_edge(source,target):
        Graph.edges[(source,target)]["weight"] += 1
    else:
        Graph.add_edge(source,target,weight=1)

tweets=[]
with open("merged.json", "r",encoding="utf-8") as f:
    tweets=json.load(f)

users={}
with open("users.json","r",encoding="utf-8") as f:
    users=json.load(f) #2029 users

G = nx.DiGraph()
G.add_nodes_from(users.values())

for tweet in tweets:
    user_node=tweet["author"]["user_id"] #source node
    
    #add edges for all the replies
    reply=tweet.get("inReplyToUserId") #target node
    if reply and G.has_node(reply):
        add_with_weight(user_node,reply,G)

    #add edges for all mentions
    mentions=tweet["user_mentions"] #target nodes
    for mention in mentions:
        if G.has_node(mention):
            add_with_weight(user_node,mention,G)
    
    #add edges from quotes
    quote=tweet.get("quoted_user_id") #target node
    if quote and G.has_node(quote):
        add_with_weight(user_node,quote,G)


print(G.number_of_nodes())
print(G.number_of_edges())
