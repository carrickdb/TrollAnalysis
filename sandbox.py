import json
from datetime import datetime
import matplotlib.pyplot as plt

with open("orig_en_train.json") as f:
    tweets = json.load(f)

x = []
y = []
for d in tweets:
    tweet_date = datetime.strptime(d['tweet_time'], '%Y-%m-%d %H:%M').timestamp()
    account_date = datetime.strptime(d['account_creation_date'], '%Y-%m-%d').timestamp()
    x.append(tweet_date - account_date)
    like_count = d['like_count']
    if like_count == '0':
        y.append(0)
    else:
        y.append(1)


plt.scatter(x, y)
plt.show()
