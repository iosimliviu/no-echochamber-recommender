import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors


pd.options.mode.chained_assignment = None

# Reading the dataframes


dfsubs = pd.read_csv("dfsubs.csv")
dflast = pd.read_csv("dflast.csv")

# Removing sparsity from the ratings dataset -- ignore zero values and create new data structure
csr_data = csr_matrix(dflast.values)
dflast.reset_index(inplace=True)

# Using K-Nearest Neighbors as a similarity metric with cosine simlarity
knn = NearestNeighbors(metric='cosine', n_neighbors=20)
knn.fit(csr_data)

# Defining subreddit recommender function
def subreddit_recommender(sub_name):
    print(sub_name)
    num_subs_to_reccomend = 10
    sub_list = dfsubs[dfsubs['subreddit'].str.contains(sub_name)]
    if len(sub_list):
        sub_idx = sub_list.iloc[0]['sub_id']
        sub_idx = dflast[dflast['sub_id'] == sub_idx].index[0]
        distances, indices = knn.kneighbors(csr_data[sub_idx], n_neighbors=num_subs_to_reccomend + 1)
        rec_sub_indices = sorted(list(zip(indices.squeeze().tolist(), distances.squeeze().tolist())),
                                 key=lambda x: x[1])[:0:-1]
        recommend_frame = []
        for val in rec_sub_indices:
            sub_idx = dflast.iloc[val[0]]['sub_id']
            idx = dfsubs[dfsubs['sub_id'] == sub_idx].index
            recommend_frame.append({'Subreddit': dfsubs.iloc[idx]['subreddit'].values[0], 'Distance': val[1]})
        recomandedDf = pd.DataFrame(recommend_frame, index=range(1, num_subs_to_reccomend + 1))
        return recomandedDf
    else:
        return "No subreddits found. Please check your input"


# subreddit_recommender("masterrace")
# subreddit_recommender("AskReddit")

# print(subreddit_recommender("AskReddit").to_markdown())


