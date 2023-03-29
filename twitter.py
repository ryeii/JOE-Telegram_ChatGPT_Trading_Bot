'''
twint tutorial: https://medium.com/@kevctae/twitter-scraping-without-using-twitter-api-2022-guide-39eaec7ccade
pymongo turotial: https://pymongo.readthedocs.io/en/stable/tutorial.html
'''

'''
TODO: figure out why does the number of tweets scraped not equal to the limit
TODO: figure out how to avoid duplicate tweets
'''

import twint
import pandas as pd
from pymongo import MongoClient
import datetime
from pprint import pprint

'''
Return a pandas dataframe of scraped tweets
'''
def scrape_tweets(username, search, limit):

    config = twint.Config()

    config.Username = username
    config.Search = search
    config.Limit = limit
    config.Pandas = True

    twint.run.Search(config=config)
    return twint.storage.panda.Tweets_df


'''
Scrape and store tweets in MongoDB
'''
def enter_tweets(mongodb_uri, database, collection, username, search, limit):

    df = scrape_tweets(username=username, search=search, limit=limit).to_dict('records')

    target = MongoClient(mongodb_uri)[database][collection]

    re = target.insert_many(df)

    return re


# test
client = MongoClient('mongodb://localhost:27017/')
db = client['test-database']
collection = db['test-collection']
collection.drop()

enter_tweets('mongodb://localhost:27017/', 'test-database', 'test-collection', 'elonmusk', 'tesla', 10)

# print number of documents in collection
print(collection.count_documents({}))

# write all documents in collection to a file
with open('test.txt', 'w') as f:
    cursor = collection.find({})
    for document in cursor:
        f.write(str(document) + '\n')

# cursor = collection.find({})
# for document in cursor: 
#     pprint(document)