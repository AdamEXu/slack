import os
from openai import OpenAI

client = OpenAI(
  # This is the default and can be omitted
  api_key=os.environ.get("OPENAI_API_KEY"),
)

def generate_response(messages_input):
  messages = [
    {"role": "system", "content": "You are a bot called 'Adam's Bot' in a Slack workspace called 'KJLS PantherCast'. Kindly respond to messages in a short and concise manner. Use emojis to enhance your responses. Do not start out your message with Adam's Bot:."}
  ]
  for message in messages_input:
    # print(message)
    messages.append({"role": "user", "content": f"{message['user']}: {message['content']}"})
  
  completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
  )
  return completion.choices[0].message.content

if __name__ == "__main__":
  messages_input = [
    {"user": "Adam", "content": "hello!"}
  ]
  print(generate_response(messages_input))