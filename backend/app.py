from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from model.chatbot_model import chatbot_response  # Import chatbot function

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend-backend communication

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    try:
        bot_response = chatbot_response(user_input)
        return jsonify({"response": bot_response})
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
