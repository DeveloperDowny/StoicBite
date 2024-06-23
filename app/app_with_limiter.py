from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from functools import wraps

app = Flask(__name__)

# Rate Limiter Setup
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["5 per minute"]
)

# API Key Verification
VALID_API_KEYS = {"key1", "key2"}

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-KEY')
        if api_key not in VALID_API_KEYS:
            return jsonify({"error": "Unauthorized"}), 403
        return f(*args, **kwargs)
    return decorated_function

@app.route('/get_stoic_quote', methods=['GET'])
@limiter.limit("3 per minute")
@require_api_key
def get_stoic_quote():
    # Your endpoint logic here
    return jsonify({"response": "Quote and explanation"})

if __name__ == '__main__':
    app.run(debug=True)