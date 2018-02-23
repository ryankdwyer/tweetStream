import tweepy
import yaml_parser
from auth import Authenticator
from streamer import MyStreamListener

class StreamHandler(Authenticator, MyStreamListener):
    def __init__(self):
        super(StreamHandler, self).__init__()

    def build_api(self, consumer_key, consumer_secret, access_token, access_token_secret):
        self.api = self.get_api(consumer_key, consumer_secret, access_token, access_token_secret)

    def create_stream(self):
        self.stream = tweepy.Stream(auth=self.api.auth, listener=self)

    def start_stream(self, filter_terms):
        if not self.stream:
            raise ValueError("Please create a stream first")

        if not filter_terms:
            raise ValueError("You must supply an array for filter_terms")

        self.stream.filter(track=filter_terms)


if __name__ == '__main__':
    creds = yaml_parser.parse('/Users/ryan/Documents/t_api.yaml')
    print creds
    streamer = StreamHandler()
    streamer.build_api(creds['twitter']['consumer_key'], creds['twitter']['consumer_secret'], creds['twitter']['access_token'], creds['twitter']['access_token_secret'])
    streamer.create_stream()
    streamer.start_stream(['trump'])
