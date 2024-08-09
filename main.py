import slack
import os
from pathlib import Path
from dotenv import load_dotenv
import ssl
import certifi
from flask import Flask
from slackeventsapi import SlackEventAdapter

# Load environment variables from .env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_events_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'],'/slack/events', app)


# Create an SSL context
ssl_context = ssl.create_default_context(cafile=certifi.where())

# Initialize Slack client with SSL context
client = slack.WebClient(token=os.environ['SLACK_TOKEN'], ssl=ssl_context)
BOT_ID = client.api_call('auth.test')['user_id']

@slack_events_adapter.on('message')
def handle_message(payload):
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')

    if BOT_ID != user_id:
        client.chat_postMessage(channel=channel_id, text=text)

# Send a message to the #general channel
try:
    response = client.chat_postMessage(channel='#slack-bot-test', text='哈咯')
    print(f"Message sent successfully: {response}")
except Exception as e:
    print(f"Error: {e}")

if __name__ == "__main__":
    app.run(debug=True)