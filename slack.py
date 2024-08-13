from slack_sdk import WebClient
import os
import time

SLACK_API_TOKEN = os.environ.get("SLACK_API_TOKEN")
if SLACK_API_TOKEN is None:
    print("Please set the environment variable SLACK_API_TOKEN")
    exit(1)

slack_client = WebClient(token=SLACK_API_TOKEN)

def get_public_channels():
    cursor = None
    channels = []
    while True:
        response = slack_client.conversations_list(cursor=cursor)
        for channel in response["channels"]:
            channels.append(channel["id"])
            cursor = response["response_metadata"]["next_cursor"]
            if len(cursor) == 0:
                break
            else:
                print("Pagination found, getting next entries")
                time.sleep(3)
        return channels

def get_thread_messages(slack_channel, ts):
    messages = []
    cursor = None
    while True:
        thread_replies = slack_client.conversations_replies(channel=slack_channel, ts=ts, cursor=cursor)
        for message in thread_replies["messages"]:
            if (message["type"] == "message"):
                messages.append(message["text"])
        if bool(thread_replies["has_more"]):
            cursor = thread_replies["response_metadata"]["next_cursor"]
        else:
            cursor = None
        if cursor is None:
            break
        else:
            print("Pagination found, getting next entries")
            time.sleep(1.2)
    return messages
        
def get_channel_messages(slack_channels):
    messages = []
    for slack_channel in slack_channels:
        cursor = None
        while True:
            channel_history = slack_client.conversations_history(channel=slack_channel, cursor=cursor)
            for message in channel_history["messages"]:
                if (message["type"] == "message"):
                    if ("thread_ts" in message):
                        for text in get_thread_messages(slack_channel, message["ts"]):
                            messages.append((slack_channel, text))
                    else:
                        messages.append((slack_channel, message["text"]))
            if bool(channel_history["has_more"]):
                cursor = channel_history["response_metadata"]["next_cursor"]
            else:
                cursor = None
            if cursor is None:
                break
            else:
                print("Pagination found, getting next entries")
                time.sleep(1.2)
    return messages

slack_channels = get_public_channels()
print(slack_channels)
messages = get_channel_messages(slack_channels)
print(messages)