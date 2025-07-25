from flask import Flask, request
import requests

app = Flask(__name__)

# GÁN TOKEN TRỰC TIẾP
TOKEN = "6737085704:AAFuXOG0aQ6xBldCJYfiqWOIquOcH8PNNek"
URL = f"https://api.telegram.org/bot{TOKEN}/"

# Danh sách câu hỏi
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

# Trạng thái người chơi
user_state = {}

# Gửi tin nhắn
def send_message(chat_id, text):
    requests.post(URL + "sendMessage", json={"chat_id": chat_id, "text": text})

# Gửi câu hỏi
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

# Webhook handler
@app.route("/", methods=["POST"])
def webhook():
    try:
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
    except Exception as e:
        print(f"❌ Lỗi webhook: {e}")
        return "ERROR", 500

# Cần để Railway khởi động web server
@app.route("/", methods=["GET"])
def index():
    return "Bot Telegram Đố Vui Đang Chạy ✅", 200
