from flask import Flask, request
import requests
import os
import json

app = Flask(__name__)
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("❌ Thiếu biến môi trường TOKEN!")

URL = f"https://api.telegram.org/bot{TOKEN}/"

# Load câu hỏi từ file JSON
with open("questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

user_state = {}

def send_message(chat_id, text):
    requests.post(URL + "sendMessage", json={"chat_id": chat_id, "text": text})

def send_question(chat_id, index):
    if index >= len(questions):
        send_message(chat_id, "🎉 Bạn đã hoàn thành tất cả câu hỏi!")
        user_state.pop(chat_id, None)
        return
    q = questions[index]
    msg = f"❓ {q['question']}\n"
    for i, opt in enumerate(q['options']):
        msg += f"{chr(65+i)}. {opt}\n"
    send_message(chat_id, msg)

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "").strip().upper()

        if text == "/START":
            user_state[chat_id] = 0
            send_question(chat_id, 0)
        elif chat_id in user_state:
            index = user_state[chat_id]
            correct = questions[index]["answer"]
            if text in ["A", "B", "C", "D"]:
                guess = ord(text) - 65
                if guess == correct:
                    send_message(chat_id, "✅ Đúng rồi!")
                else:
                    send_message(chat_id, f"❌ Sai. Đáp án đúng là {chr(65+correct)}.")
                user_state[chat_id] += 1
                send_question(chat_id, user_state[chat_id])
            else:
                send_message(chat_id, "⛔ Trả lời bằng A/B/C/D thôi nha.")
        else:
            send_message(chat_id, "👉 Gõ /start để bắt đầu.")
    return "OK", 200
