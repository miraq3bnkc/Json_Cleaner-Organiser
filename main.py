from graph_structure.network_graph import create_DiGraph, plot_graph, get_graph_features
from processing.openfiles import load_data,save_file,extract_transform,merge_quotes
from processing.data_transform import replace_username_id, account_age
import networkx as nx


path = r"../apify/digital_ids (Copy)" #path that includes the .json files (only) 

tweets=load_data(path)
cleaned_tweets,clean_quotes,users=extract_transform(tweets)
tweets=merge_quotes(clean_quotes,cleaned_tweets)

#Now that we have all the users, let's erase usernames from data
tweets=replace_username_id(tweets,users)

# save all cleaned tweets in file
save_file("merged.json",tweets)
#save users in a file
save_file("users.json",users)


#Create Network graph of user interconnection in the dataset
G=create_DiGraph(users,tweets)
#plot_graph(G,1,12)


features=get_graph_features(G)

processed_tweets=[]

for tweet in tweets:
    tweet=account_age(tweet)
    
    #Adding graph features (define it in a function for a more clean code)

    user_id=tweet["author"].get("user_id")
    tweet["author"]["betweeness"]=features[0][user_id]
    tweet["author"]["pagerank"]=features[1][user_id]
    tweet["author"]["clustering"]=features[2][user_id]
    tweet["author"]["core"]=features[3][user_id]
    if user_id in features[4]:
        tweet["author"]["has_selfloop"]=True
        tweet["author"]["weight"] = G[user_id][user_id]["weight"] 
    else:
        tweet["author"]["has_selfloop"]=False
    tweet["author"]["weighted_indeg"]=G.in_degree(user_id,weight="weight") #fix: remove selfloops in weight
    tweet["author"]["weighted_outdeg"]=G.out_degree(user_id,weight="weight") #fix

    processed_tweets.append(tweet)


save_file("processed.json",processed_tweets)