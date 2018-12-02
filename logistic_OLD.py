#!/usr/bin/env python

import numpy
import scipy.optimize
import random, json
from math import exp
from math import log

# with open("orig_content_train.json") as f:
#     data = json.load(f)

with open("train_mini.json") as f:
    data = json.load(f)

split = len(data) // 2
train = data[:split]
valid = data[split:]


def get_features(d):
    features = [1]
    # if 'https://t.co' in d['tweet_text']:
    #     features.append(1)
    # else:
    #     features.append(0)
    features.append(int(d['follower_count']))
    return features


X_train = [get_features(d) for d in train]
X_valid = [get_features(d) for d in valid]
y_train = [d['like_count'] != '0' for d in train]
y_valid = [d['like_count'] != '0' for d in valid]

Xs = [X_train, X_valid]
ys = [y_train, y_valid]


def inner(x, y):
    return sum([x[i] * y[i] for i in range(len(x))])


def sigmoid(x):
    return 1.0 / (1 + exp(-x))


##################################################
# Logistic regression by gradient ascent         #
##################################################

# NEGATIVE Log-likelihood
def f(theta, X, y, lam):
    loglikelihood = 0
    for i in range(len(X)):
        logit = inner(X[i], theta)
        loglikelihood -= log(1 + exp(-logit))
        if not y[i]:
            loglikelihood -= logit
    for k in range(len(theta)):
        loglikelihood -= lam * theta[k] * theta[k]  # regularization
    # for debugging
    print("ll =" + str(loglikelihood))
    return -loglikelihood


# NEGATIVE Derivative of log-likelihood
def fprime(theta, X, y, lam):
    dl = [0] * len(theta)
    for i in range(len(X)):
        logit = inner(X[i], theta)
        for k in range(len(theta)):
            dl[k] += X[i][k] * (1 - sigmoid(logit))
            if not y[i]:
                dl[k] -= X[i][k]
    for k in range(len(theta)):
        dl[k] -= lam * 2 * theta[k]
    return numpy.array([-x for x in dl])


##################################################
# Train                                          #
##################################################

def train(X, y_vals, lam):
    theta, _, _ = scipy.optimize.fmin_l_bfgs_b(f, [0] * len(X[0]), fprime, pgtol=10, args=(X, y_vals, lam))
    return theta


##################################################
# Predict                                        #
##################################################

def performance(theta, data_set, y_vals, print_negs=False):
    scores = [inner(theta, x) for x in data_set]
    predictions = [s > 0 for s in scores]
    correct = [(a == b) for (a, b) in zip(predictions, y_vals)]
    if print_negs:
        positives = sum(predictions)
        print("Positives:", positives)
        negatives = sum([1 - i for i in predictions])
        print("Negatives:", negatives)
        false_positives = sum([a != b and a for (a, b) in zip(predictions, y_vals)])
        print("False Positives:", false_positives)
        false_negatives = sum([a != b and not a for (a, b) in zip(predictions, y_vals)])
        print("False Negatives:", false_negatives)
        true_positives = sum([a == b and a for (a, b) in zip(predictions, y_vals)])
        print("True Positives:", true_positives)
        true_negatives = sum([a == b and not a for (a, b) in zip(predictions, y_vals)])
        print("True Negatives:", true_negatives)
    acc = sum(correct) * 1.0 / len(correct)
    return acc



##################################################
# Validation pipeline                            #
##################################################

def get_perfs(X_train, y_train, Xs, ys, lam):
    theta = train(X_train, y_train, lam)
    results = []
    for j in range(len(Xs)):
        acc = performance(theta, Xs[j], ys[j], print_negs=True)
        results.append(acc)
    return results


print("accuracy rates for lambda=1: ", get_perfs(X_train, y_train, Xs, ys, 1))

def get_best_lam(X_train, y_train, Xs, ys):
    lams = [0, 0.01, 0.1, 1, 100]
    best_lam = 0
    best_acc = -1
    accs = []
    names = ["train", "valid"]
    for i in range(len(lams)):
        theta = train(X_train, y_train, lams[i])
        trio = []
        for j in range(len(Xs)):
            acc = performance(theta, Xs[j], ys[j])
            trio.append(acc)
            if j == 1:
                if best_acc < acc:
                    best_acc = acc
                    best_lam = i
                print("lambda = ", lams[i], ":\taccuracy=", acc)
        accs.append(trio)
    return lams[best_lam], accs


# best_lam, accs = get_best_lam(X_train, y_train, Xs, ys)
# print("Best lambda:", best_lam)
# for acc in accs:
#     print(acc)


"""

1 feature: https://t.co
accuracy rates for lambda=1:  [0.771, 0.782]

2 features: t.co and num followers:
overflow error?

"""
