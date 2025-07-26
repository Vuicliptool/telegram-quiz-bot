from flask import Flask, request
import requests
import os

app = Flask(__name__)

TOKEN = "6737085704:AAFuXOG0aQ6xBldCJYfiqWOIquOcH8PNNek"  # Đảm bảo biến môi trường này tồn tại
if not TOKEN:
    raise ValueError("❌ Thiếu biến môi trường TOKEN!")

URL = f"https://api.telegram.org/bot{TOKEN}/"

questions = [
    {
        "question": "🇻🇳 Thủ đô của Việt Nam là gì?",
        "options": ["Hồ Chí Minh", "Hà Nội", "Đà Nẵng", "Huế"],
        "answer": 1
    },
    {
        "question": "🔢 5 x 6 bằng bao nhiêu?",
        "options": ["30", "11", "60", "56"],
        "answer": 0
    },
    {
        "question": "🌍 Trái đất quay quanh gì?",
        "options": ["Mặt trời", "Mặt trăng", "Sao Hỏa", "Sao Kim"],
        "answer": 0
    }
]

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

@app.route("/", methods=["GET"])
def home():
    return "✅ Bot Telegram Đố Vui Đang Chạy", 200

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

if __name__ == "__main__":
    # Chạy Flask đúng cách trên Railway (public IP)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
