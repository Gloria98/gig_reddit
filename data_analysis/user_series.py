import matplotlib
matplotlib.use('Agg')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.nonparametric.smoothers_lowess import lowess
from config import subreddits

# count the number of new users each day
def count_new_user(_start, _end, df):
    time_list = pd.date_range(start=_start, end=_end, freq='D')
    all_user = []
    new_count_list = []
    d_list = pd.to_datetime(df.time)
    for i in range(len(time_list)-1):
        new_count = 0
        sub_author = df[(d_list>time_list[i]) & (d_list<=time_list[i+1])]['author'].unique()
        for user in sub_author:
            if user not in all_user:
                new_count += 1
                all_user.append(user)
        new_count_list.append(new_count)

    return time_list, new_count_list

# plot the number of new users in subreddit each day, draw it in a form of time series
def plot_reddit(subreddit):
    dumpFolder = f'/pine/scr/m/t/mtguo/gig/new_reddit/{subreddit}'
    file_name1 = f'{dumpFolder}/{subreddit}_2019.csv'
    file_name2 = f'{dumpFolder}/{subreddit}_2020.csv'
    file_name3 = f'{dumpFolder}/{subreddit}_2019_comments.csv'
    file_name4 = f'{dumpFolder}/{subreddit}_2020_comments.csv'

    file1 = pd.read_csv(file_name1, names=['author', 'subreddit', 'id', 'title', 'time', 'score', 
                                            'num_comments', 'domain', 'url', 'body'])
    file2 = pd.read_csv(file_name2, names=['author', 'subreddit', 'id', 'title', 'time', 'score', 
                                            'num_comments', 'domain', 'url', 'body'])
    file3 = pd.read_csv(file_name3, names=['author', 'subreddit', 'id', 'parent_id', 'time', 'score', 'body'])
    file4 = pd.read_csv(file_name4, names=['author', 'subreddit', 'id', 'parent_id', 'time', 'score', 'body'])
    post_df = pd.concat([file1, file2], sort=False)
    post_df = post_df.reset_index(drop=True)
    date_list = file1['time'].to_list() + file2['time'].to_list() + file3['time'].to_list() + file4['time'].to_list()
    author_list = file1['author'].to_list() + file2['author'].to_list() + file3['author'].to_list() + file4['author'].to_list()
    df = pd.DataFrame({'time': date_list, 'author': author_list})
    time_list, count_list = count_new_user('2019-1-1', '2020-9-10', df)
    # plt.plot(time_list[:-1], count_list)
    # plt.savefig(f'images/{subreddit}.png')
    # print(count_list)
    df_loess_15 = lowess(count_list, np.arange(len(count_list)), frac=0.15)[:, 1]
    ts = pd.DataFrame({'# new users': count_list[15:], 'smoothed posts': df_loess_15[15:]}, index=time_list[15:-1])

    ts.plot()
    plt.ylabel('# New users')
    plt.title(f'{subreddit}')
    plt.savefig(f'images/{subreddit}_new_user.png')


# for subreddit in subreddits:
#     plot_reddit(subreddit)
plot_reddit("HITsWorthTurkingFor")
