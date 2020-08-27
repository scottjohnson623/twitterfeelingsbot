import tweepy
import logging
import os
from dotenv import load_dotenv, find_dotenv
logger = logging.getLogger()
load_dotenv(find_dotenv())


def create_api():
    consumer_key = os.environ.get("CONSUMER_KEY")
    consumer_secret = os.environ.get("CONSUMER_SECRET")
    access_token = os.environ.get("ACCESS_TOKEN")
    access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, 
        wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error", exc_info=True)
        raise e
    logger.info("Success")
    return api




# Create API object
api = create_api()

# Check credentials work
try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")