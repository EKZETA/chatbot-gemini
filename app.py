import os
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template 
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

try:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
    print("Model Gemini berhasil dikonfigurasi.")
except Exception as e:
    print(f"Error: Terjadi kesalahan saat konfigurasi model. {e}")
    exit()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({"error": "Pesan tidak boleh kosong"}), 400
    try:
        response = model.generate_content(user_message)
        bot_response = response.text
        return jsonify({"reply": bot_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)