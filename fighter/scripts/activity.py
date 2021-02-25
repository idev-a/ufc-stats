import os
import sys
import django
import requests
import argparse
import json
from decouple import config
from typing import NoReturn
from abc import ABC, abstractmethod

from tweepy.error import TweepError
from tweepy import OAuthHandler

class Activity:
    _protocol: str = "https:/"
    _host: str = "api.twitter.com"
    _version: str = "1.1"
    _product: str = "account_activity"
    _auth: OAuthHandler = OAuthHandler(
        config('TWITTER_BOT_CONSUMER_KEY'), config('TWITTER_BOT_CONSUMER_SECRET')
    )
    _auth.set_access_token(
        config('TWITTER_BOT_ACCESS_TOKEN'), config('TWITTER_BOT_ACCESS_TOKEN_SECRET')
    )

    def api(self, method: str, endpoint: str, data: dict = None) -> json:
        """
        :param method: GET or POST
        :param endpoint: API Endpoint to be specified by user
        :param data: POST Request payload parameter
        :return: json
        """
        try:
            with requests.Session() as r:
                response = r.request(
                    url="/".join(
                        [
                            self._protocol,
                            self._host,
                            self._version,
                            self._product,
                            endpoint,
                        ]
                    ),
                    method=method,
                    auth=self._auth.apply_auth(),
                    data=data,
                )
                return response
        except TweepError:
            raise

    def register_webhook(self, callback_url: str) -> json:
        try:
            return self.api(
                method="POST",
                endpoint=f"all/{config('TWITTER_ENV_NAME')}/webhooks.json",
                data={"url": callback_url},
            ).json()
        except Exception as e:
            raise e

    def refresh(self, webhook_id: str) -> NoReturn:
        """Refreshes CRC for the provided webhook_id.
        """
        try:
            return self.api(
                method="PUT",
                endpoint=f"all/{config('TWITTER_ENV_NAME')}/webhooks/{webhook_id}.json",
            )
        except Exception as e:
            raise e

    def delete (self, webhook_id: str) -> NoReturn:
        """Removes the webhook from the provided webhook_id.
        """
        try:
            return self.api(
                method="DELETE",
                endpoint=f"all/{config('TWITTER_ENV_NAME')}/webhooks/{webhook_id}.json",
            )
        except Exception as e:
            raise e

    def subscribe(self) -> NoReturn:
        try:
            return self.api(
                method="POST",
                endpoint=f"all/{config('TWITTER_ENV_NAME')}/subscriptions.json",
            )
        except Exception:
            raise

    def webhooks(self) -> json:
        """Returns all environments, webhook URLs and their statuses for the authenticating app.
        Only one webhook URL can be registered to each environment.
        """
        try:
            return self.api(method="GET", endpoint=f"all/webhooks.json").json()
        except Exception as e:
            raise e

if __name__ == "__main__":
    activity = Activity()
    # activity.delete('1363218664019947520')
    # print(activity.webhooks())
    res = activity.register_webhook(
        callback_url=config('TWITTER_AUTH_WEBHOOK_URL')
    )
    print(activity.subscribe())