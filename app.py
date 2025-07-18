import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

try:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel("gemini-1.5-flash")
    print("Model berhasil dikonfigurasi")
except AttributeError as e:
    print(f"Error: {e}. Pastikan Anda telah mengatur variabel lingkungan dengan benar.")
    exit()

@app.route('/', methods=["POST"])
def chat():
    user_message = request.json.get("message")

    if not user_message:
        return jsonify({"error":"Pesan tidak boleh kosong"}), 400
    
    try:
        response = model.generate_content(user_message)
        bot_response = response.text
        return jsonify({"reply": bot_response})
    
    except Exception as e:
        return jsonify({"error":str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)