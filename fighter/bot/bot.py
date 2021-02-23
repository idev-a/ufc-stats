import requests
import json
import pdb
import os
import sys
import django
from decouple import config
from time import sleep
import logging
import tweepy
import imgkit

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "."))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fighter.settings')
django.setup()

from config import create_api

from contest.views import (
    event_views
)

START_KEYWORD = "fqtestbot"
session = requests.Session()

def html2png(body=None):
    body = """
    <html>
        <head>
        <meta content="png"/>
        <meta content="Landscape"/>
        </head>
        Hello World!
        </html>
    """

    options = {
        "xvfb": ""
    }
    config = imgkit.config(wkhtmltoimage='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltoimage.exe')
    imgkit.from_string(body, 'out.png', config=config)

class TwitterBot:

    timeout = 10

    def __init__(self):
        self.tweepy_api = create_api()
        self.bearer_token = config("TWITTER_BEARER_TOKEN")
        self.headers = self.create_headers()
        self.sample_rules = [
            {"value": START_KEYWORD, "tag": START_KEYWORD},
        ]

        # initialize rules
        rules = self.get_rules()
        self.delete_all_rules(rules)
        self.set_rules()

    def reply(self, text, id):
        logger.info('reply command:: ' + text)
        self.tweepy_api.update_status(
            status=text,
            in_reply_to_status_id=id,
        )

    def upload_photo(self, text, id, path):
        img = self.tweepy_api.media_upload(path)
        self.tweepy_api.send_direct_message(id, text, attachment_type='media', attachment_media_id=img.media_id)

    def manage_shows(self, tweet, block):
        first_command = block.split(' ')[0]
        logger.info(first_command)
        if first_command == 'show__all_commands':
            self.reply('show__latest_event', tweet['id'])

        elif first_command == 'show__latest_event':
            event = event_views.show__latest_event()
            self.reply(event.__str__(), tweet['id'])

    def create_headers(self):
        headers = {"Authorization": "Bearer {}".format(self.bearer_token)}
        return headers

    def get_rules(self):
        response = session.get(
            "https://api.twitter.com/2/tweets/search/stream/rules", headers=self.headers
        )
        if response.status_code != 200:
            raise Exception(
                "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
            )
        logger.info('[bot] get_rules')
        logger.info(json.dumps(response.json()))
        return response.json()


    def delete_all_rules(self, rules):
        if rules is None or "data" not in rules:
            return None

        ids = list(map(lambda rule: rule["id"], rules["data"]))
        payload = {"delete": {"ids": ids}}
        response = session.post(
            "https://api.twitter.com/2/tweets/search/stream/rules",
            headers=self.headers,
            json=payload
        )
        if response.status_code != 200:
            raise Exception(
                "Cannot delete rules (HTTP {}): {}".format(
                    response.status_code, response.text
                )
            )
        logger.info('[bot] delete_all_rules')
        logger.info(json.dumps(response.json()))


    def set_rules(self):
        # You can adjust the rules if needed
        payload = {"add": self.sample_rules}
        response = session.post(
            "https://api.twitter.com/2/tweets/search/stream/rules",
            headers=self.headers,
            json=payload,
        )
        if response.status_code != 201:
            raise Exception(
                "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
            )
        logger.info('[bot] set_rules')
        logger.info(json.dumps(response.json()))


    def get_stream(self):
        try:
            response = session.get(
                "https://api.twitter.com/2/tweets/search/stream?tweet.fields=created_at&expansions=author_id&user.fields=created_at", headers=self.headers, stream=True,
            )
            logger.info(response)
            if response.status_code != 200:
                logger.info("Cannot get stream (HTTP {}): {}".format(
                    response.status_code, response.text
                ))
                sleep(2*self.timeout)
                self.get_stream()
        except Exception as err:
            logger.info(err)
            sleep(2*self.timeout)
            self.get_stream()
            return

        for response_line in response.iter_lines():
            if response_line:
                json_response = json.loads(response_line)
                tweet = json_response['data']
                commands_block = tweet['text'].split(START_KEYWORD)[1].strip()
                first_command = commands_block.split(' ')[0]
                if first_command.startswith('show__'):
                    self.manage_shows(tweet, commands_block)


if __name__ == "__main__":
    # bot = TwitterBot()
    # bot.get_stream()
    # html2png()

    event = event_views.show__latest_event()
    print(event)
    
    # api = create_api()
    # image_path = 'out.png'
    # tweet_text = 'The below shows top games'
    # status = api.update_with_media(image_path, tweet_text, in_reply_to_status_id='1362837934567616515')
