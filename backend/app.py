from flask import Flask, jsonify, request
from config.log import logger as log
from flask import abort, redirect, request

import time

app = Flask(__name__)


@app.errorhandler(404)
def not_found(error):
    response = {
        "error": "404: NOT FOUND.",
        "message": "THe requested resource you are looking for could not be found.",
        "status": 404
    }

    return jsonify(response), 404


@app.errorhandler(429)
def too_many_requests(error):
    response = {
        "error": "429: TOO MANY REQUESTS.",
        "message": "You have exceeded the maximum number of requests allowed.",
        "status": 429
    }

    return jsonify(response), 429


@app.errorhandler(500)
def internal_server_error(error):
    response = {
        "error": "500: INTERNAL SERVER ERROR.",
        "message": "Its not you, its us. We are experiencing some technical difficulties.",
        "status": 500
    }

    return jsonify(response), 500


@app.route("/transcribe", methods=['POST'])
def transcribe():  # put application's code here
    if "file" not in request.files:
        return jsonify({
            "error": "400: BAD REQUEST.",
            "message": "No file part in the request.",
            "status": 400
        }), 400

    file = request.files["file"]

    file_path = f"./temp/{file.filename}"
    file.save(file_path)

    # TODO: Turn .mp4 to .wav
    # TODO: Transcribe .wav file to text using AI (TBD)
    # TODO: Return transcribed text in JSON
    # TODO: Store in Database (TBD)
    # TODO: Delete .wav file ./uploads
    # TODO: Delete .mp4 file from ./temp


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        if request.files:
            file = request.files["file"]
            file.save(f"./uploads/{file.filename}_{time.time()}.")


if __name__ == '__main__':
    start_time = time.time()
    app.run(debug=True)
    log.info(f"Application started in {time.time() - start_time} seconds")

