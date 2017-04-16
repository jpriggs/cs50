from flask import Flask, redirect, render_template, request, url_for

import helpers
import sys
import os
from analyzer import Analyzer
from tweet import Tweet

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():

    # validate screen_name
    screen_name = request.args.get("screen_name", "").lstrip("@")
    if not screen_name:
        return redirect(url_for("index"))

    # get screen_name's tweets
    tweets = helpers.get_user_timeline(screen_name, 100)
    
    # checks if any tweets exist in the user timeline
    if tweets == None:
        return redirect(url_for("index"))
    
    # absolute paths to lists
    positives = os.path.join(sys.path[0], "positive-words.txt")
    negatives = os.path.join(sys.path[0], "negative-words.txt")
    
    # instantiate Analyzer
    analyzer = Analyzer(positives, negatives)

    # TODO
    positive, negative, neutral = 0.0, 0.0, 0.0
    tweetObjectList = list()
    
    # iterate over each tweet and score them positive, negative, or neutral
    for tweet in tweets:
        
        tweetValue = analyzer.analyze(tweet)
        tweetObject = Tweet(tweet, tweetValue)
        tweetObjectList.append(tweetObject)

        if tweetValue > 0.0:

            positive += 1

        elif tweetValue < 0.0:

            negative += 1

        else:

            neutral += 1
    
    # generate chart
    chart = helpers.chart(positive, negative, neutral)

    # render results
    return render_template("search.html", chart=chart, screen_name=screen_name, totalTweets=len(tweets), tweets=tweetObjectList)