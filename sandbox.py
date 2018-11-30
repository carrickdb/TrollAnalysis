import json

with open("train_mini.json") as f:
    tweets = json.load(f)

print(tweets[0])