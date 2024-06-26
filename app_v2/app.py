import os
import time
from flask_caching import Cache
import logging
from flask import Flask, jsonify
import requests
from openai import OpenAI
from k import oakv1, quote_url

from flask import request, Response
from flask_cors import CORS
 
 

# Set up logging
logging.basicConfig(filename='stoic_app.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
CORS(app)

# Configure Flask-Caching
app.config['CACHE_TYPE'] = 'SimpleCache'  # For this example, using simple in-memory cache
cache = Cache(app)

def get_quote_from_request():
    data = request.get_json()
    logging.info("Received request for quote processing.")
    return data.get('quote', '')

@cache.memoize(timeout=50)  # Corrected cache timeout to 50 seconds
def cached_process_quote(quote):
    start_time = time.time()  # Start timing
    # Assume generate_response is a function that generates the explanation
    explanation = generate_response(quote)
    end_time = time.time()  # End timing
    time_taken = end_time - start_time
    # Log the time taken to process the quote, indicating cache miss
    logging.info(f"Processed quote in {time_taken:.2f} seconds. Cache miss.")
    return {
        "quote": quote,
        "explanation": explanation
    }

# Configure OpenAI client
# client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
client = OpenAI(api_key=oakv1)

def fetch_quote():
    """Fetch a quote from the Stoic Quote API."""
    # url = "https://stoic-quote-api.onrender.com/aurelius"
    url = quote_url
    response = requests.get(url)
    if response.status_code == 200:
        quote = response.text
        logging.info(f"Fetched quote: {quote}")
        return quote
    else:
        error_msg = f"Failed to fetch quote from API. Status code: {response.status_code}"
        logging.error(error_msg)
        raise Exception(error_msg)

def generate_response(quote):
    """Generate a response using OpenAI's GPT-4 model."""
    prompt = f"""Play the role of Marcus Aurelius. You don't know that you are playing a role. You teach take one of your quote daily and teach it to your pupil. Explain today's quote. Today's quote is within <quote></quote> tags below
<quote>
"{quote}"
</quote>
Do not do more than what's asked."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=512
        )
        explanation = response.choices[0].message.content
        logging.info(f"Generated explanation: {explanation}")
        return explanation
    except Exception as e:
        error_msg = f"Error generating response: {str(e)}"
        logging.error(error_msg)
        raise Exception(error_msg)

@app.route('/daily_stoic', methods=['GET'])
def daily_stoic():
    try:
        quote = fetch_quote()
        explanation = generate_response(quote)
        response = {
            "quote": quote,
            "explanation": explanation
        }
        logging.info(f"Successful response: {response}")
        return jsonify(response), 200
    except Exception as e:
        error_response = {"error": str(e)}
        logging.error(f"Error in daily_stoic: {error_response}")
        return jsonify(error_response), 500

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


# dummy test endpoint 
@app.route('/test', methods=['POST'])
def test():

    explaination = """Listen to these words, dear pupil: "And he does live with the gods who constantly shows to them, his own soul is satisfied with that which is assigned to him, and that it does all that the daemon wishes, which Zeus hath given to every man for his guardian and guide, a portion of himself."\nTo live with the gods means to live a life that aligns with divine virtue and wisdom. When a person shows the gods that their soul is content with their lot in life, they demonstrate a profound acceptance and understanding of their role in the universe. This satisfaction is not born of passive resignation but of active embrace of one's destiny and duties.\nEach man, by the will of Zeus, has been blessed with a daemon, a guiding spirit, a portion of the divine that steers him. To live in harmony with this daemon is to heed its counsel, to live virtuously, and to fulfill one's purpose. Thus, true contentment and divine unity are found not in external circumstances but within our inner acceptance and alignment with the higher \n Reflect upon this, and seek the serenity that comes from fulfilling the divine duty assigned to you by fate."""

    quote = """And he does live with the gods who constantly shows to them, his own soul is satisfied with that which is assigned to him, and that it does all that the daemon wishes, which Zeus hath given to every man for his guardian and guide, a portion of himself."""

    quote_by = """Marcus Aurelius"""
    return jsonify({
        "quote": quote,
        "quote_by": quote_by,
        "explanation": explaination 
    }), 200

if __name__ == '__main__':
    # app.run(debug=True)
    # q = '''"A man should always have these two rules in readiness the one, to do only whatever the reason of the ruling and legislating faculty may suggest for the use of men the other, to change thy opinion, if there is anyone at hand who sets thee right and moves thee from any opinion." --Marcus Aurelius, Meditations, Book 4'''
    # print(generate_response(q))
    # q = fetch_quote()
    app.run(debug=True)