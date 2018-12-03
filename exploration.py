#!/usr/bin/env python3

import json, statistics
from pprint import pprint
from collections import defaultdict
import matplotlib.pyplot as plt

train_file = "orig_en_train.json"
# valid_file = "init_valid.json"

"""
data to look at:

when the account was created
number pretending to be BLM? (e.g. location = Ferguson)
liberal v. conservative?
twitter client (russian origin??)
language associated with account
Are people with like 0 followers doing the RTing?
number of times a user repeated one of their own tweets verbatim
likes to time
"""

with open(train_file) as f:
    tweets = json.load(f)
    # tweets.extend(json.load(f))

tweet_text = defaultdict(list)
total_likes = 0
zero_likes = 0
zero_RTs = 0
replies = 0
RT_count = 0
is_reply = 0
accounts = {}
no_like_data = 0
no_RT_data = 0
num_tweets = len(tweets)
RT_likes = []
orig_content_likes = []
RT_RTs = []
orig_content_RTs = []
most_successful_tweet = None
highest_num_likes = 0
RTd_users = 0
tweet_text_repeaters = {}
tweet_text_counts = defaultdict(int)
likes = []
num_likes_RT = 0
languages = defaultdict(int)
unique_tweets = defaultdict(int)
for tweet in tweets:
    unique_tweets[tweet['tweet_text']] += 1
    userid = tweet['userid']
    if userid not in accounts:
        accounts[userid] = {}
        accounts[userid]['account_creation_date'] = tweet['account_creation_date']
        accounts[userid]['account_language'] = tweet['account_language']
        accounts[userid]['follower_count'] = int(tweet['follower_count'])
        accounts[userid]['following_count'] = int(tweet['following_count'])
        accounts[userid]['tweet_client_name'] = tweet['tweet_client_name']
        accounts[userid]['num_tweets'] = 1
        languages[tweet['account_language']] += 1
    else:
        accounts[userid]['num_tweets'] += 1
    if tweet['like_count']:
        num_likes = int(tweet['like_count'])
        if num_likes > 25000:
            print(tweet['tweet_text'], ":", num_likes)
        if num_likes > highest_num_likes:
            highest_num_likes = num_likes
            most_successful_tweet = tweet['tweet_text']
        total_likes += num_likes
        if num_likes == 0:
            zero_likes += 1
        if tweet['is_retweet'] == 'true':
            RT_likes.append(num_likes)
        else:
            likes.append(num_likes)
            orig_content_likes.append(num_likes)
    else:
        no_like_data += 1
    if tweet['is_retweet'] == 'true':
        RT_count += 1
        if tweet['retweet_userid'] in accounts:
            RTd_users += 1
        if tweet['like_count']:
            num_likes_RT += int(tweet['like_count'])
    else:
        tweet_text_counts[tweet['tweet_text']] += 1
        tweet_text = tweet['tweet_text']
        if tweet_text in tweet_text_repeaters:
            if userid in tweet_text_repeaters[tweet_text]:
                tweet_text_repeaters[tweet_text][userid] += 1
            else:
                tweet_text_repeaters[tweet_text][userid] = 1
        else:
            tweet_text_repeaters[tweet_text] = {}
            tweet_text_repeaters[tweet_text][userid] = 1
    if tweet['retweet_count']:
        num_RTs = int(tweet['retweet_count'])
        if num_RTs == 0:
            zero_RTs += 1
        if tweet['is_retweet'] == 'true':
            RT_RTs.append(num_RTs)
        else:
            orig_content_RTs.append(num_RTs)
    else:
        no_RT_data += 1  # is there something common among the tweets with no like/RT data?
    if tweet['in_reply_to_tweetid']:
        is_reply += 1
    if tweet['reply_count']:
        replies += int(tweet['reply_count'])


# for language, count in languages.items():
#     print(language, count)



likes = sorted(likes)
threshold = 0
for i in range(len(likes)):
    if likes[i] > 1000:
        threshold = i
        break
unliked = likes[:threshold]
liked = likes[threshold:]
plt.hist(unliked)
plt.show()

bins = [1000]
more_bins = [i*1000 for i in range(1, 11)]
bins.extend(more_bins)
plt.hist(liked, bins=more_bins)
axes = plt.gca()
axes.set_ylim([0,150])
plt.show()
tally = []
num_repeaters = 0
num_repeats = 0
max_repeats = 0
most_repeated = None
for repeated_text, repeaters in tweet_text_repeaters.items():
    for repeater, count in repeaters.items():
        if count > 1:
            if count > max_repeats:
                max_repeats = count
                most_repeated = repeated_text
            num_repeats += count - 1
            num_repeaters += 1
            tally.append(count)
print(most_repeated)
print(max_repeats)
print(num_repeaters)
print(num_repeats)
print("\tMax:", max(tally))
print("\tMin:", min(tally))
print("\tMean:", statistics.mean(tally))
print("\tMedian:", statistics.median(tally))
print("\tStandard deviation:", statistics.stdev(tally))
total_copies = 0
for tweet_t, count in tweet_text_counts.items():
    if count > 1:
        total_copies += count
print(total_copies)
copycat_counts = defaultdict(int)
copy_counts = []
for tweet_text, copycats in tweet_text_counts.items():
    if len(copycats) > 1:
        for copycat in copycats:
            copycat_counts[copycat] += 1
        copy_counts.append(len(copycats))
copycat_count_list = [x for x in copycat_counts.values()]
for tally in [copy_counts, copycat_count_list]:
    print("\tMax:", max(tally))
    print("\tMin:", min(tally))
    print("\tMean:", statistics.mean(tally))
    print("\tMedian:", statistics.median(tally))
    print("\tStandard deviation:", statistics.stdev(tally))
    print()
print(RTd_users/RT_count)
for unique_tweet, count in unique_tweets.items():
    if count > 1:
        print(count)
tweets_per_account = []
for account, account_data in accounts.items():
    tweets_per_account.append(account_data['num_tweets'])
for tally in [RT_RTs, orig_content_RTs]:
    print("\tMax:", max(tally))
    print("\tMin:", min(tally))
    print("\tMean:", statistics.mean(tally))
    print("\tMedian:", statistics.median(tally))
    print("\tStandard deviation:", statistics.stdev(tally))
    print()
followers = []
following = []
for account, account_data in accounts.items():
    followers.append(account_data['follower_count'])
    following.append(account_data['following_count'])

print("percentage that are themselves replies:", is_reply/num_tweets)
print("no RT data:", no_RT_data)
print("no_like_data:", no_like_data)
print("Orig content stats:")
print("\tMax:", max(orig_content_likes))
print("\tMedian:", statistics.median(orig_content_likes))
print("\tStandard deviation:", statistics.stdev(orig_content_likes))
print("\nRT stats:")
print("\tnum stats on RTs", len(RT_likes))
print("\tMax:", max(RT_likes))
print("\tMedian:", statistics.median(RT_likes))
print("\tStandard deviation:", statistics.stdev(RT_likes))
print("average # of likes:", total_likes/num_tweets)
print("average # of replies:", replies/num_tweets)
# print("number of separate accounts:", len(accounts))
print("percentage that are retweets:", RT_count/num_tweets)
print("percentage of tweets with 0 likes:", zero_likes/num_tweets)
print("percentage of tweets with 0 RTs:", zero_RTs/num_tweets)



"""
average # of likes: 8.579955
average # of replies: 0.519565
number of separate accounts: 2774
percentage that are retweets: 0.326515
percentage of tweets with 0 likes: 0.85143
percentage of tweets with 0 RTs: 0.85718
percentage that are themselves replies: 0.02798
percentage of RTs that are tweets by another account in this dataset
    (the echochamber metric): 0.12350121740195703
    (none of those original tweets are in these sets)
no RT data: 111
no_like_data: 111
Orig content stats:
	Max: 150363
	Median: 0
	Standard deviation: 525.5241029130985
RT stats:
	num stats on RTs 65192
	Max: 0
	Median: 0.0
	Standard deviation: 0.0
    (so this study is going to be only about original content)
Followers per account:
	Max: 257638
	Min: 0
	Mean: 2050.9643114635905
	Median: 140.5
	Standard deviation: 10082.681958997044
Following per account:
	Max: 74664
	Min: 0
	Mean: 1018.2253064167268
	Median: 283.0
	Standard deviation: 3158.550859146856

Number of tweets repeated verbatim from different users: 12315
Total number of copied tweets??: 18283

Number of times RT'd content was RT'd: (maybe this data wasn't used for RT'd content?)
    Max: 0
	Min: 0
	Mean: 0
	Median: 0.0
	Standard deviation: 0.0

Number of times original content was RT'd:
	Max: 51472
	Min: 0
	Mean: 9.057633057900324
	Median: 0
	Standard deviation: 219.97283978589496

Number of times a tweet appeared verbatim (not RT'd) (of the tweets that appeared more than once):
	Max: 22
	Min: 2
	Mean: 3.012233484795526
	Median: 2.0
	Standard deviation: 2.5480916650954932

Number of times a user tweeted content copied verbatim (not RT'd) (of the users that copied content):
	Max: 15
	Min: 2
	Mean: 2.267405063291139
	Median: 2.0
	Standard deviation: 1.0333645939355958

Most successful tweet:
Don’t ever tell me kneeling for the flag is disrespectful to our troops when  Trump calls a sitting Senator “Pocahontas” in front of Native American war heroes.
150363
(Not conservative!!)

Number of tweets per account (prolificness):
	Max: 6872
	Min: 1
	Mean: 72.09805335255948
	Median: 14.0
	Standard deviation: 260.87055519301225

None of these tweets are RTs of a different tweet in this set

Tweet that was repeated most frequently by the same user (15x): Honor scores  #sports
Number of account that tweeted content copied verbatim from their *own* account: 632
number of times an account tweeted content they already tweeted: 801
stats on accounts that repeated content:
	Max: 15
	Min: 2
	Mean: 2.267405063291139
	Median: 2.0
	Standard deviation: 1.0333645939355958

Account language count (orig content only):
en 1711
es 137
id 1
de 86
zh-cn 3
ru 328
en-gb 4
ar 9
fr 2
it 1


Sample tweet:
{'tweetid': '502371804913348608', 'userid': 'b0b90ae15ea8fcad5fd0fe5666ba65680a9b76103c4cee437d44456e12d00066',
'user_display_name': 'b0b90ae15ea8fcad5fd0fe5666ba65680a9b76103c4cee437d44456e12d00066',
'user_screen_name': 'b0b90ae15ea8fcad5fd0fe5666ba65680a9b76103c4cee437d44456e12d00066',
'user_reported_location': 'cleveland / ohio', 'user_profile_description': 'wanna live 4ever',
'user_profile_url': '', 'follower_count': '145', 'following_count': '318',
'account_creation_date': '2014-03-15', 'account_language': 'en', 'tweet_language': 'en',
'tweet_text': 'Boy have no fear (have no fear)', 'tweet_time': '2014-08-21 08:29',
'tweet_client_name': 'vavilonX', 'in_reply_to_tweetid': '', 'in_reply_to_userid': '',
'quoted_tweet_tweetid': '', 'is_retweet': 'false', 'retweet_userid': '', 'retweet_tweetid': '',
'latitude': '', 'longitude': '', 'quote_count': '0', 'reply_count': '0', 'like_count': '0',
'retweet_count': '0', 'hashtags': '', 'urls': '', 'user_mentions': '', 'poll_choices': ''}
"""
