import matplotlib
matplotlib.use('Agg')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.nonparametric.smoothers_lowess import lowess
plt.rcParams.update({'font.size': 16})

# this file contain code that plot the number of post or comments in each day in a form of time series

# get the number of posts posted in each day from the dataframe df
# input: _start: the start of the time, _end: the end of time, df: a dataframe with all the posts or comments
# output: a list of time from _start to _end, a corresponding list with the number of posts or comment from that day
def count_time_series(_start, _end, df):
    time_list = pd.date_range(start=_start, end=_end, freq='D')
    count_list = []
    d_list = pd.to_datetime(df.time)
    for i in range(len(time_list)-1):
        c = np.sum((d_list>time_list[i]) & (d_list<=time_list[i+1]))
        count_list.append(c)
    
    return time_list, count_list

# plot the time series of everything, include posts and comments
# input: subreddit name
def plot_reddit(subreddit):
    dumpFolder = f'/pine/scr/m/t/mtguo/gig/reddit/{subreddit}'
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
    df = pd.DataFrame({'time': date_list})
    time_list, count_list = count_time_series('2019-1-1', '2020-9-10', df)
    # plt.plot(time_list[:-1], count_list)
    # plt.savefig(f'images/{subreddit}.png')
    # print(count_list)

    df_loess_15 = lowess(count_list, np.arange(len(count_list)), frac=0.15)[:, 1]
    ts = pd.DataFrame({'# posts': count_list, 'smoothed posts': df_loess_15}, index=time_list[:-1])

    ts.plot()
    plt.ylabel('# posts and comments')
    plt.title(f'{subreddit}')
    plt.savefig(f'images/{subreddit}.png')
    print(subreddit)
    select = find_top_10(time_list, count_list)
    extract_days(select, post_df, subreddit)

# plot the time series of posts
# input: subreddit name
def plot_reddit_posts(subreddit):
    matplotlib.rc('lines', linewidth=2)
    plt.rcParams["figure.figsize"] = (6.8,5)
    dumpFolder = f'/pine/scr/m/t/mtguo/gig/reddit/{subreddit}'
    file_name1 = f'{dumpFolder}/{subreddit}_2019.csv'
    file_name2 = f'{dumpFolder}/{subreddit}_2020.csv'

    file1 = pd.read_csv(file_name1, names=['author', 'subreddit', 'id', 'title', 'time', 'score', 
                                            'num_comments', 'domain', 'url', 'body'])
    file2 = pd.read_csv(file_name2, names=['author', 'subreddit', 'id', 'title', 'time', 'score', 
                                            'num_comments', 'domain', 'url', 'body'])
    post_df = pd.concat([file1, file2], sort=False)
    post_df = post_df.reset_index(drop=True)
    date_list = file1['time'].to_list() + file2['time'].to_list()
    df = pd.DataFrame({'time': date_list})
    time_list, count_list = count_time_series('2019-1-1', '2020-9-10', df)
    # plt.plot(time_list[:-1], count_list)
    # plt.savefig(f'images/{subreddit}.png')
    # print(count_list)

    df_loess_15 = lowess(count_list, np.arange(len(count_list)), frac=0.15)[:, 1]
    ts = pd.DataFrame({'# posts': count_list, 'smoothed posts': df_loess_15}, index=time_list[:-1])

    ts.plot(legend=None)
    plt.ylabel('# posts')
    plt.title(f'{subreddit}')
    plt.savefig(f'images/{subreddit}_posts.png')
    print(subreddit)
    # select = find_top_10(time_list, count_list)
    # extract_days_post(select, post_df, subreddit)

# find the top 10 days where there are most activities
# intput: a list of days, a corresponding list of number of posts or comments in that day
# output: top 10 days with most posts or comments
def find_top_10(time_list, count_list):
    sort_list = np.argsort(count_list[:-1])
    select = []
    for i in range(1,11):
        select.append(time_list[sort_list[-i]])
        print(time_list[sort_list[-i]])
    return select

# find the posts from special days from subreddit and save it to a csv
# input: _start: a day to start, _end: a day to end, subreddit: subreddit name
# output: None
def extract_days_special(_start, _end, subreddit):
    dt_start = pd.to_datetime(_start)
    dt_end = pd.to_datetime(_end)
    dumpFolder = f'/pine/scr/m/t/mtguo/gig/reddit/{subreddit}'
    file_name1 = f'{dumpFolder}/{subreddit}_2019.csv'
    file_name2 = f'{dumpFolder}/{subreddit}_2020.csv'

    file1 = pd.read_csv(file_name1, names=['author', 'subreddit', 'id', 'title', 'time', 'score', 
                                            'num_comments', 'domain', 'url', 'body'])
    file2 = pd.read_csv(file_name2, names=['author', 'subreddit', 'id', 'title', 'time', 'score', 
                                            'num_comments', 'domain', 'url', 'body'])
    post_df = pd.concat([file1, file2], sort=False)
    post_df = post_df.reset_index(drop=True)
    d_list = pd.to_datetime(post_df.time)
    selected = post_df[(d_list >= dt_start)&(d_list <= dt_end)]
    selected.to_csv(f'infos/{subreddit}_{_start}.csv')

# find the comments from special days from subreddit and save it to a csv
def extract_com_special(_start, _end, subreddit):
    dt_start = pd.to_datetime(_start)
    dt_end = pd.to_datetime(_end)
    dumpFolder = f'/pine/scr/m/t/mtguo/gig/reddit/{subreddit}'
    file_name1 = f'{dumpFolder}/{subreddit}_2019_comments.csv'
    file_name2 = f'{dumpFolder}/{subreddit}_2020_comments.csv'

    file1 = pd.read_csv(file_name1, names=['author', 'subreddit', 'id', 'parent_id', 'time', 'score', 'body'])
    file2 = pd.read_csv(file_name2, names=['author', 'subreddit', 'id', 'parent_id', 'time', 'score', 'body'])
    post_df = pd.concat([file1, file2], sort=False)
    post_df = post_df.reset_index(drop=True)
    d_list = pd.to_datetime(post_df.time)
    selected = post_df[(d_list >= dt_start)&(d_list <= dt_end)]
    selected.to_csv(f'infos/{subreddit}_comments_{_start}.csv')


# find posts from the days listed in date_list
def extract_days(date_list, df, subreddit):
    d_list = pd.to_datetime(df.time)
    out_df = pd.DataFrame()
    for date in date_list:
        records = df[(d_list>date)&(d_list<=(date+1))]
        out_df = pd.concat([out_df, records], sort=False)
    out_df.to_csv(f'infos/{subreddit}.csv')

def extract_days_post(date_list, df, subreddit):
    d_list = pd.to_datetime(df.time)
    out_df = pd.DataFrame()
    for date in date_list:
        print(date)
        records = df[(d_list>date)&(d_list<=(date+1))]
        print(len(records))
        out_df = pd.concat([out_df, records], sort=False)
    out_df.to_csv(f'infos/{subreddit}_posts.csv')

subreddits = ["airbnb_hosts", "AirBnB", "couchsurfing", "vrbo", "CaregiverSupport", "Nanny", "AmazonFlexDrivers", 
            "InstacartShoppers", "instacart", "ShiptShoppers", "doordash", "doordash_drivers",
            "UberEATS", "grubhubdrivers", "postmates", "FieldAgent", "TaskRabbit", "RoverPetSitting",
            "Etsy", "EtsySellers", "uber", "uberdrivers", "lyftdrivers", "Lyft", "GetAround",
            "mturk", "TurkerNation", "vipkid", "Upwork", "kaggle", "Fiverr", "MusicEd"]

# for subreddit in subreddits:
#     plot_reddit(subreddit)
#     print('post')
#     plot_reddit_posts(subreddit)
# plot_reddit("HITsWorthTurkingFor")
# extract_com_special('2019-08-23', '2019-08-24', 'mturk')
# extract_com_special('2020-07-31', '2020-08-01', 'Fiverr')
# extract_days_special('2020-04-30', '2020-05-02', 'Fiverr')
# extract_days_special('2019-07-01', '2019-07-15', 'Upwork')
# extract_days_special('2020-08-24', '2020-08-25', 'EtsySellers')
subreddit = 'couchsurfing'
plot_reddit_posts(subreddit)