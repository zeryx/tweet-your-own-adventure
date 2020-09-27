from __future__ import annotations

from src.local_fragment import LocalFragment
from tweepy.api import API
import pyshorteners

shortener = pyshorteners.Shortener()


class TwitterFragment:
    left = None
    right = None
    localFragment = None
    id = None
    tweet = None
    terminus = False

    def __init__(self, fragment: LocalFragment, tweepy_api: API):
        self.id = fragment.id
        self.body = fragment.body
        self.terminus = fragment.terminus
        if fragment.left:
            self.left = fragment.left
        if fragment.right:
            self.right = fragment.right
        self.tweet = self.__tweet_fragment(tweepy_api)

    def __tweet_fragment(self, tweepy_api: API):
        tweet = tweepy_api.update_status(self.body)
        return tweet

    def add_paths(self, username, left: TwitterFragment, right: TwitterFragment, tweepy_api: API):
        self.left['tweet'] = left.tweet
        self.right['tweet'] = right.tweet
        left_tweet_url = "https://twitter.com/{}/status/{}".format(username, left.tweet.id)
        right_tweet_url = "https://twitter.com/{}/status/{}".format(username, right.tweet.id)
        left_shortened = shortener.tinyurl.short(left_tweet_url)
        right_shortened = shortener.tinyurl.short(right_tweet_url)
        tweepy_api.update_status("{} \n {}".format(self.left['body'], left_shortened), in_reply_to_status_id=self.tweet.id)
        tweepy_api.update_status("{} \n {}".format(self.right['body'], right_shortened), in_reply_to_status_id=self.tweet.id)
