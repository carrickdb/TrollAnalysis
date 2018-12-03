import json, statistics, pprint, re
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.ensemble import AdaBoostClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
from time import sleep
from datetime import datetime
import numpy as np
from pprint import pprint

with open("orig_en_train.json") as f:
    data = json.load(f)

split = len(data)//2
train = data[split:]
valid = data[:split]

X_train = []
y_train = []

account_likes = {}
tweets = {}
tweet_clients = defaultdict(int)
for d in train:
    tweet_clients[d['tweet_client_name']] += 1
    # tweet_text = d['tweet_text']
    # if tweet_text in tweets:
    #     tweets[tweet_text].append(int(d['like_count']))
    # else:
    #     tweets[tweet_text] = [int(d['like_count'])]
    user = d['userid']
    if user in account_likes:
        account_likes[user].append(int(d['like_count']))
    else:
        account_likes[user] = [int(d['like_count'])]
    if int(d['like_count']) > 10:
        pprint(d)
        assert False


clients = {}
i = 0
for client, count in tweet_clients.items():
    clients[client] = i
    i += 1

for user, likes in account_likes.items():
    account_likes[user] = statistics.median(likes)

popular_hashtags = {'sports': 0, 'politics': 1, 'local': 2, 'world': 3, 'news': 4, 'SanDiego': 5, 'Syria': 6, \
                    'ISIS': 7, 'WakeUpAmerica': 8, 'Trump': 9, 'business': 10, 'Chicago': 11, 'health': 12, \
                    'love': 13, 'TopNews': 14, 'BLM': 15, 'PoliceBrutality': 16, 'Obama': 17, 'BlackTwitter': 18, \
                    'Trump2016': 19}

def process_tweet(tweet):
    if len(re.findall("(https://[^\s]+)", tweet)) > 0:
        tweet = re.sub("(https://[^\s]+)", "", tweet)
    if len(re.findall("(http://[^\s]+)", tweet)) > 0:
        tweet = re.sub("(http://[^\s]+)", "", tweet)
    if len(re.findall('@[^\s@]+', tweet)) > 0:
        tweet = re.sub('@[^\s@]+', "", tweet)
    if len(re.findall("(#[^#\s]+)", tweet)) > 0:
        tweet = re.sub("(#[^#\s]+)", "", tweet)
    return tweet

corpus = []
for d in train:
    corpus.append(process_tweet(d['tweet_text']))
    # corpus.append(d['tweet_text'])

bow = TfidfVectorizer(min_df=0.01, max_df=0.95)  #
bow.fit(corpus)
print(len(bow.vocabulary_))

def get_features(d):
    features = []

    # mean # of likes
    user =  d['userid']
    if user in account_likes:
        features.append(0)
        features.append(account_likes[user])
    else:
        features.append(1)
        features.append(0)

    # Twitter client
    client_features = [0 for i in range(len(clients))]
    client = d['tweet_client_name']
    if client in clients:
        features.append(0)
        client_index = clients[client]
        client_features[client_index] = 1
    else:
        features.append(1)
    features.extend(client_features)

    # popular hashtags
    curr_hashtags = d['hashtags'][1:-1].split(', ')
    hashtag_features = [0 for i in range(len(popular_hashtags))]
    for ht in curr_hashtags:
        if ht in popular_hashtags:
            ht_index = popular_hashtags[ht]
            hashtag_features[ht_index] = 1
    features.extend(hashtag_features)

    # url
    if 'https://t.co' in d['tweet_text'] or d['urls'] != '':
        features.append(1)
    else:
        features.append(0)

    # follower count
    features.append(int(d['follower_count']))

    # BOW
    features.extend(bow.transform([d['tweet_text']]).toarray()[0])

    # Time since epoch
    date = datetime.strptime(d['tweet_time'], '%Y-%m-%d %H:%M')
    features.append(date.timestamp())

    # Time of day
    minutes_in_day = 24 * 60
    minutes = date.hour * 60 + date.minute
    sin_time = np.sin(2 * np.pi * minutes / minutes_in_day)
    cos_time = np.cos(2 * np.pi * minutes / minutes_in_day)

    features.append(sin_time)
    features.append(cos_time)
    return features


for d in train:
    X_train.append(get_features(d))
    if d['like_count'] == '0':
        y_train.append(0)
    else:
        y_train.append(1)

X_valid = []
y_valid = []
for d in valid:
    X_valid.append(get_features(d))
    like_count = int(d['like_count'])
    if like_count == 0:
        y_valid.append(0)
    else:
        y_valid.append(1)

# gpc = GaussianProcessClassifier(1.0 * RBF(1.0))
# gpc.fit(X_train, y_train)
#
# print(gpc.score(X_train, y_train))
# print(gpc.score(X_valid, y_valid))

ada = AdaBoostClassifier()
ada.fit(X_train, y_train)
print(ada.score(X_train, y_train))
print(ada.score(X_valid, y_valid))

# predictions = ada.predict(X_train)
#
# j = 0
# for i in range(len(train)):
#     if predictions[i] != y_train[i]:
#         print("prediction:", predictions[i], "|  reality:", y_train[i])
#         pprint.pprint(train[i])
#
#         j += 1
#     if j > 10:
#         break

"""
only mean likes per account
0.8418
0.84044

mean likes, top 10 hashtags
0.84204
0.8404

mean likes, top 10 hashtags, follower count, url
0.84304
0.84132

median likes, top 10 hashtags, follower count, url
0.84588
0.84304

mean likes, follower count, url
0.84276
0.84124

mean likes, top 10 hashtags, follower count
0.84212
0.84044

mean likes, top 10 hashtags, url
0.84312
0.842

mean likes, url
0.84624
0.84268

mean likes, follower count
0.8418
0.84044

median likes
0.84448
0.84016

median likes, url
0.84624
0.84268

url
0.7868
0.78832

copied tweets
0.99932
0.78776

copied tweets and median likes
0.99932
0.78796

BOW (100)
0.787
0.7882

median likes, top 10 hashtags, follower count, url, 100 BOW (w/o hashtags)
0.84572
0.84244

3 classes, mean likes
0.84448
0.79048

client
0.78716
0.78856

client, median likes
0.84432
0.84296

client, median likes, url
0.84616
0.84268

median likes, top 10 hashtags, follower count, url, 100 BOW (w/o hashtags), client
0.84676
0.84336

BOW with min/max df
0.78836
0.78952

BOW with min/max df, median likes
0.8448
0.8398

BOW with min/max df, median likes, top 10 hashtags, follower count, url, client
0.84592
0.84304

BOW with min/max df, median likes, top 10 hashtags, follower count, url, client, time since epoch
0.84804
0.84648

BOW with min/max df, median likes, top 10 hashtags, follower count, url, client, time since epoch, time of day
0.84844
0.8466
"""