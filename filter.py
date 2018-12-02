#!/usr/bin/env python3

import csv, json, re
from random import shuffle

filename = "/Users/carrickdb/Desktop/ira_tweets_csv_hashed.csv"

"""
0 tweetid
1 userid
2 user_display_name
3 user_screen_name
4 user_reported_location
5 user_profile_description
6 user_profile_url
7 follower_count
8 following_count
9 account_creation_date
10 account_language
11 tweet_language
12 tweet_text
13 tweet_time
14 tweet_client_name
15 in_reply_to_tweetid
16 in_reply_to_userid
17 quoted_tweet_tweetid
18 is_retweet
19 retweet_userid
20 retweet_tweetid
21 latitude
22 longitude
23 quote_count
24 reply_count
25 like_count
26 retweet_count
27 hashtags
28 urls
29 user_mentions
30 poll_choices
"""
data = []
# 12th item is tweet text
i = 0
with open(filename) as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        if not re.findall(r'[А-я]+', row[12]) and row[18]!='true' and row[17] == '' and row[11] == 'en' \
                and 'https://t.co' not in row[12] and row[28] == '':
            data.append(row)
            i += 1
            if i % 100000 == 0:
                print(i)
        if i == 2000000:
            break

data = [dict(zip(header, d)) for d in data]
print(len(data))
shuffle(data)

print("writing to file")
with open('orig_en_noURL_train.json', 'w') as f:
    json.dump(data[:50000], f)

with open('orig_en_noURL_test.json', 'w') as f:
    json.dump(data[50000:75000], f)
