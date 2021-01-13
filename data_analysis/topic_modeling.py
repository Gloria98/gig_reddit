import matplotlib
matplotlib.use('Agg')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 16})
from nltk.tokenize import word_tokenize
import string
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")
from config import subreddits, dumpFolder_base, verbs, stem_verbs, verbs_small
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
import csv
from absl import app
from absl import flags
FLAGS = flags.FLAGS

import re
from pprint import pprint
from collections import Counter
import pickle
import json

# Gensim
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
# Plotting tools
# import pyLDAvis
# import pyLDAvis.gensim  # don't skip this
import matplotlib.pyplot as plt
#TF-IDF
from sklearn.feature_extraction.text import TfidfTransformer,CountVectorizer
# spacy for lemmatization
import spacy
#nltk
from nltk.corpus import stopwords
# Enable logging for gensim - optional
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.ERROR)

flags.DEFINE_integer(
    "num_topics", 10, "The number of topics to model on.", lower_bound=0
)

# read all the collective action posts
def read_posts():
    all_posts = pd.read_csv("action_ext/all_new.csv", lineterminator='\n')
    all_content = []
    for idx, row in all_posts.iterrows():
        all_content.append(str(row["title"]) + " " + str(row["body"]))
    return all_content

def sent_to_words(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))  # deacc=True removes punctuations

def preprocess(data):
    data = [re.split('https:\/\/.*', str(x))[0] for x in data]
    # Remove new line characters
    data = [re.sub('\s+', ' ', sent) for sent in data]

    # Remove distracting single quotes
    data = [re.sub("\'", "", sent) for sent in data]

    data_words = list(sent_to_words(data))

    return data_words

def get_phraser(data_words):
    # Build the bigram and trigram models
    bigram = gensim.models.Phrases(data_words, min_count=5, threshold=100) # higher threshold fewer phrases.
    trigram = gensim.models.Phrases(bigram[data_words], threshold=100)

    # Faster way to get a sentence clubbed as a trigram/bigram
    bigram_mod = gensim.models.phrases.Phraser(bigram)
    trigram_mod = gensim.models.phrases.Phraser(trigram)

    return bigram_mod, trigram_mod

def remove_stopwords(texts):
    stop_words = stopwords.words('english')
    return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]

def make_bigrams(texts, bigram_mod):
    return [bigram_mod[doc] for doc in texts]

def make_trigrams(texts, bigram_mod, trigram_mod):
    return [trigram_mod[bigram_mod[doc]] for doc in texts]

def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
    """https://spacy.io/api/annotation"""
    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent)) 
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return texts_out

def get_lem_content():
    all_content = read_posts()
    data_words = preprocess(all_content)
    # print(data_words[0])
    bigram_mod, trigram_mod = get_phraser(data_words)
    # Remove Stop Words
    data_words_nostops = remove_stopwords(data_words)

    # Form Bigrams
    data_words_bigrams = make_bigrams(data_words_nostops, bigram_mod)

    # Do lemmatization keeping only noun, adj, vb, adv
    data_lemmatized = lemmatization(data_words_bigrams, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])
    # print(trigram_mod[bigram_mod[data_words[0]]])
    with open('action_ext/all_post_new.json', 'w', encoding='utf-8') as f:
        json.dump(data_lemmatized, f, ensure_ascii=False, indent=4)

# train LDA
def mallet_modeling(data_lemmatized, num_topics):
    print("start modeling")
    # Create Dictionary
    id2word = corpora.Dictionary(data_lemmatized)

    # Create Corpus
    texts = data_lemmatized

    # Term Document Frequency
    corpus = [id2word.doc2bow(text) for text in texts]

    # # training
    # mallet_path = 'mallet-2.0.8/bin/mallet' # update this path
    # ldamallet = gensim.models.wrappers.LdaMallet(mallet_path, corpus=corpus, num_topics=num_topics, id2word=id2word)
    # ldamallet.save("ldamallet_model_6_3.model")
    
    # loading
    ldamallet = gensim.models.wrappers.LdaMallet.load("ldamallet_model_6_2.model")
    pprint(ldamallet.print_topics(num_topics=20, num_words=10))
    # Compute Perplexity
    
    # Compute Coherence Score
    coherence_model_ldamallet = CoherenceModel(model=ldamallet, texts=data_lemmatized, dictionary=id2word, coherence='c_v')
    coherence_ldamallet = coherence_model_ldamallet.get_coherence()
    print('\nCoherence Score: ', coherence_ldamallet)
    return ldamallet, corpus, id2word, coherence_ldamallet


def format_topics_sentences(ldamodel, corpus):
    # Init output
    sent_topics_df = pd.DataFrame()

    # Get main topic in each document
    for i, row in enumerate(ldamodel[corpus]):
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        # Get the Dominant topic, Perc Contribution and Keywords for each document
        for j, (topic_num, prop_topic) in enumerate(row):
            if j == 0:  # => dominant topic
                wp = ldamodel.show_topic(topic_num)
                topic_keywords = ", ".join([word for word, prop in wp])
                sent_topics_df = sent_topics_df.append(pd.Series([int(topic_num), round(prop_topic,4), topic_keywords]), ignore_index=True)
            else:
                break
    sent_topics_df.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']

    # Add original text to the end of the output
    # contents = pd.Series(texts)
    # sent_topics_df = pd.concat([sent_topics_df, contents], axis=1)
    return sent_topics_df

def train_lda():
    with open('action_ext/all_post_new.json', 'r', encoding='utf-8') as f:
        data_lemmatized = json.load(f)
    # print(len(data_lemmatized))
    # best_score = 0
    # for i in range(3, 12):
    # ldamallet, corpus, id2word, score = mallet_modeling(data_lemmatized, 12)
        # if score > best_score:
        #     best_score = score
        #     ldamallet.save("ldamallet_model.model")
    # post_line = [12, score]
    # with open("topic_opt5.csv", 'a') as f:
    #     csv.writer(f).writerow(post_line)
    # for i in range(8, 13):
    #     score_sum = 0
    #     for j in range(5):
    #         ldamallet, corpus, id2word, score = mallet_modeling(data_lemmatized, i)
    #         score_sum += score
    #     post_line = [i, float(score_sum/5.0)]
    #     with open("topic_opt4.csv", 'a') as f:
    #         csv.writer(f).writerow(post_line)
    ldamallet, corpus, id2word, score = mallet_modeling(data_lemmatized, 6)

# get the topic information of each post and save it to a csv file
def post_topic():
    with open('action_ext/all_post_new.json', 'r', encoding='utf-8') as f:
        data_lemmatized = json.load(f)
    ldamallet, corpus, id2word, _ = mallet_modeling(data_lemmatized, 6)
    sent_topics_df = format_topics_sentences(ldamallet, corpus)
    print(len(sent_topics_df))
    all_post = pd.read_csv("action_ext/all_new.csv", lineterminator='\n')
    sent_topics_df['subreddit'] = all_post['subreddit']
    sent_topics_df['title'] = all_post['title']
    sent_topics_df['body'] = all_post['body']
    sent_topics_df['score'] = all_post['score']
    sent_topics_df['num_comments'] = all_post['num_comments']
    sent_topics_df['author'] = all_post['author']
    sent_topics_df['time'] = all_post['time']
    sent_topics_df.to_csv("action_ext/post_topic_6_2.csv", index=False)

# print the top 5 subreddit that generate most content for each topic
def sub_for_topic():
    all_posts = pd.read_csv("action_ext/post_topic_6_2.csv", lineterminator='\n')
    print(len(all_posts))
    num_post = 0
    for i in range(8):
        topic = float(i)
        sub_posts = all_posts[all_posts['Dominant_Topic']==topic]
        print(len(sub_posts))
        num_post += len(sub_posts)
        sub_for_topic = sub_posts.groupby("subreddit").size().sort_values(ascending=False)
        print(sub_for_topic[:5])
    print(num_post)

# get the top post from each topic and save it to a csv file
# ->232, change the value used to sort
def post_for_topic():
    all_posts = pd.read_csv("action_ext/post_topic_6_2.csv", lineterminator='\n')
    print(len(all_posts))
    for i in range(6):
        topic = float(i)
        sub_posts = all_posts[all_posts['Dominant_Topic']==topic]
        post_for_topic = sub_posts.sort_values(['Perc_Contribution'], ascending=False)
        total=0
        for j, row in post_for_topic.iterrows():
            if total==10:
                break
            post_line = [i, row['subreddit'], row['title'], row['body']]
            with open("action_ext/top_posts_new_6_2.csv", 'a') as f:
                csv.writer(f).writerow(post_line)
            total += 1

# plot the scores of lda
def plot_score():
    df = pd.read_csv("topic_opt5.csv", names=['num_topic', 'score'])
    plt.figure(figsize=(9,6))
    plt.xlim(4,26)
    plt.xticks(np.arange(4, 26, step=2))
    plt.plot(df['num_topic'].values, df['score'].values, 'o-',)
    plt.ylabel('Coherence score')
    plt.xlabel('Number of topic')
    plt.grid()
    plt.savefig('topic_opt.png')

train_lda()
