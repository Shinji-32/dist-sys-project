from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

messages = []

@app.route('/echo', methods=['POST'])
def echo_post():
    data = request.get_json()
    if not data or 'message' not in data:
        logger.error("Invalid request: 'message' field is required")
        return jsonify({"error": "Message is required"}), 400

    message = data['message']
    messages.append(message)
    logger.info(f"Received and stored message: {message}")
    return jsonify({"received": message}), 200

@app.route('/echo', methods=['GET'])
def echo_get():
    logger.info("Returning all messages")
    return jsonify({"messages": messages}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
