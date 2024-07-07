# app.py
from flask import Flask, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route("/")
def home():
    return jsonify({"message": "Welcome to the rate-limited API!"})

@app.route("/limited")
@limiter.limit("5 per minute")
def limited():
    return jsonify({"message": "This endpoint is rate-limited to 5 requests per minute."})

if __name__ == "__main__":
    app.run(debug=True)