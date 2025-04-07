
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

    print("📩 收到 LINE 的 webhook 訊息囉！")  # ← 新加這行！
    print("📦 webhook 資料：", body)  # ← 印出完整 webhook 內容幫你 debug

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

