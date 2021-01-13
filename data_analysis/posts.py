import matplotlib
matplotlib.use('Agg')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.nonparametric.smoothers_lowess import lowess
from config import dumpFolder_base, subreddits
from user_list import top_users


# draw the image of participation pattern, x is number of comments and y is number of upvote
# intput: subreddit name
# output: None
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

    x = post_df['num_comments'].astype(int).to_list()
    y = post_df['score'].astype(int).to_list()
    # get std and mean

    comm_mean = np.mean(x)
    comm_std = np.std(x)
    score_mean = np.mean(y)
    score_std = np.std(y)
    for i in range(3, 30):
        comm_threshold = comm_mean +  i * comm_std
        score_threshold = score_mean + i * score_std
        out_posts = post_df[(post_df['num_comments']>comm_threshold) | (post_df['score']>score_threshold)]
        if len(out_posts)>30:
            continue
        out_posts.to_csv(f'post_info/{subreddit}.csv', index=False)
        print(i)
        print(len(out_posts))
        break
    # plot
    color = 'black'
    plt.scatter(x, y, c=color, alpha=0.5)
    plt.xlabel('Comments')
    plt.ylabel('Upvotes')
    plt.title(f'{subreddit}')
    plt.savefig(f'post_images/{subreddit}.png')

process_subreddit('MusicEd')