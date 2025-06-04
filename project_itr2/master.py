from flask import Flask, request, jsonify
import aiohttp
import asyncio
import logging
import time
import uuid
import threading

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

messages = []

SECONDARIES = ['http://secondary1:5001', 'http://secondary2:5001']

async def replicate_to_secondary(secondary, message_data, timeout=15):
    try:
        start_time = time.time()
        logger.info(f"Attempting to replicate to {secondary}")
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{secondary}/replicate", json=message_data, timeout=timeout) as response:
                response.raise_for_status()
                logger.info(f"Received ACK from {secondary} in {time.time() - start_time:.2f}s")
                return True
    except Exception as e:
        logger.error(f"Failed to replicate to {secondary}: {e}")
        return False

def run_async_tasks_in_background(tasks):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(asyncio.gather(*tasks))
    finally:
        loop.close()

@app.route('/messages', methods=['POST'])
def post_message():
    data = request.get_json()
    if not data or 'message' not in data or 'w' not in data:
        logger.error("Invalid request: 'message' and 'w' fields are required")
        return jsonify({"error": "Message and write concern (w) are required"}), 400

    message = data['message']
    w = data['w']
    message_id = str(uuid.uuid4())

    if not isinstance(w, int) or w < 1 or w > len(SECONDARIES) + 1:
        logger.error(f"Invalid write concern: w={w}, must be between 1 and {len(SECONDARIES) + 1}")
        return jsonify({"error": f"Write concern must be between 1 and {len(SECONDARIES) + 1}"}), 400

    message_entry = {"id": message_id, "message": message, "order": len(messages)}
    if any(m["id"] == message_id for m in messages):
        logger.warning(f"Duplicate message ID {message_id}, ignoring")
        return jsonify({"status": "Message already exists"}), 200
    messages.append(message_entry)
    logger.info(f"Stored message: {message} with ID {message_id}")

    tasks = [replicate_to_secondary(secondary, {"id": message_id, "message": message, "order": message_entry["order"]}) for secondary in SECONDARIES]

    if w == 1:
        threading.Thread(target=run_async_tasks_in_background, args=(tasks,), daemon=True).start()
        logger.info(f"Received 1 ACKs, satisfying w={w}")
        return jsonify({"status": "Message replicated", "message_id": message_id}), 200

    async def replicate_with_concern():
        acks = [True]
        required_acks = w - 1

        if w == len(SECONDARIES) + 1:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for result in results:
                acks.append(result if isinstance(result, bool) and result else False)
            return acks

        for task in asyncio.as_completed(tasks, timeout=15):
            try:
                result = await task
                acks.append(result if isinstance(result, bool) and result else False)
                if sum(acks) >= w:
                    return acks
            except Exception as e:
                logger.error(f"Task failed: {e}")
                acks.append(False)
                if sum(acks) >= w:
                    return acks
        return acks

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        acks = loop.run_until_complete(replicate_with_concern())
    finally:
        loop.close()

    if sum(acks) >= w:
        logger.info(f"Received {sum(acks)} ACKs, satisfying w={w}")
        return jsonify({"status": "Message replicated", "message_id": message_id}), 200
    else:
        logger.error(f"Not enough ACKs: received {sum(acks)}, required w={w}")
        return jsonify({"error": "Not enough ACKs received"}), 500

@app.route('/messages', methods=['GET'])
def get_messages():
    logger.info("Returning all messages")
    sorted_messages = sorted(messages, key=lambda x: x["order"])
    return jsonify({"messages": [m["message"] for m in sorted_messages]}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
