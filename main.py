from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Lấy token từ biến môi trường
TOKEN = "6737085704:AAFuXOG0aQ6xBldCJYfiqWOIquOcH8PNNek"
if not TOKEN:
    raise ValueError("❌ Thiếu biến môi trường TOKEN!")

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

user_state = {}

# Gửi tin nhắn đến Telegram
def send_message(chat_id, text):
    payload = {"chat_id": chat_id, "text": text}
    try:
        requests.post(URL + "sendMessage", json=payload, timeout=5)
    except Exception as e:
        print("❌ Lỗi gửi tin nhắn:", e)

# Gửi câu hỏi
def send_question(chat_id, index):
    if index >= len(questions):
        send_message(chat_id, "🎉 Bạn đã hoàn thành tất cả câu hỏi!")
        user_state.pop(chat_id, None)
        return
    q = questions[index]
    msg = f"❓ {q['question']}\n"
    for i, opt in enumerate(q["options"]):
        msg += f"{chr(65+i)}. {opt}\n"
    send_message(chat_id, msg)

# Xử lý webhook
@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    print("📩 Nhận dữ liệu:", data)

    if "message" not in data:
        return "OK", 200

    message = data["message"]
    chat_id = message.get("chat", {}).get("id")
    text = message.get("text", "").strip().upper()

    if not chat_id:
        print("❌ Không lấy được chat_id!")
        return "OK", 200

    if text == "/START":
        user_state[chat_id] = 0
        send_question(chat_id, 0)
    elif chat_id in user_state:
        index = user_state[chat_id]
        correct = questions[index]["answer"]
        if text in ["A", "B", "C", "D"]:
            guess = ord(text) - 65
            if guess == correct:
                send_message(chat_id, "✅ Chính xác!")
            else:
                send_message(chat_id, f"❌ Sai. Đáp án đúng là {chr(65+correct)}.")
            user_state[chat_id] += 1
            send_question(chat_id, user_state[chat_id])
        else:
            send_message(chat_id, "⛔ Trả lời bằng A/B/C/D thôi nha.")
    else:
        send_message(chat_id, "👉 Gõ /start để bắt đầu!")

    return "OK", 200  # 🔴 Trả lời nhanh để tránh timeout

# Cho chạy nếu deploy local
if __name__ == "__main__":
    app.run(debug=True)
