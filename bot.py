# -*- coding: utf-8 -*-
"""
Created on Tues Jul 27 21:45:00 2021

@author: jaydenclark
"""

import tweepy, time

class bot():
    def __init__(self):
        #Enter personal API details below
        self.consumer_key = ''
        self.consumer_secret = ''
        self.access_token = ''
        self.access_secret = ''

        self.api = None
        self.last_seen_id = None

        self.file_name = 'last_seen_id.txt'

        #Enter values in terminal when running.
        self.hashtag = str(input('Enter name of hashtag to scrape: ')) 
        self.comment = str(input('Enter your automatic comment: '))
            

    def login(self):

        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_secret)
        self.api = tweepy.API(auth)

    def retrieve_last_seen_id(self, file_name):
        f_read = open(file_name, 'r')
        last_seen_id = int(f_read.read().strip())
        f_read.close()
        return last_seen_id

    def store_last_seen_id(self, last_seen_id, file_name):
        f_write = open(file_name, 'w')
        f_write.write(str(last_seen_id))
        f_write.close()
        return

    def reply_to_tweets(self):
        print('checking that hashtage is valid...', flush=True)
        if self.hashtag.startswith('#') == False:
            raise Exception('Remember to inlude the hash symbol at the beginning! Try again!') #be sure to include a hashtag in your input!
        else:
            print('Valid Hashtag!')

        while True:
            print('retrieving and replying to tweets...', flush=True)

            self.last_seen_id = self.retrieve_last_seen_id(self.file_name)
            
            hashtags = self.api.home_timeline(
                                20,
                                self.last_seen_id, 
                                tweet_mode='extended')
            for hashtags in reversed(hashtags):
                print(str(hashtags.id) + ' - ' + hashtags.full_text, flush=True)
                self.last_seen_id = hashtags.id
                self.store_last_seen_id(self.last_seen_id, self.file_name)
                if self.hashtag in hashtags.full_text.lower():
                    print(f'found {self.hashtag}', flush=True)
                    print('responding back...', flush=True)
                    self.api.update_status('@' + hashtags.user.screen_name +
                                    self.comment, 
                                    hashtags.id
                                    )
            time.sleep(15)

if __name__ == '__main__':
    b = bot()
    b.login()
    b.reply_to_tweets()
        