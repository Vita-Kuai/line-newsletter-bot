
from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))

@app.route("/")
def home():
    return "LINE bot is running!"

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except:
        return 'Invalid signature', 400

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    user_id = event.source.user_id
    print(f"🧸 使用者 ID：{user_id}")  # 這行會印出 userId 到 Render 的 log
    reply = TextSendMessage(text='你說了：' + text)
    line_bot_api.reply_message(event.reply_token, reply)
def send_newsletter():
    user_id = '<<在這裡貼上你的 LINE user ID>>'
    message = TextSendMessage(text='📰 這是你的最新電子報：今日大肥語錄：開口就輸了😌')
    line_bot_api.push_message(user_id, message)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

