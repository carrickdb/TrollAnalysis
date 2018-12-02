# #!/usr/bin/env python3

# import tensorflow as tf
#import numpy as np
#import sklearn.metrics
import json, datetime, math
from sklearn import svm
import datetime
# import matplotlib.pyplot as plt

"""
baseline model:
    just predict 0 for everything

other ideas:
    if we've seen the user before, predict whether they usually have likes. Else, 0
    based on # of followers
"""

# with open("orig_content_train.json") as f:
#     data = json.load(f)

with open("train_mini.json") as f:
    data = json.load(f)
    # print("number of tweets", len(data))
split = len(data)//2
train = data[:split]
valid = data[split:]

# the_master = '4272870988'
# the_biggest_loser = '2943515140'

def get_accuracy(predictions, y):
    right = 0
    for i in range(len(predictions)):
        if predictions[i] == y[i]:
            right += 1
    return right/len(predictions)

def create_features(data_set):
    X = []
    y = []
    unliked = []
    liked = []
    for d in data_set:
        # int(d['follower_count'])
        features = [1]
        if 'https://t.co' in d['tweet_text']:
            features.append(1)
        else:
            features.append(0)
        features.append(int(d['follower_count']))
        X.append(features)
        if d['like_count'] == '0':
            y.append(0)
            # unliked.append(d)
        else:
            y.append(1)
            # liked.append(d)

    # for liked_sets in [liked, unliked]:
    #     print("_____________________")
    #     for d in liked_sets[:10]:
    #         print("Screen name:", d['user_screen_name'])
    #         print("Location:", d['user_reported_location'])
    #         print("Follower count:", d['follower_count'])
    #         print("Tweet time", d['tweet_time'])
    #         print("in reply to:", d['in_reply_to_tweetid'])
    #         print("hashtags:", d['hashtags'])
    #         print("urls:", d['urls'])
    #         print("user_mentions:", d['user_mentions'])
    #         print("tweet text:", d['tweet_text'])
    #         print("like count:", d['like_count'])
    #         print()
    return X, y


X_train, y_train = create_features(train)
X_valid, y_valid = create_features(valid)

clf = svm.SVC(C=100, kernel='linear', class_weight='balanced')
print("initialized SVM")
clf.fit(X_train, y_train)
print("created model")
train_pred = clf.predict(X_train)
print("predicted values for training set")
valid_pred = clf.predict(X_valid)
print("predicted values for validation set")

# graph 1-D follower count?

train_compare = [(train_pred[i] == y_train[i]) for i in range(len(y_train))]
valid_compare = [(valid_pred[i] == y_valid[i]) for i in range(len(y_valid))]

train_acc = sum(train_compare) * 1.0 / len(train_compare)
valid_acc = sum(valid_compare) * 1.0 / len(valid_compare)

print("training accuracy:", train_acc)
print("validation accuracy:", valid_acc)


# # Guess 0 for everything
# for data_set in [train, valid]:
#     y = []
#     predictions = []
#     for d in data_set:
#         if int(d['like_count']) != 0:
#             y.append(1)
#         else:
#             y.append(0)
#     print(get_accuracy(predictions, y))


"""
# the biggest loser: All but 4 of 1541 tweets with 0 likes!!!

total likes in training set 932474

features: followers, num tweets, time since account start, number of exclamation points,
emojis, hashtags, bag of words, account language, tweet language, whether it has a link or not,
length of tweet

average number of followers for tweets with 0 likes:

___0/not 0 classification___
just guess 0 for everything:
train: 0.7790061834165238
valid: 0.7816434478134545

___SVM with just follower count as feature___
training accuracy: 0.771
validation accuracy: 0.782

__SVM with follower count and https://t.co___
training accuracy: 0.771
validation accuracy: 0.782

___SVM with follower count, tweet time___

"""

# global_average = total_likes/len(data)
