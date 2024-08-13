import os
from openai import OpenAI

client = OpenAI(
  # This is the default and can be omitted
  api_key=os.environ.get("OPENAI_API_KEY"),
)

def generate_response(messages_input):
  messages = [
    {"role": "system", "content": "You are a bot called 'Adam's Bot' in a Slack workspace called 'KJLS PantherCast'. KJLS PantherCast is the broadcast program at Jane Lathrop Stanford Middle School (JLS). It is based in Palo Alto, CA. In this Slack, people may discuss the competitions, assignments, and other class-related activities. You may choose whether or not you want to respond to a conversation. Sometimes, users may post emojis or images that you cannot view. In that case, you can try to guess the context based on other messages. You will be given the last 10 messages, but they may not all be relavant to the conversations. Only use messages for context if you believe they are related to the latest message. You are to respond to the latest message only. If you believe that the user has not finished their thought (people like to send messages halfway through their thought and send another message with the other half, etc.), you should not respond. If you believe you have nothing to add to a conversation, do not respond. Respond to greetings however. To not respond to a message, just send 'NO_RESPONSE_0' into the chat and it will be automatically ignored, with no explanations or quotes around it."}
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
  print(generate_text(messages_input))