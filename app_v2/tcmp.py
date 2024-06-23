from flask import Flask, jsonify, request
from flask_caching import Cache
import logging

app = Flask(__name__)
# Configure Flask-Caching
app.config['CACHE_TYPE'] = 'SimpleCache'  # For this example, using simple in-memory cache
cache = Cache(app)

def get_quote_from_request():
    data = request.get_json()
    return data.get('quote', '')

@cache.memoize(timeout=50)  # Cache timeout of 50 seconds
def cached_process_quote(quote):
    # Assume generate_response is a function that generates the explanation
    explanation = generate_response(quote)
    return {
        "quote": quote,
        "explanation": explanation
    }

@app.route('/process_quote', methods=['POST'])
def process_quote():
    try:
        quote = get_quote_from_request()
        if not quote:
            return jsonify({"error": "No quote provided"}), 400

        response = cached_process_quote(quote)
        return jsonify(response), 200
    except Exception as e:
        error_response = {"error": str(e)}
        logging.error(f"Error in process_quote: {error_response}")
        return jsonify(error_response), 500

# Other routes and app initialization here

if __name__ == '__main__':
    app.run(debug=True)