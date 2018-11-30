#!/usr/bin/env python3

import json

train_file = "init_train.json"
valid_file = "init_valid.json"
test_file = "init_test.json"

with open(valid_file) as f:
    train_tweets = json.load(f)

with open(train_file) as f:
    train_tweets.extend(json.load(f))

with open(test_file) as f:
    test_tweets = json.load(f)

orig_train = []
orig_test = []
for tweet in train_tweets:
    if tweet['is_retweet'] == 'false':
        orig_train.append(tweet)

for tweet in test_tweets:
    if tweet['is_retweet'] == 'false':
        orig_test.append(tweet)

smallest = min(len(orig_train)//2, len(orig_test))

with open('orig_content_train.json', 'w') as f:
    json.dump(orig_train[:smallest*2], f)

with open('orig_content_test.json', 'w') as f:
    json.dump(orig_test[:smallest], f)
