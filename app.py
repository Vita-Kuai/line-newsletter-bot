
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

import json
import hashlib
import hmac
import base64

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    
    print("📩 收到 LINE 的 webhook！")
    print("📦 webhook 原始內容：", body)

    # 驗證簽章（自己算）
    hash = hmac.new(
        os.getenv('CHANNEL_SECRET').encode('utf-8'),
        body.encode('utf-8'),
        hashlib.sha256
    ).digest()

    computed_signature = base64.b64encode(hash).decode('utf-8')

    print("🧾 驗證用簽章：", computed_signature)
    print("🆚 LINE 傳來簽章：", signature)

    if computed_signature != signature:
        print("❌ 簽章不符合！拒絕處理")
        return 'Invalid signature', 400

    # 轉成 JSON 看有沒有 userId
    try:
        data = json.loads(body)
        print("👤 webhook 內容解析後：", data)
        if 'events' in data and len(data['events']) > 0:
            uid = data['events'][0]['source']['userId']
            print("🧸 抓到 userId：", uid)
    except Exception as e:
        print("❌ webhook 資料解析錯誤：", str(e))

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

