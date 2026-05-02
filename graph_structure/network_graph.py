import json
import networkx as nx
import matplotlib.pyplot as plt

def add_with_weight(source,target,Graph):
    if Graph.has_edge(source,target):
        Graph.edges[(source,target)]["weight"] += 1
    else:
        Graph.add_edge(source,target,weight=1)

def create_DiGraph(users,tweets):
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
    return G

def plot_graph(Graph,threshold,window):

    # Detect self-loop nodes before removing loops
    self_loop_nodes = set(u for u, v in nx.selfloop_edges(Graph))

    # Remove self-loops from drawing
    Graph.remove_edges_from(nx.selfloop_edges(Graph))

    #remove isolated nodes, with degree less than threshold
    nodes_to_keep = [n for n in Graph.nodes() if Graph.degree(n) > threshold]

    G_plot = Graph.subgraph(nodes_to_keep)
    
    print("Number of edges in figure: ",G_plot.number_of_edges())
    print("Number of nodes in figure: ",len(nodes_to_keep))
    
    # Layout
    pos = nx.spring_layout(G_plot, k=0.2, iterations=50, seed=42)

    # Degree-based sizes
    degrees = dict(G_plot.degree())

    node_sizes = [
        20 + degrees[n] * 8   # base size + scaling
        for n in G_plot.nodes()
    ]

    # Color nodes with self-loops differently
    node_colors = [
        'orange' if n in self_loop_nodes else 'steelblue'
        for n in G_plot.nodes()
    ]

    plt.figure(figsize=(window, window))

    nx.draw_networkx_nodes(
        G_plot,
        pos,
        node_size=node_sizes,
        node_color=node_colors,
        alpha=0.8
    )

    nx.draw_networkx_edges(
        G_plot,
        pos,
        arrows=True,
        arrowsize=4,
        width=0.3,
        alpha=0.3
    )

    plt.axis('off')
    plt.show()