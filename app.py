from flask import Flask, redirect, url_for, session, request, jsonify, render_template, flash

app = Flask(__name__)

@app.route('/')
def index():
  return('scram!')

# slack bot challenge
@app.route('/small-bot-event')
def small_bot_event():
  json = request.get_json()
  return jsonify({'challenge': json['challenge']})


if __name__ == '__main__':
  app.run(debug=True, port=80, host='0.0.0.0')