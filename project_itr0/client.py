import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def send_message(message):
    url = 'http://server:5000/echo'
    data = {'message': message}
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        logger.info(f"Sent message: {message}, Received: {response.json()}")
    except requests.RequestException as e:
        logger.error(f"Failed to send message: {e}")

def get_messages():
    url = 'http://server:5000/echo'
    try:
        response = requests.get(url)
        response.raise_for_status()
        logger.info(f"Retrieved messages: {response.json()}")
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve messages: {e}")

if __name__ == '__main__':
    send_message("Hello, Echo Server!")
    get_messages()
