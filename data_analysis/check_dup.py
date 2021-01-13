'''
check duplicate posts, you may not need this
'''
import pandas as pd
import shutil
from os import path

def check_dup_reddit(year):
    subreddits = ["airbnb_hosts", "AirBnB", "couchsurfing", "vrbo", "CaregiverSupport", "Nanny", "AmazonFlexDrivers", 
            "InstacartShoppers", "instacart", "ShiptShoppers", "doordash", "doordash_drivers",
            "UberEATS", "grubhubdrivers", "postmates", "FieldAgent", "TaskRabbit", "RoverPetSitting",
            "Etsy", "EtsySellers", "uber", "uberdrivers", "lyftdrivers", "Lyft", "GetAround",
            "mturk", "TurkerNation", "vipkid", "Upwork", "kaggle", "Fiverr", "crowdSPRING", "MusicEd"]
    for subreddit in subreddits:
        if path.exists(f"/pine/scr/m/t/mtguo/gig/reddit/{subreddit}/{subreddit}_{year}.csv")==False:
            continue
        records = pd.read_csv(f'/pine/scr/m/t/mtguo/gig/reddit/{subreddit}/{subreddit}_{year}.csv', names = ["author","subreddit", "id", "title", "time","score","num_comments","domain","url","selftext"])
        if len(records) != len(records['id'].unique()):
            print(f"detect duplicate of {subreddit} {year}")
            deduped = records.drop_duplicates(["id"])
            deduped.to_csv(f'/pine/scr/m/t/mtguo/gig/reddit/{subreddit}/temp_{subreddit}_{year}.csv', index=False)
            shutil.move(f'/pine/scr/m/t/mtguo/gig/reddit/{subreddit}/temp_{subreddit}_{year}.csv', f'/pine/scr/m/t/mtguo/gig/reddit/{subreddit}/{subreddit}_{year}.csv')


def check_dup_uberpeople():
    forums = ['Coronavirus', 'AmazonFlex', "UberEATS", "Lyft", "Tips", "confessions",
            "people", "Complaints", "Pay", "Technology", "Ratings", "Licensed", "Vehicles", "Insurance", 
            "Taxes", "Gratuity", "Surge", "news", "Autonomous", "Advocacy", "Notifications", "Deliver",
            "Quit"]
    for forum in forums:
        if path.exists(f"/pine/scr/m/t/mtguo/gig/uberpeople/{forum}/{forum}.csv")==False:
            continue
        records = pd.read_csv(f'/pine/scr/m/t/mtguo/gig/uberpeople/{forum}/{forum}.csv', names = ["thread_name","thread_id", "thread_author", "time", "message_author","author_id","message","message_id"])
        if len(records) != len(records['message_id'].unique()):
            print(f"detect duplicate of {forum}")
    
check_dup_uberpeople()
