
import tweepy
import time
import requests
from bs4 import BeautifulSoup
import html5lib
import random
import os

# Kyes are in keys_format.py

from keys import *

print("Starting Twitter bot, made by Omar Garrido", flush=True )

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

FILE_NAME = 'last_seen_id.txt'

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
url = "https://www.dreamstime.com/photos-images/capybara.html"
html = requests.get(url, headers=headers)
#print(html)
soup = BeautifulSoup(html.text, 'html5lib')
imgHtmlList = soup.find_all("img")
Len_list = len(imgHtmlList)
#print(Len_list, flush=True)

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id


def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return


def get_capybara(imgHtmlList,Len_list):
    capy_Html = imgHtmlList[random.randint(0, Len_list)]
    #print(capy_Html)
    capy_URL = capy_Html['data-src']
    capy = requests.get(capy_URL)
    capy_name = capy_URL.split("/")[-1]
    open(capy_name + '.png', 'wb').write(capy.content)
    #print('descargando: {}.png'.format(capy_name))
    return capy_name


def reply_to_tweets():
    print('retrieving and replying to tweets...', flush=True)
    # DEV NOTE: use 1060651988453654528 for testing.
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    # NOTE: We need to use tweet_mode='extended' below to show
    # all full tweets (with full_text). Without it, long tweets
    # would be cut off.
    mentions = api.mentions_timeline(since_id=last_seen_id)
    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.text, flush=True)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)
        if '#helloworld' in mention.text.lower():
            print('found #helloworld!', flush=True)
            print('responding back...', flush=True)
            api.update_status('@' + mention.user.screen_name +
                              '#HelloWorld back to you!', in_reply_to_status_id=mention.id)
        if '#capibara' in mention.text.lower():
            print ('Capibara requested',flush=True)
            print('Sending Capibara', flush=True)
            capy_name = get_capybara(imgHtmlList,Len_list)
            api.update_status_with_media('@' + mention.user.screen_name + ' A tactical #Capibara has appeared', '{}.png'.format(capy_name),in_reply_to_status_id=mention.id)
            os.remove('{}.png'.format(capy_name))


while True:
    reply_to_tweets()
    time.sleep(15)
