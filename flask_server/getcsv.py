import pandas as pd
pd.options.mode.chained_assignment = None

df = pd.read_csv("reddit_data.csv");
# drop datetime column => not useful
df.drop(['utc'], inplace=True, axis=1)

# finding each user's total number of comments for each subreddit
dftot = df.groupby(['username', 'subreddit']).size().reset_index(name="tot_comments")

# Finding each user's max number of comments for all subreddits
dfmax = dftot.groupby(['username'])['tot_comments'].max().reset_index(name="max_comments")

# Merging total and max comments onto new dataframe
dfnew = pd.merge(dftot, dfmax, on='username', how='left')

# Calculate a user's subreddit rating based on total and max comments
dfnew['rating'] = dfnew['tot_comments'] / dfnew['max_comments'] * 10

# Create new dataframe and drop duplicate users
dfusers = df.drop_duplicates(subset='username')
# Drop subs
dfusers.drop(['subreddit'], inplace=True, axis=1)
# Sort by users
dfusers = dfusers.sort_values(['username'], ascending=True)
# Reset index
dfusers.reset_index(drop=True, inplace=True)
# Create user id from index
dfusers['user_id'] = dfusers.index + 1

# Create new dataframe and drop duplicate subs
dfsubs = df.drop_duplicates(subset='subreddit')
# # Drop users
dfsubs.drop(['username'], inplace=True, axis=1)
# # Sort by subs
dfsubs = dfsubs.sort_values(['subreddit'], ascending=True)
# # Reset index
dfsubs.reset_index(drop=True, inplace=True)
# # Create user id from index
dfsubs['sub_id'] = dfsubs.index + 1

# merging user id onto dataframe, moving position
dfnew = pd.merge(dfnew, dfusers, on='username', how='left')
move_pos = dfnew.pop('user_id')
dfnew.insert(1, 'user_id', move_pos)
# Merging sub id onto dataframe, moving position
dfnew = pd.merge(dfnew, dfsubs, on='subreddit', how='left')
move_pos = dfnew.pop('sub_id')
dfnew.insert(3, 'sub_id', move_pos)




# similarity matrix
# create new dataframe
dfnum = dfnew

# Drop non-numerical columns
dfnew.drop(['username', 'subreddit', 'tot_comments', 'max_comments'], inplace=True, axis=1)

# Pivot dataframe into a matrix of total ratings for users and subs
dfrat = dfnum.pivot(index='sub_id', columns='user_id', values='rating')

# Replace all null values with 0 -- null values are subreddits on which user has no interaction
dfrat.fillna(0, inplace=True)

# Calculating number of users commenting per sub
num_users = dfnum.groupby('sub_id')['rating'].agg('count')

# Calculating number of subs per user
num_subs = dfnum.groupby('user_id')['rating'].agg('count')

# Limiting dataframe to only subreddits with 100 or more commenting users
dflast = dfrat.loc[num_users[num_users > 100].index, :]

# Limiting dataframe to only users following 10 or more subs
dflast = dflast.loc[:, num_subs[num_subs > 10].index]

dflast.to_csv('dflast.csv')
dfsubs.to_csv("dfsubs.csv")
dfnew.to_csv('dfnew.csv')