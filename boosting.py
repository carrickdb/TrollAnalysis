import json
import sklearn.ensemble

with open("orig_en_train.json") as f:
    data = json.load(f)

split = len(data)//2
train = data[:split]
valid = data[split:]

train_pred = []
y_train = []

for d in train:
    if 'http://t.co' in d['tweet_text'] or d['urls'] != '':
        train_pred.append(1)
    else:
        train_pred.append(0)
    if d['like_count'] == '0':
        y_train.append(0)
    else:
        y_train.append(1)

train_compare = [(train_pred[i] == y_train[i]) for i in range(len(y_train))]
# valid_compare = [(valid_pred[i] == y_valid[i]) for i in range(len(y_valid))]
train_acc = sum(train_compare) * 1.0 / len(train_compare)
print(train_acc)
# valid_acc = sum(valid_compare) * 1.0 / len(valid_compare)

