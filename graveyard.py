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