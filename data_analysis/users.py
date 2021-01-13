import matplotlib
matplotlib.use('Agg')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.nonparametric.smoothers_lowess import lowess
from config import dumpFolder_base, subreddits
from user_list import top_users


def process_user(user, df):
    sub_df = df[df['author']==user]
    num_posts = len(sub_df)
    num_com = 0
    for idx, row in sub_df.iterrows():
        num_com += int(row['num_comments'])
    return num_posts, num_com

def plot_users(subreddit):
    user_df = pd.read_csv(f'user_infos/{subreddit}.csv')
    x = user_df['num_posts'].astype(int).to_list()
    y = user_df['num_comments'].astype(int).to_list()
    # print(max(y))
    color = 'orange'
    plt.scatter(x, y, c=color, alpha=0.5)
    plt.xlabel('Posts')
    plt.ylabel('Comments')
    plt.title(f'{subreddit}')
    plt.savefig(f'user_images/{subreddit}.png')

def process_subreddit(subreddit):
    dumpFolder = f'{dumpFolder_base}/{subreddit}'
    file_name1 = f'{dumpFolder}/{subreddit}_2019.csv'
    file_name2 = f'{dumpFolder}/{subreddit}_2020.csv'
    file1 = pd.read_csv(file_name1, names=['author', 'subreddit', 'id', 'title', 'time', 'score', 
                                            'num_comments', 'domain', 'url', 'body'])
    file2 = pd.read_csv(file_name2, names=['author', 'subreddit', 'id', 'title', 'time', 'score', 
                                            'num_comments', 'domain', 'url', 'body'])
    post_df = pd.concat([file1, file2], sort=False)
    post_df = post_df.reset_index(drop=True)
    users = post_df.author.unique()
    user_df = pd.DataFrame()
    for user in users:
        num_posts, num_com = process_user(user, post_df)
        user_df = user_df.append({'author': user, 'num_posts': num_posts, 'num_comments': num_com}, ignore_index=True)
    user_df = user_df[user_df['author'] != '[deleted]']
    # plot_users(user_df, subreddit)
    user_df = user_df.sort_values(by=['num_posts'], ascending=False)
    user_df.to_csv(f'user_infos/{subreddit}.csv', index=False)



def extract_users(user_list, subreddit):
    dumpFolder = f'{dumpFolder_base}/{subreddit}'
    file_name1 = f'{dumpFolder}/{subreddit}_2019.csv'
    file_name2 = f'{dumpFolder}/{subreddit}_2020.csv'
    file1 = pd.read_csv(file_name1, names=['author', 'subreddit', 'id', 'title', 'time', 'score', 
                                            'num_comments', 'domain', 'url', 'body'])
    file2 = pd.read_csv(file_name2, names=['author', 'subreddit', 'id', 'title', 'time', 'score', 
                                            'num_comments', 'domain', 'url', 'body'])
    post_df = pd.concat([file1, file2], sort=False)
    post_df = post_df.reset_index(drop=True)
    res = pd.DataFrame()
    for user in user_list:
        sub_df = post_df[post_df['author']==user]
        res = pd.concat([res, sub_df], sort=False)
    res.to_csv(f'user_infos/{subreddit}_ulist.csv', index=False)

# for subreddit in subreddits:
#     # print(subreddit)
#     # process_subreddit(subreddit)
#     user_df = pd.read_csv(f'user_infos/{subreddit}.csv')
#     user_df = user_df.sort_values(by=['num_comments'], ascending=False)
#     user_df.to_csv(f'user_infos/{subreddit}_comments.csv', index=False)

for subreddit in subreddits:
    users = top_users[subreddit]
    extract_users(users, subreddit)

#     plot_users(subreddit)

