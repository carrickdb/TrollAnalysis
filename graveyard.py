"""
If we just predicted 0 for everything (training set only): 691.4553004003672
If we just predicted 0 for everything (validation set only): 276.44231438915426

Predict only global average (6.9468375176935115):
train: 691.3506033824447
valid: 276.2380278022926

Predict user average if seen user before; else global:
MSE: 674.188114535534
MSE: 282.5908248095771

median (user and global) instead of average:
RMSE: 687.7623507316756
RMSE: 269.71118663034423
"""


print("RMSE:", math.sqrt(sklearn.metrics.mean_squared_error(y, predictions)))



n = [478110.4324517619, 76420.353184832, 477965.65679727023,76307.4480041002, 454529.61378097837, 79857.57426655709]

for num in n:
    print(math.sqrt(num))
# theta = tf.Variable(tf.constant([0.0] *


account_likes = {}
followers = {}

i = 0
total_likes = 0
for d in train:
    account = d['userid']
    if account not in followers:
        followers[account] = d['follower_count']
    like_count = int(d['like_count'])
    total_likes += like_count
    if account in account_likes:
        account_likes[account].append(like_count)
    else:
        account_likes[account] = [like_count]

for account, likes in account_likes.items():
    account_likes[account] = np.median(likes)

URL_liked = 0
URL_unliked = 0
noURL_liked = 0
noURL_unliked = 0

for d in train:
    like_count = int(d['like_count'])
    if like_count < 0:
        print("wtf")
    if 'https://t.co' in d['tweet_text']:
        if like_count == 0:
            URL_unliked += 1
        if like_count > 0:
            URL_liked += 1
    else:
        if like_count == 0:
            noURL_unliked += 1
        else:
            noURL_liked += 1

print(URL_liked / (URL_liked + noURL_liked))
print(URL_unliked / (URL_unliked + noURL_unliked))
print(URL_liked / (URL_liked + URL_unliked))
# print(noURL_unliked)

# '2014-08-21 08:29'
times = []
likes = []
for d in train:
    date = datetime.strptime(d['tweet_time'], '%Y-%m-%d %H:%M')
    like_count = int(d['like_count'])
    if like_count < 200 and date > datetime.strptime("2012-01-01 12:00", '%Y-%m-%d %H:%M'):
        times.append(date)
        likes.append(like_count)

plt.scatter(times, likes)
plt.show()

date = datetime.strptime(d['tweet_time'], '%Y-%m-%d %H:%M')

print(date.hour, date.minute)
minutes_in_day = 24 * 60
seconds = date.hour * 60 + date.minute
sin_time = np.sin(2 * np.pi * seconds / minutes_in_day)
cos_time = np.cos(2 * np.pi * seconds / minutes_in_day)
print(cos_time, sin_time)

features.append(sin_time)
features.append(cos_time)

x = []
y = []
for d in train:
    like_count = int(d['like_count'])
    if like_count < 100:
        date = datetime.strptime(d['tweet_time'], '%Y-%m-%d %H:%M')
        time_of_day = date.hour * 60 + date.minute
        x.append(time_of_day)
        y.append(like_count)

plt.scatter(x, y)
plt.show()


hashtag_tuples = sorted([(hashtag, likes) for hashtag, likes in hashtags.items()], key=lambda x: len(x[1]), reverse=True)
unliked_hashtags = []
liked_hashtags = []
for hashtag, likes in hashtag_tuples:
    if statistics.median(likes) > 0:
        liked_hashtags.append((hashtag, likes))
    else:
        unliked_hashtags.append((hashtag, likes))

for ht in unliked_hashtags[:5]:
    print(ht[0])
print()
for ht in liked_hashtags[:5]:
    print(ht[0])


if 'https://t.co' in d['tweet_text'] or d['urls'] != '':
    features.append(1)
else:
    features.append(0)
features.append(int(d['follower_count']))

ht_feature = 0
for ht in curr_hashtags:  # 1 if using a popular hashtag, 0 else
    if ht in hashtags:
        ht_count = [1 for likes in hashtags[ht] if likes > 0]
        if sum(ht_count) >= len(ht_count) / 2:
            ht_feature += 1
features.append(ht_feature)

if d['tweet_text'] in tweets:
    features.append(0)
    old_likes = statistics.median(tweets[d['tweet_text']])
    features.append(old_likes)
else:
    features.append(1)
    features.append(0)


"""
All languages except Russian:

just t.co:
0.771
0.782

just follower count:
0.788
0.794

follower count and t.co
0.798
0.801

no effect (alone): Hillary, Trump, timestamp (time since Unix epoch), time of day

follower count and t.co with balanced class weights:
0.713
0.712

median account likes:
0.82
0.816

mean account likes:
0.817
0.82

median account likes and follower count:
0.811
0.808
"""