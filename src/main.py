
import boto3
from pathlib import Path
import os
import random
import _pickle as cPickle

s3 = boto3.client('s3')
bucket = os.environ['bucketName']
key = 'markov.state'
location = '/tmp/markov.state'
s3.download_file(bucket, key, location)

class MarkovBot:
    MAXGEN = 1000
    NONWORD = '\n'

    def __init__(self, location):
        dataFile = open(location, 'rb')
        self.dict = cPickle.load(dataFile, encoding='latin1')
        return

    def generate(self):
        word1 = self.NONWORD
        word2 = self.NONWORD
        text = ""

        for i in range(self.MAXGEN):
            if (word1,word2) not in self.dict:
                successorList = random.choice(self.dict.keys())
            else:
                successorList = self.dict[(word1,word2)]

            word3 = random.choice(successorList)

            if word3 == self.NONWORD:
                break

            text = text + " " + word3
            word1, word2 = word2, word3

        return text

def my_handler(event, context):
    bot = MarkovBot(location = location)
    
    return { 
        'message' : bot.generate()
    }  