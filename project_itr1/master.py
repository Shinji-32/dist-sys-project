from flask import Flask, request, jsonify
import requests
import logging
import time

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

messages = []

SECONDARIES = ['http://secondary1:5001', 'http://secondary2:5001']

@app.route('/messages', methods=['POST'])
def post_message():
    data = request.get_json()
    if not data or 'message' not in data:
        logger.error("Invalid request: 'message' field is required")
        return jsonify({"error": "Message is required"}), 400

    message = data['message']
    messages.append(message)
    logger.info(f"Stored message: {message}")

    acks = []
    for secondary in SECONDARIES:
        try:
            start_time = time.time()
            response = requests.post(f"{secondary}/replicate", json={'message': message}, timeout=10)
            response.raise_for_status()
            acks.append(True)
            logger.info(f"Received ACK from {secondary} in {time.time() - start_time:.2f}s")
        except requests.RequestException as e:
            logger.error(f"Failed to replicate to {secondary}: {e}")
            return jsonify({"error": f"Failed to replicate to {secondary}"}), 500

    if all(acks):
        logger.info("All Secondaries acknowledged")
        return jsonify({"status": "Message replicated"}), 200
    else:
        logger.error("Not all Secondaries acknowledged")
        return jsonify({"error": "Replication failed"}), 500

@app.route('/messages', methods=['GET'])
def get_messages():
    logger.info("Returning all messages")
    return jsonify({"messages": messages}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
