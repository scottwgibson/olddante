
__name__ = '.'.join(__name__.split('/'))
__package__ = '.'.join('.'.join(__name__.split('/')).split('.')[:-1])

import boto3
import os
from flask import Flask
import json
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from markov import MarkovBot

s3 = boto3.client('s3')
bucket = os.environ['bucketName']
key = 'markov.state'
location = '/tmp/markov.state'
s3.download_file(bucket, key, location)


ssm = boto3.client('ssm')
bot_token = ssm.get_parameter(Name='/olddante/slack/bot_token', WithDecryption=False)['Parameter']['Value']
slack_secret = ssm.get_parameter(Name='/olddante/slack/signing_secret', WithDecryption=False)['Parameter']['Value']

app = Flask(__name__)
slack_events_adapter = SlackEventAdapter(slack_secret, "/slack/events", app)
slack = WebClient(token=bot_token)

bot = MarkovBot(location = location)

@slack_events_adapter.on("app_mention")
def message(payload):
    event = payload.get("event", {})

    channel_id = event.get("channel")
    user_id = event.get("user")
    text = event.get("text")

    slack.chat_postMessage(
        channel=channel_id,
        text=bot.generate())

@app.route('/', methods=['GET', 'POST'])
def basePath():
    data = {
        'message': bot.generate()
    }
    return (
        json.dumps(data, indent=4, sort_keys=True),
        200,
        {'Content-Type': 'application/json'}
    )