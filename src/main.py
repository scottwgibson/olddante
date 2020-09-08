
import boto3
from pathlib import Path
import os
import random
import _pickle as cPickle
from flask import Flask

s3 = boto3.client('s3')
bucket = os.environ['bucketName']
key = 'markov.state'
location = '/tmp/markov.state'
s3.download_file(bucket, key, location)

app = Flask(__name__)

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

@app.route('/', methods=['GET', 'POST'])
def basePath():
    bot = MarkovBot(location = location)

    data = {
        'message': bot.generate()
    }
    return (
        json.dumps(data, indent=4, sort_keys=True),
        200,
        {'Content-Type': 'application/json'}
    )

if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    app.run(host="0.0.0.0", port="3000")