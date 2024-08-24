from flask import jsonify

def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(error):
        response = {
            "error": "404: NOT FOUND.",
            "message": "The requested resource you are looking for could not be found.",
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
            "message": "It's not you, it's us. We are experiencing some technical difficulties.",
            "status": 500
        }
        return jsonify(response), 500