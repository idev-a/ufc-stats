
import tweepy
import logging
from config import create_api
import json
import time
import pdb
import os
import sys
import django

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "."))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fighter.settings')
django.setup()

from contest.models import Event

from contest.views import (
    event_views
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

START_KEYWORD = "fqtestbot"

class FavRetweetListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def reply(self, text, id):
        logger.info('reply command:: ' + text)
        self.api.update_status(
            status=text,
            in_reply_to_status_id=id,
        )

    def manage_shows(self, tweet, block):
        first_command = block.split(' ')[0]
        logger.info(first_command)
        if first_command == 'show__all_commands':
            self.reply('show__latest_event', tweet.id)

        elif first_command == 'show__latest_event':
            event = Event.objects.latest_event()
            self.reply(event.__str__(), tweet.id)

    def on_status(self, tweet):
        logger.info(f"Processing tweet id {tweet.id}")
        commands_block = tweet.text.split(START_KEYWORD)[1].strip()
        first_command = commands_block.split(' ')[0]
        if first_command.startswith('show__'):
            self.manage_shows(tweet, commands_block)
        # if tweet.in_reply_to_status_id is not None or \
        #     tweet.user.id == self.me.id:
        #     # This tweet is a reply or I'm its author so, ignore it
        #     return

    def on_error(self, status_code):
        logger.error(status_code)
        if status_code == 420:
            return True

def main(keywords):
    api = create_api()
    tweets_listener = FavRetweetListener(api)
    stream = tweepy.Stream(api.auth, tweets_listener)
    stream.filter(track=keywords, languages=["en"], is_async=True)

if __name__ == "__main__":
    main([START_KEYWORD])
