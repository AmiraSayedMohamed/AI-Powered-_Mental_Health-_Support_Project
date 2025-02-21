from flask import Flask, request, jsonify
import openai
from flask_cors import CORS
import os
from flask import send_from_directory
from dotenv import load_dotenv
app = Flask(__name__)

CORS(app)  # Enable CORS for frontend-backend communication
load_dotenv()
# # Set your OpenAI API key here
OPENAI_API_KEY=""
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/")
def serve_frontend():
    return send_from_directory("../frontend", "index.html")

@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory("../frontend", path)

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    try:
        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a mental health assistant. Be empathetic and supportive."},
                {"role": "user", "content": user_input}
            ]
        )
        bot_response = response['choices'][0]['message']['content']
        return jsonify({"response": bot_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)