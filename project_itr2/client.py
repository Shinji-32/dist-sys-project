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
    if not data or 'id' not in data or 'message' not in data or 'order' not in data:
        logger.error("Invalid request: 'id', 'message', and 'order' fields are required")
        return jsonify({"error": "ID, message, and order are required"}), 400

    message_id = data['id']
    message = data['message']
    order = data['order']

    if any(m["id"] == message_id for m in messages):
        logger.warning(f"Duplicate message ID {message_id}, ignoring")
        return jsonify({"status": "ACK"}), 200

    time.sleep(8)
    messages.append({"id": message_id, "message": message, "order": order})
    logger.info(f"Replicated message: {message} with ID {message_id}")
    return jsonify({"status": "ACK"}), 200

@app.route('/messages', methods=['GET'])
def get_messages():
    logger.info("Returning all messages")
    sorted_messages = sorted(messages, key=lambda x: x["order"])
    return jsonify({"messages": [m["message"] for m in sorted_messages]}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
