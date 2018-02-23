import requests
import tweepy
import json
from redis_obj import Redis

class MyStreamListener(tweepy.StreamListener):

    def __init__(self):
        self.redis = Redis().build_redis()
        self.text_job_queue = 'TEXT_ANALYSIS_JOB'

    def on_status(self, status):
        if status.retweeted:
            return
        processed_tweet = self.process_tweet(status)
        self.add_text_analysis_job(processed_tweet)

    def on_error(self, status_code):
        if status_code == 403:
            return False

    def process_tweet(self, status):
        return {
            'description': status.user.description,
            'loc': status.user.location,
            'text': status.text,
            'coords': json.dumps(status.coordinates),
            'name': status.user.screen_name,
            'user_created': status.user.created_at.now().strftime("%Y-%m-%d %H:%M:%S"),
            'followers': status.user.followers_count,
            'id_str': status.id_str,
            'created': status.created_at.now().strftime("%Y-%m-%d %H:%M:%S"),
            'retweets': status.retweet_count,
            'bg_color': status.user.profile_background_color,
        }

    def add_text_analysis_job(self, obj):
        self.redis.rpush(self.text_job_queue, json.dumps(obj))
