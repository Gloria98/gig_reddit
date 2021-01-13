import requests
import csv
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from os import path, makedirs, cpu_count, environ, remove
from datetime import datetime
from config_uberpeople import *
import nltk
import time
import sys


session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

class Entry(object):
    def __init__(self, tn, ti, aot, tr, tv, ts, aom, ai, mt, mi):
        self.Thread_Name = tn
        self.Thread_ID = ti
        self.Author_of_Thread = aot
        self.Thread_Replies = tr
        self.Thread_Views = tv
        self.Time_Stamp = ts
        self.Author_of_Message = aom
        self.Author_ID = ai
        self.Message_Text = mt
        self.Message_ID = mi


class Entries(object):
    def __init__(self):
        self.EntryList = []

    def addEntry(self, e):
        self.EntryList.append(e)


def process_text(raw_text):
    text_list = nltk.word_tokenize(raw_text)
    paga = " ".join(text_list)
    return paga

def get_next_url(curr_url):
    page = session.get(curr_url, verify=True)
    soup = BeautifulSoup(page.text, 'html.parser')
    nav = soup.findAll('a', 'pageNav-jump pageNav-jump--next')
    if len(nav)==0:
        return ""
    else:
        return nav[0]['href']

def processThread(link, threadNum, employee_writer):
    base_url = 'https://uberpeople.net'
    net_url = "thread"
    curr_url = link
    cont = True
    while net_url != "" and cont:
        cont = processThread_page(curr_url, threadNum, employee_writer)
        net_url = get_next_url(curr_url)
        curr_url = f'{base_url}{net_url}'
        time.sleep(0.5)

def processThread_page(link, threadNum, employee_writer):
    oldest_pd = datetime.strptime(oldest_post_date, '%d/%m/%Y')
    response = session.get(
        link, verify=True)

    soup = BeautifulSoup(response.text, 'html.parser')
    # Initializing the variables
    tn = ""
    ti = ""
    aot = ""
    tr = ""
    tv = ""
    ts = ""
    aom = ""
    ai = ""
    mt = ""
    mi = ""
    ThreadEntryList = Entries()
    AuthorMap = {}
    MessageCount = 1
    authorId = 1
    # This is the Forum Name
    # forum_name = soup.find(
    #     class_='p-body-header')

    # forum_name = "Advice"

    # This will be Thread Title
    thread_title = soup.find(
        class_='p-title')

    thread_title = thread_title.find('h1').text
    print(thread_title)
    # This is the thread_id
    # To be done
    thread_id = threadNum

    # This is the thread author
    thread_author = soup.find(
        class_='p-description')
    thread_author = thread_author.find('a').text
    print(thread_author)
    # Now we go through all the messages and print the data we already have for all of them
    listofMessages = soup.findAll(
        class_='message message--post js-post js-inlineModContainer')

    #nav = soup.findAll('a', 'pageNav-jump pageNav-jump--next')

    for i in range(listofMessages.__len__()):
        tn = thread_title
        ti = thread_id
        aot = thread_author

        timestamp = listofMessages[i].find('time')['title']
        ts = timestamp
        message_time = datetime.strptime(timestamp, '%b %d, %Y at %I:%M %p')
        if message_time < oldest_pd:
            break
        author_of_message = listofMessages[i].find("a").find('img')
        aom = author_of_message
        if author_of_message is not None:
            author_of_message = author_of_message['alt']
            aom = author_of_message

        if author_of_message in AuthorMap:
            ai = AuthorMap[author_of_message]
        else:
            AuthorMap[author_of_message] = authorId
            ai = authorId
            authorId += 1

        messageClass = listofMessages[i].find(
            class_='bbWrapper')

        wrapperText = messageClass.text

        message_text = wrapperText
        mt = process_text(message_text)

        mi = MessageCount
        MessageCount += 1

        

        entry = Entry(tn, ti, aot, tr, tv, ts, aom, ai, mt, mi)
        ThreadEntryList.addEntry(entry)

    for e in ThreadEntryList.EntryList:
        employee_writer.writerow(
                [e.Thread_Name, e.Thread_ID, e.Author_of_Thread, e.Time_Stamp, e.Author_of_Message,
                 e.Author_ID, e.Message_Text, e.Message_ID])
    if len(ThreadEntryList.EntryList)==0:
        return False
    else: 
        return True



def processPage(pageLink, employee_writer):
    oldest_pd = datetime.strptime(oldest_post_date, '%d/%m/%Y')
    allAdviceThreadsRequest = session.get(
        pageLink, verify=True)

    AdviceSoup = BeautifulSoup(allAdviceThreadsRequest.text, 'html.parser')
    allAdviceThreads = AdviceSoup.findAll(
        class_='structItem-cell structItem-cell--main')

    allLinks = []

    for thread in allAdviceThreads:
        title = thread.find(
            class_='structItem-title')

        minor = thread.find(
            class_='structItem-minor')

        jumps = minor.find(
            class_='structItem-pageJump')

        link = title.find('a')['href']
        date = minor.find('time')['data-date-string']
        post_time = datetime.strptime(date, '%b %d, %Y')
        totalString = 'https://www.uberpeople.net' + link
        if post_time > oldest_pd:
            allLinks.append(totalString)

            if jumps is not None:
                j = jumps.findAll('a')
                if j is not None:
                    for sec in j:
                        totalLink = 'https://www.uberpeople.net' + sec['href']
                        allLinks.append(totalLink)

    # This will process the link base
    threadNum = 1
    for link in allLinks:
        print("Thread " + str(threadNum) + " of " + str(allLinks.__len__()))
        try:
            processThread(link, threadNum, employee_writer)
        except:
            continue
        threadNum += 1
    if len(allLinks)==0:
        return False
    else: 
        return True



def extract_forum(forum):
    dump_folder = f'/pine/scr/m/t/mtguo/gig/uberpeople/{forum}/'
    try:    
        if not path.exists(dump_folder): makedirs(dump_folder) #Create dir if required
    except: pass
    # save to csv
    dump_file = f'{dump_folder}/{forum}.csv'
    if path.exists(dump_file):
        remove(dump_file)
    with open(dump_file, mode='a', encoding="utf-8", newline='') as employee_file:
        employee_writer = csv.writer(
            employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        employee_writer.writerow(
            ['Thread_Name', 'Thread_ID', 'Author_Of_Thread', 'Time_Stamp', 'Author_of_Message',
             'Author_ID', 'Message_Text', 'Message_ID'])
        base_url = 'https://uberpeople.net'
        curr_url = f'{base_url}/forums/{forum}'
        net_url = "forum"
        cont = True
        while net_url != "" and cont:
            print(curr_url)
            cont = processPage(curr_url, employee_writer)
            net_url = get_next_url(curr_url)
            curr_url = f'{base_url}{net_url}'


# for forum in forums:
#     if path.exists(f"/pine/scr/m/t/mtguo/gig/uberpeople/{forum}/{forum}.csv"):
#         remove(f"/pine/scr/m/t/mtguo/gig/uberpeople/{forum}/{forum}.csv")
jobid = int(sys.argv[1])
forum = forums[jobid]
extract_forum(forum)

# dump_folder = f'/pine/scr/m/t/mtguo/gig/uberpeople/try/'
# try:    
#     if not path.exists(dump_folder): makedirs(dump_folder) #Create dir if required
# except: pass
# dump_file = f'/pine/scr/m/t/mtguo/gig/uberpeople/try/try.csv'
# with open(dump_file, mode='a', encoding="utf-8", newline='') as employee_file:
#     employee_writer = csv.writer(
#         employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#     link = "https://uberpeople.net/forums/Tips/page-197"
#     processPage(link, employee_writer)
#         employee_writer.writerow(
#             ['Thread_Name', 'Thread_ID', 'Author_Of_Thread', 'Time_Stamp', 'Author_of_Message',
#              'Author_ID', 'Message_Text', 'Message_ID'])
#         processThread("https://uberpeople.net/threads/we-got-the-600-plus-1200.408505/page-14", 1, employee_writer)