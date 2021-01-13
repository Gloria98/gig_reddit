import requests
import json
import re
import time
from time import sleep
from json import dump
import pandas as pd
import shutil
import csv
from datetime import datetime
from multiprocessing import Pool
from itertools import product
from os import path, makedirs, cpu_count, environ, remove
import sys
from random import sample

# this file contains some code to validate the collective data

PUSHSHIFT_REDDIT_URL = "http://api.pushshift.io/reddit"
def val(subreddit, year):
    dumpFolder = f'/pine/scr/m/t/mtguo/gig/reddit/{subreddit}'
    if path.exists(f"{dumpFolder}/{subreddit}_{year}.csv"):
        data_path = f'{dumpFolder}/{subreddit}_{year}.csv'
        data = pd.read_csv(data_path, names=['author', 'subreddit', 'id', 'title', 'time', 'score', 'num_comments', 'domain', 'url', 'selftext'])
        data_records = data.to_dict('record')
        # sample 100 posts to validate information
        sample_posts = sample(data_records, min(100, len(data_records)))
        for post in sample_posts:
            # search for this post
            post_id = post['id']
            record_author = post['author']
            record_score = post['score']
            record_comments = post['num_comments']
            params = {'ids': post_id}
            req_url = f'{PUSHSHIFT_REDDIT_URL}/submission/search/'
            r = requests.get(req_url, params=params, timeout=30)
            if r.status_code == 200:
                response = json.loads(r.text)
                if len(response['data']) == 0:
                    print(f'{subreddit} {year} cannot find {post_id}')
                    continue
                data = response['data'][0]
                author = data['author']
                score = data['score']
                num_comments = data['num_comments']
                if author!=record_author:
                    print(f"{year} submission {post_id} author wrong, record is {record_author}, api gives {author}")
                if score!=record_score:
                    print(f"{year} submission {post_id} score wrong, record is {record_score}, api gives {score}")
                if num_comments!=record_comments:
                    print(f"{year} submission {post_id} comments wrong, record is {record_comments}, api gives {num_comments}")

subreddits = ["airbnb_hosts", "AirBnB", "couchsurfing", "vrbo", "CaregiverSupport", "Nanny", "AmazonFlexDrivers", 
            "InstacartShoppers", "instacart", "ShiptShoppers", "doordash", "doordash_drivers",
            "UberEATS", "grubhubdrivers", "postmates", "FieldAgent", "TaskRabbit", "RoverPetSitting",
            "Etsy", "EtsySellers", "uber", "uberdrivers", "lyftdrivers", "Lyft", "GetAround",
            "mturk", "TurkerNation", "vipkid", "Upwork", "kaggle", "Fiverr", "crowdSPRING", "MusicEd"]

for subreddit in subreddits:
    val(subreddit, 2019)
    val(subreddit, 2020)
# data_path = '/pine/scr/m/t/mtguo/gig/reddit/AirBnB/AirBnB_2020.csv'
# data = pd.read_csv(data_path, names=['author', 'subreddit', 'id', 'title', 'time', 'score', 'num_comments', 'domain', 'url', 'selftext'])
# sub_data = data[data['id']=='i2p7no']
# print(sub_data['title'])
# params = {'q': "Host say they don't want to pay the electric"}

# req_url = f'{PUSHSHIFT_REDDIT_URL}/submission/search/'
# r = requests.get(req_url, params=params, timeout=30)
# if r.status_code == 200:
#     response = json.loads(r.text)
#     print(response['data'][0])