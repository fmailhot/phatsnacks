# PhatSnacks
#
# A Twitter bot: tweet a food at it, it'll reply with a recipe.
# (forked from Molly White's twitterbot_framework: https://github.com/molly/twitterbot_framework)
import os
import tweepy
from secrets import *
from time import gmtime, strftime
import logging
import requests

# ====== Individual bot configuration ==========================
bot_username = "phatsnacks1974"
logfile_name = bot_username + ".log"
logging.basicConfig(filename=logfile_name, datefmt="%Y%m%d_%H%M",
                    level=logging.DEBUG)
food2fork_url = "http://food2fork.com/api/search"
# ==============================================================


def create_tweet(food_name):
    """Create the text of the tweet you want to send."""
    r = requests.get(food2fork_url, params={"q": food_name, "key": F2F_KEY})
    try:
        r_json = r.json()
    except Exception as e:
        return "No recipe found. #sadpanda"
    # fetch top-ranked recipe
    recipe = r_json["recipes"][0]
    recipe_f2f_url = recipe["f2f_url"]
    recipe_name = recipe["title"]
    recipe_publisher = recipe["publisher"]
    recipe_img = recipe["image_url"]
    text = "\"%s\" by %s: %s" % (recipe_name, recipe_publisher, recipe_f2f_url)
    return text


def tweet(text):
    """Send out the text as a tweet."""
    # Twitter authentication
    auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
    auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
    api = tweepy.API(auth)

    # Send the tweet and log success or failure
    try:
        api.update_status(text)
    except tweepy.error.TweepError as e:
        logging.error(e.message)
    else:
        logging.info("Tweeted: " + text)


if __name__ == "__main__":
    food_name = raw_input("Enter a food/ingredient: ")
    tweet_text = create_tweet(food_name)
    tweet(tweet_text)
#    print tweet_text

