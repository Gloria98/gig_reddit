import matplotlib
matplotlib.use('Agg')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.nonparametric.smoothers_lowess import lowess

from nltk.tokenize import word_tokenize
import string
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")
from config import subreddits, dumpFolder_base, verbs, stem_verbs, verbs_small, lem_verbs
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from absl import app
from absl import flags
FLAGS = flags.FLAGS
import spacy

'''
This file contains code that lemmatize posts, extract posts with collective action words as listed in config.py
'''

flags.DEFINE_integer(
    "subreddit", 0, "The subreddit to process.", lower_bound=0
)

# get stemmed keywords (in config.py), you may not need this
def stem_keywords(k_list):
    new_list = []
    for k in k_list:
        words = word_tokenize(k)
        new_k = ' '.join(str(stemmer.stem(j)) for j in words)
        new_list.append(new_k)
    print(new_list)

# get lemmatized keywords (in config.py), you may not need this
def lem_keywords(k_list, nlp):
    doc = nlp(" ".join(k_list)) 
    texts_out = [token.lemma_ for token in doc]
    print(texts_out)
    return texts_out

# read all the post from the subreddit
# input: subreddit name, a full list in config.py
# output: a pandas dataframe containing all the posts
def read_subred(subreddit):
    dumpFolder = f'{dumpFolder_base}/{subreddit}'
    file_name1 = f'{dumpFolder}/{subreddit}_2019.csv'
    file_name2 = f'{dumpFolder}/{subreddit}_2020.csv'

    file1 = pd.read_csv(file_name1, names=['author', 'subreddit', 'id', 'title', 'time', 'score', 
                                            'num_comments', 'domain', 'url', 'body'])
    file2 = pd.read_csv(file_name2, names=['author', 'subreddit', 'id', 'title', 'time', 'score', 
                                            'num_comments', 'domain', 'url', 'body'])
    post_df = pd.concat([file1, file2], sort=False)
    post_df = post_df.reset_index(drop=True)
    print(len(post_df))
    return post_df

def lemmatization(texts, nlp):
    """https://spacy.io/api/annotation"""
    
    doc = nlp(texts) 
    texts_out = [token.lemma_ for token in doc]
    texts_out = " ".join(texts_out)
    return texts_out

# lemmatize the how dataset
# input: a pandas dataframe where each row is a post
# output: a list of post content (title +  body)
def process_dset(subred_df):
    content_list = []
    nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
    print("finish loading en core")
    for idx, row in subred_df.iterrows():
        content = str(row['title']) + " " + str(row['body'])
        content = content.lower()
        content_list.append(lemmatization(content, nlp))
    return content_list

# process the how dataset, do lemmatization to the post content, and then output
# the processed version to a new csv file to save effort later on
# input: subreddit name
# output: None
def process_subreddit(subreddit):
    dumpFolder = f'{dumpFolder_base}/{subreddit}'
    post_df = read_subred(subreddit)
    content_list = process_dset(post_df)
    processed_df = pd.DataFrame({"stem_content": content_list})
    processed_df.to_csv(f'{dumpFolder}/{subreddit}_processed3.csv', index=False)

# judge whether the sentence s contain any of the keyword in k_list
# input: s (string), k_list (keyword list, a list of string)
# output: true is s contains at least one word in k_list, otherwise false
def judge_action(s, k_list):
    s_words = word_tokenize(s)
    for k in k_list:
        k_words = word_tokenize(k)
        if len(k_words)==1:
            if k_words[0] in s_words:
                # print(k)
                return True
        elif k_words[0] in s_words:
            index = s_words.index(k_words[0])
            match = True
            for i in range(len(k_words)):
                if len(s_words)>index+i and k_words[i]!=s_words[index+i]:
                    match=False
            if match:
                # print(k)
                return True
    return False

# extract all the collective action posts from the whole dataset and save them to a csv file
# input: None
# output: None
def action_info():
    all_action_post = pd.DataFrame(columns=['subreddit', 'title', 'body', 'author', 'time', 'score', 'num_comments'])
    for subreddit in subreddits:
        dumpFolder = f'{dumpFolder_base}/{subreddit}'
        content_df = pd.read_csv(f'{dumpFolder}/{subreddit}_processed3.csv', lineterminator='\n')
        df = read_subred(subreddit)
        action_df = pd.DataFrame(columns=['title', 'body', 'author', 'time', 'score', 'num_comments'])
        k_list = lem_verbs
        for idx, row in df.iterrows():
            s = str(content_df['stem_content'][idx])
            if judge_action(s, k_list):
                action_df = action_df.append(row[['title', 'body', 'author', 'time', 'score', 'num_comments']])
        action_df['subreddit'] = subreddit
        all_action_post = pd.concat([all_action_post, action_df], ignore_index=True)
        print(f"{subreddit}: {len(action_df)}")
        print(len(all_action_post))
    all_action_post.to_csv(f"action_ext/all_new.csv", index=False)

# def check_words():
#     all_posts = pd.read_csv("action_ext/post_topic_6_2.csv", lineterminator='\n')
#     print(len(all_posts))
#     topic = float(4)
#     sub_posts = all_posts[all_posts['Dominant_Topic']==topic]
#     content_list = process_dset(sub_posts)
#     print(len(content_list))
#     k_list = ['full time']
#     total = 0
#     for c in content_list:
#         if judge_action(c, k_list):
#             total+=1
#     print(total)




def main(_):
    subreddit = subreddits[FLAGS.subreddit]
    process_subreddit(subreddit)
    # for subreddit in subreddits:
    #     print(f"-----------{subreddit}-----------")
    #     process_subreddit(subreddit)

def cal():
    total = 0
    for subreddit in subreddits:
        df = pd.read_csv(f"action_ext/{subreddit}_l.csv", lineterminator='\n')
        print(f"{subreddit} : {len(df)}")
        total += len(df)
    print(total)

# if __name__ == "__main__":
#     app.run(main)
# pd.read_csv(f"action_ext/AirBnB.csv", lineterminator='\n')
# cal()
check_words()