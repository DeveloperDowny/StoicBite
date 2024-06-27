import os
import time
from flask_caching import Cache
import logging
from flask import Flask, jsonify
import requests
from openai import OpenAI
from flask import request, Response
from flask_cors import CORS
import threading
import logging
from collections import deque
import random
import json
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# ... (keep your existing imports and configurations)

app = Flask(__name__)
CORS(app)

# Configure rate limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["5 per minute", "100 per day"],
    storage_uri="memory://"
)

# ... (keep your existing code)

@app.route('/daily_stoic', methods=['GET'])
@limiter.limit("5 per minute")  # Apply rate limiting to this route
def daily_stoic():
    global processing_quote
    try:
        # Check if rate limit is exceeded
        if getattr(request, 'limited', False):
            # If rate limit is exceeded, return a random quote from stale_quote_queue
            if len(stale_quote_queue) > 0:
                response = random.choice(stale_quote_queue)
                logger.info(f"Rate limit exceeded. Serving from stale_quote_queue: {response}")
                return jsonify(response), 200
            else:
                return jsonify(fallback_res), 200

        # If rate limit is not exceeded, proceed with the original logic
        if len(ready_quote_queue) > 0:
            response = ready_quote_queue.popleft()

            if kDebugMode:
                thread = threading.Thread(target=long_running_task, kwargs={
                            'post_data': {}})
            else:
                thread = threading.Thread(target=long_running_task_of_fetching_quote_and_explanation, kwargs={
                            'post_data': {}})
                
            thread.start()
            logger.info(f"Successful response from ready_quote_queue: {response}")
            return jsonify(response), 200

        if len(stale_quote_queue) > 0:
            if not processing_quote and len(ready_quote_queue) == 0:
                processing_quote = True
                if kDebugMode:
                    thread = threading.Thread(target=long_running_task, kwargs={
                            'post_data': {}})
                else:
                    thread = threading.Thread(target=long_running_task_of_fetching_quote_and_explanation, kwargs={
                            'post_data': {}}) 
                thread.start()
            
            response = random.choice(stale_quote_queue)
            logger.info(f"Successful response from stale_quote_queue: {response}")
            return jsonify(response), 200

        return jsonify(fallback_res), 200 
    except Exception as e:
        error_response = {"error": str(e)}
        logger.error(f"Error in daily_stoic: {error_response}")
        return jsonify(error_response), 500

# ... (keep your existing code for other routes)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))