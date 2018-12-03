#!/usr/bin/env python3

import json, statistics
from pprint import pprint
from collections import defaultdict
from datetime import datetime
import matplotlib.pyplot as plt

train_file = "orig_en_train.json"
# test_file = "orig_en_test.json"

with open(train_file) as f:
    tweets = json.load(f)

zero_likes = 0
likes = []

first = float("inf")
last = float("-inf")

# accounts = set()
for d in tweets:
    like_count = int(d['like_count'])
    likes.append(like_count)
    # accounts.add(d['userid'])
    # timestamp = datetime.strptime(d['tweet_time'], '%Y-%m-%d %H:%M').timestamp()
    # if timestamp < first:
    #     first = timestamp
    # if timestamp > last:
    #     last = timestamp


y = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
plt.hist(likes, bins=y)
plt.title("Distribution of likes (0-10)")
plt.xlabel("Number of likes")
plt.ylabel("Number of tweets")
plt.show()

y = [10, 20, 30, 40, 50, 60, 70 ,80, 90, 100]
plt.hist(likes, bins=y)
plt.title("Distribution of likes (10-100)")
plt.xlabel("Number of likes")
plt.ylabel("Number of tweets")
plt.show()

y = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
plt.hist(likes, bins=y)
plt.title("Distribution of likes (100-1000)")
plt.xlabel("Number of likes")
plt.ylabel("Number of tweets")
plt.show()
# first = datetime.fromtimestamp(first).isoformat()
# print("first tweet:", first)
# last = datetime.fromtimestamp(last).isoformat()
# print("last tweet:", last)
#
# print("number of accounts:", len(accounts))
#
# print("Stats on tweets that got at least one like")
# print("\tMax:", max(likes))
# print("\tMin:", min(likes))
# print("\tMean:", statistics.mean(likes))
# print("\tMedian:", statistics.median(likes))
# print("\tStandard deviation:", statistics.stdev(likes))
# print()



# print(zero_likes/len(tweets))