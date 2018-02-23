from redis_obj import Redis
from textblob import TextBlob
import dataset
import json

class TextAnalyzer:
    def __init__(self):
        self.text_job_queue = 'TEXT_ANALYSIS_JOB'
        self.redis = Redis().build_redis()
        self.db = dataset.connect("sqlite:///tweets.db")

    
    def get_job(self):
        return self.redis.lpop(self.text_job_queue)

    def get_sentiment(self, status):
        print status
        if not status['text']:
            print "no text"
            return False

        text = TextBlob(status['text'])
        status['polarity'] = text.sentiment.polarity
        status['subjectivity'] = text.sentiment.subjectivity
        print status
        return status

    def write_to_db(self, table, obj):
        self.db[table].insert(obj)

    def run(self):

        while (True):

            job = self.get_job()
            if not job:
                continue

            job = json.loads(job)

            processed = self.get_sentiment(job)

            self.write_to_db('tweet', processed)


if __name__ == '__main__':
    text_analyzer = TextAnalyzer()
    text_analyzer.run()


