from twikit import Client, TooManyRequests
import time
import csv
from datetime import datetime
from configparser import ConfigParser
from random import randint
import asyncio
import pandas as pd


min_tweet = 1


queries = ["目黒駅"] #contents of interest


async def manually_get_tweets(tweets, query):
    if tweets is None: #begin search at every new round
        print(f'{datetime.now()} - Collecting...')
        tweets = await client.search_tweet(query, 'Latest') #get tweets using main function
    else: #use "next" method instead "search" when one round of search is already started
        wait = randint(7,15) #create random wait time to simulate human action
        print(f'{datetime.now()} - Collect after {wait} seconds...')
        time.sleep(wait)
        tweets = await tweets.next()

    return tweets


config = ConfigParser()
config.read('config.ini') #login info stored in cofig
username = config['X']['username']
password = config['X']['password']
email = config['X']['email']

#create a csv file to store the tweets
with open('tweets_info.csv', 'w', newline='', encoding='utf-8-sig') as file:
    csv_file = csv.writer(file)
    csv_file .writerow(['Number', 'Username', 'content', 'Create_time', 'Retweet_count', 'Likes', 'Station'])

client = Client(language='en-US')


async def main():
    #################### uncomment if first use and modify the login credential in config.ini#########################
    await client.login(
        auth_info_1=username ,
        auth_info_2=email,
        password=password
    )
    #################### uncomment if first use and modify the login credential in config.ini#########################
    # client.load_cookies('cookies.json') #use cookie to login after the first login
    for query in queries:
        tweet_count = 0
        tweets = None

        while tweet_count < min_tweet:
            try:
                tweets = await manually_get_tweets(tweets, query)
            except TooManyRequests as error: #pause search until rate limit reset
                reset = datetime.fromtimestamp(error.rate_limit_reset)
                print(f'{datetime.now()} - Rate limit reached. Waiting until {reset}')
                wait = reset - datetime.now()
                time.sleep(wait.total_seconds)
                continue

            if not tweets: #break the loop if no more tweets are found
                print(f'{datetime.now()} - No more tweets found!')
                break

            for tweet in tweets:
                tweet_count += 1
                tweet_data = [tweet_count, tweet.user.name, tweet.text, tweet.created_at, tweet.retweet_count, tweet.favorite_count, query]
                with open(f'tweets_info_{query}.csv', 'a', newline='', encoding='utf-8-sig', errors='replace') as file: #save the data into a csv file
                    csv_file = csv.writer(file)
                    csv_file.writerow(tweet_data)

        print(f'{datetime.now()} - {tweet_count} tweets found!')
    


asyncio.run(main())

