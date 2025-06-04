from flask import Flask, request, jsonify
import logging
import time

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

messages = []

@app.route('/replicate', methods=['POST'])
def replicate_message():
    data = request.get_json()
    if not data or 'message' not in data:
        logger.error("Invalid request: 'message' field is required")
        return jsonify({"error": "Message is required"}), 400

    message = data['message']
    time.sleep(2)
    messages.append(message)
    logger.info(f"Replicated message: {message}")
    return jsonify({"status": "ACK"}), 200

@app.route('/messages', methods=['GET'])
def get_messages():
    logger.info("Returning all messages")
    return jsonify({"messages": messages}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
