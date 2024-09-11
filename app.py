import logging
from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from config import LINE_CHANNEL_SECRET
from line_bot_utils import process_message

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    logging.info(f"Received webhook body: {body}")
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    message = event.message.text
    reply_token = event.reply_token
    process_message(message, reply_token)

@app.route("/test")
def test():
    return "Hello, LINE Bot!"

if __name__ == "__main__":
    app.run(debug=True)
