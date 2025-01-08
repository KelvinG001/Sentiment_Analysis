from sentiment_analysis import predict_sentiment, supported_languages
from translate import translate
import csv

# tweet = {
#     "id": 0,  
#     "text": "Ich liebe @Kawabata Zemi um Keio Universitat https://sites.google.com/keio.jp/mizuki-seminar/",
#     "language": "de"
# }

def read_tweets(path):
    with open(path, encoding='utf-8-sig') as file:
        csv_file = csv.DictReader(file)
        tweets = list(csv_file)
    return tweets

tweets = read_tweets("./tweets_info.csv")

for tweet in tweets[:20]:
    text = tweet['content']
    language = "jp"


    if not language or not language in supported_languages:
        translated, language = translate(text)

    if language in supported_languages:
        sentiment = predict_sentiment(text)
    else:
        sentiment = predict_sentiment(translated)
    print(text)
    print(translated)
    print(sentiment)