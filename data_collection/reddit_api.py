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
from config import *
from itertools import product
from os import path, makedirs, cpu_count, environ, remove
import sys


PUSHSHIFT_REDDIT_URL = "http://api.pushshift.io/reddit"



# def fetchComments(subreddit, submission_id, year):
#     url = f'https://api.pushshift.io/reddit/submission/comment_ids/{submission_id}'
#     r = requests.get(url, timeout=30)
#     comment_url = "https://api.pushshift.io/reddit/comment/search"
#     dumpFolder = f'/pine/scr/m/t/mtguo/gig/reddit/{subreddit}'
#     # Check the status code, if successful, process the data
#     if r.status_code == 200:
#         response = json.loads(r.text)
#         comment_ids = response['data']
#         print(len(comment_ids))
#         if len(comment_ids)==0:
#             return
#         for comment_id in comment_ids:
#             params = {'ids': comment_id}
#             r = requests.get(comment_url, params=params, timeout=30)
#             if r.status_code == 200:
#                 response = json.loads(r.text)
#                 _object = response['data'][0]
#                 created_utc = _object['created_utc']
#                 timeInIso = datetime.utcfromtimestamp(created_utc).isoformat(' ')
#                 post_line = [_object["author"],subreddit,_object["id"],submission_id, timeInIso, _object["score"], _object['body'].replace(',',' ').replace('\n',' ')]
#                 with open(f"{dumpFolder}/{subreddit}_{year}_comments.csv", 'a') as f:
#                     csv.writer(f).writerow(post_line)
#             else:
#                 print(f"get comments error {r.status_code}")
#             print(response)
#             break
#     else:
#         print(f"get comments id error {r.status_code}")

def fetchObjects(**kwargs):
    # Default paramaters for API query
    params = {
        "sort_type":"created_utc",
        "sort":"asc",
        "size":250,
        "before": 1577854800 # 2020/1/1
        }
    # params = {
    #     "sort_type":"created_utc",
    #     "sort":"asc",
    #     "size":250
    #     }
    # Add additional paramters based on function arguments
    for key,value in kwargs.items():
        params[key] = value

    # Print API query paramaters
    after_time = datetime.utcfromtimestamp(params['after']).isoformat(' ')
    subreddit = params['subreddit']
    print(f"after time {subreddit}: {after_time}")

    # Set the type variable based on function input
    # The type can be "comment" or "submission", default is "submission"
    _type = "submission"
    if 'type' in kwargs and kwargs['type'].lower() == "comment":
        _type = "comment"
    
    # Perform an API request
    r = requests.get(PUSHSHIFT_REDDIT_URL + "/" + _type + "/search/", params=params, timeout=30)

    # Check the status code, if successful, process the data
    if r.status_code == 200:
        response = json.loads(r.text)
        data = response['data']
        sorted_data_by_id = sorted(data, key=lambda x: int(x['id'],36))
        return sorted_data_by_id

def extract_reddit_data(year, subreddit, _type='submission'):
    # Speficify the start timestamp
    max_created_utc = 1546318800  # 01/01/2019 @ 12:00am (UTC)
    # max_created_utc = 1577854800  # 01/01/2020 
    #max_created_utc = 1589116446
    max_id = 0
    dumpFolder = f'/pine/scr/m/t/mtguo/gig/reddit/{subreddit}'
    count = 0
    # While loop for recursive function
    while 1:
        nothing_processed = True
        # Call the recursive function
        objects = fetchObjects(subreddit=subreddit, type=_type,after=max_created_utc)
        if objects==None:
            sleep(5)
            nothing_processed = False
            count += 1
            if count==5:
                print(f"------------------{subreddit}----------------------")
                break
            else:
                continue
        # Loop the returned data, ordered by date
        for _object in objects:
            count = 0
            _id = int(_object['id'],36)
            if _id > max_id:
                nothing_processed = False
                created_utc = _object['created_utc']
                max_id = _id
                if created_utc > max_created_utc: max_created_utc = created_utc
                timeInIso = datetime.utcfromtimestamp(created_utc).isoformat(' ')
                parent_id = _object["parent_id"].split('_')[1]
                post_line = [_object["author"],_object["subreddit"],_object["id"], parent_id, timeInIso, _object["score"], '.' if "body" not in _object else _object["body"].replace(',',' ').replace('\n',' ')]
                #post_line = [_object["author"],_object["subreddit"],_object["id"],_object["title"].replace(","," "), timeInIso, _object["score"], _object["num_comments"], _object["domain"], _object["url"], '.' if "selftext" not in _object else _object["selftext"].replace(',',' ').replace('\n',' ')]
                with open(f"{dumpFolder}/{subreddit}_{year}_comments.csv", 'a') as f:
                    csv.writer(f).writerow(post_line)
        
        # Exit if nothing happened
        if nothing_processed: return
        max_created_utc -= 1

        # Sleep a little before the next recursive function call
        time.sleep(1)

year = 2019
extract_reddit_data(year, 'HITsWorthTurkingFor', "comment")

# Start program by calling function with:
# 1) Subreddit specified
# 2) The type of data required (comment or submission)
# year = 2019
# for subreddit in subreddits:
#     if path.exists(f"/pine/scr/m/t/mtguo/gig/reddit/{subreddit}/{subreddit}_{year}_comments.csv"):
#         remove(f"/pine/scr/m/t/mtguo/gig/reddit/{subreddit}/{subreddit}_{year}_comments.csv")
#         print("remove existing file")
#     extract_reddit_data(year, subreddit, "comment")
#extract_reddit_data("AmazonFlexDrivers", "submission")
# max_created_utc = 1546318800
# objects = fetchObjects(subreddit="AirBnB", type="submission",after=max_created_utc)
# _id = objects[1]['id']
# print(_id)
# fetchComments("AirBnB", _id, 2019)
# jobid = int(sys.argv[1])
# subreddit = subreddits[jobid]
# year = 2019
# dumpFolder = f'/pine/scr/m/t/mtguo/gig/reddit/{subreddit}'
# if path.exists(f"{dumpFolder}/{subreddit}_{year}_comments.csv"):
#     remove(f"{dumpFolder}/{subreddit}_{year}_comments.csv")
# if path.exists(f"{dumpFolder}/{subreddit}_{year}.csv"):
#     data_path = f'{dumpFolder}/{subreddit}_{year}.csv'
#     data = pd.read_csv(data_path, names=['author', 'subreddit', 'id', 'title', 'time', 'score', 'num_comments', 'domain', 'url', 'selftext'])
#     id_list = data['id'].to_list()
#     print(f'fetching comments of {subreddit}, in total {len(id_list)}')
#     for i, _id in enumerate(id_list):
#         fetchComments(subreddit, _id, year)
#         # except:
#         #     with open(f"error_{subreddit}_{year}.out", 'a') as f:
#         #         f.write(f'{_id}\n')
#         if i%10==0:
#             print(f'fetched {i}')
#     print(f'finish fetching {subreddit}')
