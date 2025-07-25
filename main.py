from flask import Flask, request
import requests
import os

app = Flask(__name__)

# ✅ Lấy token từ biến môi trường (Railway)
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    print("❌ Lỗi: Chưa thiết lập biến môi trường TOKEN")
URL = f"https://api.telegram.org/bot{TOKEN}/"

# ✅ Câu hỏi đố vui
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

# ✅ Lưu trạng thái người chơi
user_state = {}

def send_message(chat_id, text):
    payload = {"chat_id": chat_id, "text": text}
    r = requests.post(URL + "sendMessage", json=payload)
    print("📤 Gửi tin nhắn:", r.text)

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

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    print("📩 Dữ liệu nhận:", data)

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
                send_message(chat_id, "⛔ Vui lòng trả lời bằng A / B / C / D.")
        else:
            send_message(chat_id, "👉 Gõ /start để bắt đầu chơi.")
    return "OK", 200

# ✅ Khởi chạy Flask app (nếu chạy local)
if __name__ == "__main__":
    print("🚀 Bot đang chạy...")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
