from flask import Flask, redirect, url_for, session, request, jsonify, render_template, flash, make_response
from slack_sdk import WebClient
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
  if type == 'reaction_added':
    slack_client.reactions_add(channel=event['item']['channel'], name=event['reaction'], timestamp=event['item']['ts'])
  return jsonify({'status': 'ok'}), 200


if __name__ == '__main__':
  app.run(debug=True, port=80, host='0.0.0.0')