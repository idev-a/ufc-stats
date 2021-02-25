# tweepy-bots/bots/config.py
import tweepy
import logging
import os
from decouple import config

logger = logging.getLogger(__name__)

def create_api():
    consumer_key = config("TWITTER_BOT_CONSUMER_KEY")
    consumer_secret = config("TWITTER_BOT_CONSUMER_SECRET")
    access_token = config("TWITTER_BOT_ACCESS_TOKEN")
    access_token_secret = config("TWITTER_BOT_ACCESS_TOKEN_SECRET")

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, 
        wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api