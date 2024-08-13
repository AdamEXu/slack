from flask import Flask, redirect, url_for, session, request, jsonify, render_template, flash, make_response
from slack_sdk import WebClient
from openai_utils import generate_response
import os

SLACK_API_TOKEN = os.environ.get("SLACK_API_TOKEN")
if SLACK_API_TOKEN is None:
    print("Please set the environment variable SLACK_API_TOKEN")
    exit(1)

slack_client = WebClient(token=SLACK_API_TOKEN)

BOT_SLACK_ID = "U07GCL7QHT9"

app = Flask(__name__)

@app.route('/')
def index():
  return('scram!')

# slack bot challenge
@app.route('/small-bot-event', methods=['POST'])
def small_bot_event():
  json = request.get_json()
  event = json['event']
  if event['user'] == BOT_SLACK_ID:
    return jsonify({'status': 'ok'}), 200
  type = event['type']
  print(type)
  if type == 'reaction_added':
    slack_client.reactions_add(channel=event['item']['channel'], name=event['reaction'], timestamp=event['item']['ts'])
  elif type == 'app_mention':
    if event['user'] == BOT_SLACK_ID:
      return jsonify({'status': 'ok'}), 200
    # get last 10 messages
    messages = slack_client.conversations_history(channel=event['channel'], limit=10)
    messages_improved = []
    # example: [{"user_name": "Adam", "text": "Hello"}]
    for message in messages['messages']:
      user = slack_client.users_info(user=message['user'])
      messages_improved.append({'user': user['user']['real_name'], 'content': message['text']})
    messages_improved = messages_improved.reverse()
    print(messages_improved)
    print("generating response")
    response = generate_response(messages_improved)
    print(response)
    if response != 'NO_RESPONSE_0':
      slack_client.chat_postMessage(channel=event['channel'], text=response)
  return jsonify({'status': 'ok'}), 200


if __name__ == '__main__':
  app.run(debug=True, port=80, host='0.0.0.0')