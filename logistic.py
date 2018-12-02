import json, re
import sklearn.linear_model as sk
from time import sleep
import statistics
from datetime import datetime
from sklearn.decomposition import TruncatedSVD
# import matplotlib.pyplot as plt
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

# with open("orig_content_train.json") as f:
#     data = json.load(f)

# age of account

with open("orig_en_train.json") as f:
    data = json.load(f)

split = len(data)//2
train = data[:split]
valid = data[split:]

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

bow = TfidfVectorizer()  # max_features=100
X_train = bow.fit_transform(corpus).toarray()
svd = TruncatedSVD(n_components=20)
X_train = svd.fit_transform(X_train)


corpus = []
for d in valid:
    corpus.append(process_tweet(d['tweet_text']))

X_valid = bow.transform(corpus).toarray()
X_valid = svd.transform(X_valid)



# hashtags = {}
# for d in train:
#     curr_hashtags = d['hashtags']
#     like_count = int(d['like_count'])
#     if curr_hashtags:
#         curr_hashtags = curr_hashtags[1:-1].split(', ')
#         if not (len(curr_hashtags) == 1 and curr_hashtags[0] == ''):
#             for tag in curr_hashtags:
#                 if tag in hashtags:
#                     hashtags[tag].append(like_count)
#                 else:
#                     hashtags[tag] = [like_count]
#
# account_likes = {}
# for d in train:
#     user = d['userid']
#     if user in account_likes:
#         account_likes[user].append(int(d['like_count']))
#     else:
#         account_likes[user] = [int(d['like_count'])]
#
# for user, likes in account_likes.items():
#     account_likes[user] = statistics.median(likes)
#
#
# popular_hashtags = {'sports': 0, 'politics': 1, 'local': 2, 'world': 3, 'news': 4, 'SanDiego': 5, 'Syria': 6, \
#                     'ISIS': 7, 'WakeUpAmerica': 8, 'Trump': 9, 'business': 10, 'Chicago': 11, 'health': 12, \
#                     'love': 13, 'TopNews': 14, 'BLM': 15, 'PoliceBrutality': 16, 'Obama': 17, 'BlackTwitter': 18, \
#                     'Trump2016': 19}


def get_features(d):
    tweet_text = process_tweet(d['tweet_text'])
    features = bow.transform([tweet_text])[0].toarray()
    # features = svd.transform(BOW)[0]


    # curr_hashtags = d['hashtags'][1:-1].split(', ')
    # hashtag_features = [0 for i in range(len(popular_hashtags))]
    # for ht in curr_hashtags:
    #     if ht in popular_hashtags:
    #         ht_index = popular_hashtags[ht]
    #         hashtag_features[ht_index] = 1
    # features.extend(hashtag_features)
    # user =  d['userid']
    # if user in account_likes:
    #     features.append(account_likes[user])
    # else:
    #     features.append(0)

    return features

# X_train = [get_features(d) for d in train]
# X_valid = [get_features(d) for d in valid]
y_train = [int(d['like_count']) != 0 for d in train]
y_valid = [int(d['like_count']) != 0 for d in valid]

lr = sk.LogisticRegression(C=1.0, fit_intercept=True, class_weight=None, random_state=1, max_iter=100).fit(X_train, y_train)

predictions = lr.predict(X_train)
print(sum(predictions))
print(lr.score(X_train, y_train))
print(lr.score(X_valid, y_valid))

"""
____orig_en_train____

bias only
0.7868
0.78832

only follower count
0.79312
0.79332

mean likes:
0.82084
0.82252

mean likes and follower count:
0.80752
0.80656

mean likes and time:
0.7868
0.78832

mean likes and hashtag popularity:
0.82156
0.82196

follower count, time, hashtag popularity, mean tweets
0.81932
0.81964

hashtag popularity:
0.7868
0.78832

mean and BOW 5 hashtags:
0.82216
0.82376

mean and BOW 10 hashtags:
0.82268
0.82384

mean, BOW 5 hashtags, and timestamp:
0.7868
0.78832

mean, BOW 10 ht, hashtag popularity, URL, follower count:
0.81268
0.81132

no better than bias only:
follower count, time, popular hashtags, median tweets, URLs
BOW with PCA 10 features
BOW top 10 words

BOW with PCA

BOW top 100 words:
0.78792
0.78504

BOW 5 hashtags:
0.7886
0.78968

median likes:
0.821
0.82172

median likes with 10 BOW hashtags:
0.82064
0.82092

___en, noURLs___
0.98808
0.98784


"""