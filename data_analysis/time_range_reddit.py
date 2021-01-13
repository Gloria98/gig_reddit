from datetime import datetime
import pandas as pd
import csv
from multiprocessing import Pool
from os import path, makedirs, cpu_count, environ, remove
from itertools import product
import numpy as np

# this file contains code to see how many posts are there in each month

def time_range_2020(subreddit):
    print(f'subreddit: {subreddit} ---------------------')
    file_name = f'/pine/scr/m/t/mtguo/gig/reddit/{subreddit}/{subreddit}_2020_comments.csv'
    records = pd.read_csv(file_name, names = ["author","subreddit", "id", "title", "time","score","num_comments","domain","url","selftext"])
    print(f'total posts collected: {len(records)}')
    d1 = datetime.strptime("2020-1-1", '%Y-%m-%d')
    d2 = datetime.strptime("2020-2-1", '%Y-%m-%d')
    d3 = datetime.strptime("2020-3-1", '%Y-%m-%d')
    d4 = datetime.strptime("2020-4-1", '%Y-%m-%d')
    d5 = datetime.strptime("2020-5-1", '%Y-%m-%d')
    d6 = datetime.strptime("2020-6-1", '%Y-%m-%d')
    d7 = datetime.strptime("2020-7-1", '%Y-%m-%d')
    d8 = datetime.strptime("2020-8-1", '%Y-%m-%d')
    d9 = datetime.strptime("2020-9-1", '%Y-%m-%d')
    p1, p2, p3, p4, p5, p6, p7, p8, p9 = 0, 0, 0, 0, 0, 0, 0, 0, 0
    dates = records['time'].to_list()
    for date in dates:
        try:
            date = date.split()[0]
            d = datetime.strptime(date, '%Y-%m-%d')
        except:
            continue
        
        if d>=d1 and d<d2:
            p1 += 1
        elif d>=d2 and d<d3:
            p2 += 1
        elif d>=d3 and d<d4:
            p3 += 1
        elif d>=d4 and d<d5:
            p4 += 1
        elif d>=d5 and d<d6:
            p5 += 1
        elif d>=d6 and d<d7:
            p6 += 1
        elif d>=d7 and d<d8:
            p7 += 1
        elif d>=d8 and d<d9:
            p8 += 1
        elif d>=d9:
            p9 += 1
    total = len(records)
    post_line = [subreddit, total, p1/total, p2/total, p3/total, p4/total, p5/total, p6/total, p7/total, p8/total, p9/total]
    with open("reddit_info_comments2020.csv", 'a') as f:
        csv.writer(f).writerow(post_line)


def time_range_2019(subreddit):
    print(f'subreddit: {subreddit} ---------------------')
    file_name = f'/pine/scr/m/t/mtguo/gig/reddit/{subreddit}/{subreddit}_2019_comments.csv'
    records = pd.read_csv(file_name, names = ["author","subreddit", "id", "title", "time","score","num_comments","domain","url","selftext"])
    print(f'total posts collected: {len(records)}')
    # d1 = datetime.strptime("2020-1-1", '%Y-%m-%d')
    # d2 = datetime.strptime("2020-2-1", '%Y-%m-%d')
    # d3 = datetime.strptime("2020-3-1", '%Y-%m-%d')
    # d4 = datetime.strptime("2020-4-1", '%Y-%m-%d')
    # d5 = datetime.strptime("2020-5-1", '%Y-%m-%d')
    # d6 = datetime.strptime("2020-6-1", '%Y-%m-%d')
    # d7 = datetime.strptime("2020-7-1", '%Y-%m-%d')
    # d8 = datetime.strptime("2020-8-1", '%Y-%m-%d')
    # d9 = datetime.strptime("2020-9-1", '%Y-%m-%d')
    d1 = datetime.strptime("2019-1-1", '%Y-%m-%d')
    d2 = datetime.strptime("2019-2-1", '%Y-%m-%d')
    d3 = datetime.strptime("2019-3-1", '%Y-%m-%d')
    d4 = datetime.strptime("2019-4-1", '%Y-%m-%d')
    d5 = datetime.strptime("2019-5-1", '%Y-%m-%d')
    d6 = datetime.strptime("2019-6-1", '%Y-%m-%d')
    d7 = datetime.strptime("2019-7-1", '%Y-%m-%d')
    d8 = datetime.strptime("2019-8-1", '%Y-%m-%d')
    d9 = datetime.strptime("2019-9-1", '%Y-%m-%d')
    d10 = datetime.strptime("2019-10-1", '%Y-%m-%d')
    d11 = datetime.strptime("2019-11-1", '%Y-%m-%d')
    d12 = datetime.strptime("2019-12-1", '%Y-%m-%d')
    d_next = datetime.strptime("2019-12-31", '%Y-%m-%d')
    p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    dates = records['time'].to_list()
    for date in dates:
        try:
            date = date.split()[0]
            d = datetime.strptime(date, '%Y-%m-%d')
        except:
            continue
        
        if d>=d1 and d<d2:
            p1 += 1
        elif d>=d2 and d<d3:
            p2 += 1
        elif d>=d3 and d<d4:
            p3 += 1
        elif d>=d4 and d<d5:
            p4 += 1
        elif d>=d5 and d<d6:
            p5 += 1
        elif d>=d6 and d<d7:
            p6 += 1
        elif d>=d7 and d<d8:
            p7 += 1
        elif d>=d8 and d<d9:
            p8 += 1
        elif d>=d9 and d<d10:
            p9 += 1
        elif d>=d10 and d<d11:
            p10 += 1
        elif d>=d11 and d<d12:
            p11 += 1
        elif d>=d12 and d<=d_next:
            p12 += 1
    total = len(records)
    post_line = [subreddit, total, p1/total, p2/total, p3/total, p4/total, p5/total, p6/total, p7/total, p8/total, p9/total, p10/total, p11/total, p12/total]
    with open("reddit_info_comments2019.csv", 'a') as f:
        csv.writer(f).writerow(post_line)

subreddits = ["airbnb_hosts", "AirBnB", "couchsurfing", "vrbo", "CaregiverSupport", "Nanny", "AmazonFlexDrivers", 
            "InstacartShoppers", "instacart", "ShiptShoppers", "doordash", "doordash_drivers",
            "UberEATS", "grubhubdrivers", "postmates", "FieldAgent", "TaskRabbit", "RoverPetSitting",
            "Etsy", "EtsySellers", "uber", "uberdrivers", "lyftdrivers", "Lyft", "GetAround",
            "mturk", "TurkerNation", "vipkid", "Upwork", "kaggle", "Fiverr", "MusicEd"]

def main():
    for subreddit in subreddits:
        time_range_2019(subreddit)

def cal_2019():
    all_info = pd.read_csv("reddit_info_comments2019.csv", names=["subreddit", "total", "p1", "p2", "p3","p4", "p5", "p6", "p7", "p8", "p9", "p10", "p11", "p12"])
    means = np.mean(all_info[["total", "p1", "p2", "p3","p4", "p5", "p6", "p7", "p8", "p9", "p10", "p11", "p12"]].values, axis=0)
    print(means)

def cal_2020():
    all_info = pd.read_csv("reddit_info_comments2020.csv", names=["subreddit", "total", "p1", "p2", "p3","p4", "p5", "p6", "p7", "p8", "p9"])
    means = np.mean(all_info[["total", "p1", "p2", "p3","p4", "p5", "p6", "p7", "p8", "p9"]].values, axis=0)
    print(means)

cal_2019()