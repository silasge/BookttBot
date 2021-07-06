import re
from http.client import IncompleteRead
from urllib3.exceptions import ProtocolError
from time import sleep
import logging 
import tweepy 
from booktt.config import create_api

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class BookTTFavRetweetListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api 
        self.me = api.me()


    def on_status(self, tweet):
        logger.info(f'Processando tweet com id {tweet.id}')
        if tweet.in_reply_to_status_id is not None \
            or tweet.user.id == self.me.id:
            return
        if not tweet.retweeted:
            try:
                if tweet.is_quote_status:
                    pattern = r'booktt|booktwitter|bktt|bookstan'
                    quoted_tweet_matches_pat = bool(re.search(pattern, tweet.text))
                    if quoted_tweet_matches_pat:
                        tweet.retweet()
                        logger.info(f'Tweet com id {tweet.id} retuitado com sucesso')
                        sleep(101)
                else:
                    tweet.retweet()
                    logger.info(f'Tweet com id {tweet.id} retuitado com sucesso')
                    sleep(101)
            except:
                logger.error('Problema ao retuitar o tweet', exc_info=True)


    def on_error(self, status_code):
        logger.error(status_code)
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False



def main():
    palavras_chave = ['booktt', 'booktwitter', 'bktt', 'bookstan']
    api = create_api()
    booktt_listener = BookTTFavRetweetListener(api)
    while True:
        try:
            stream = tweepy.Stream(api.auth, booktt_listener)
            stream.filter(track=palavras_chave, languages=['pt'], stall_warnings=True)
        except (IncompleteRead, ProtocolError, ValueError):
            continue
        except KeyboardInterrupt:
            stream.disconnect()
            break


if __name__ == "__main__":
    main()