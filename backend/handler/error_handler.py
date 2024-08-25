import time
from flask import jsonify
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")


def check_message(message: str) -> bool:
    if message is None or message == "":
        return False

    return True


def handle_404_json(message: str):
    check_message(message)

    return jsonify({
        "error": "404: NOT FOUND.",
        "message": f"The requested URL was not found on the server. ERR: {message}",
        "status": 404,
        "date": time.time()
    }), 404


def handle_200_json(message: str):
    check_message(message)
    
    return jsonify({
        "error": None,
        "message": f"200: {message}",
        "status": 200,
        "date": time.time()
    }), 200


def handle_400_json(message: str):
    check_message(message)
    
    return jsonify({
        "error": "400: BAD REQUEST.",
        "message": f"There was an error made with the request, please try again. ERR: {message}",
        "status": 400,
        "date": time.time()
    }), 400


def handle_429_json(message: str):
    check_message(message)
    
    return jsonify({
        "error": "429: TOO MANY REQUESTS.",
        "message": f"Too many requests were made, please try again. ERR: {message}",
        "status": 429,
        "date": time.time()
    }), 429
