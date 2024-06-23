import os
import logging
from flask import Flask, jsonify
import requests
from openai import OpenAI
from k import oakv1, quote_url

from flask import request


# Set up logging
logging.basicConfig(filename='stoic_app.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

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
        # Extract quote from request body
        data = request.get_json()
        quote = data.get('quote')
        if not quote:
            return jsonify({"error": "No quote provided"}), 400

        # Generate explanation for the provided quote
        explanation = generate_response(quote)

        # Construct and return the response
        response = {
            "quote": quote,
            "explanation": explanation
        }
        return jsonify(response), 200
    except Exception as e:
        error_response = {"error": str(e)}
        logging.error(f"Error in process_quote: {error_response}")
        return jsonify(error_response), 500


# dummy test endpoint
@app.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "Hello, World!"}), 200

if __name__ == '__main__':
    # app.run(debug=True)
    # q = '''"A man should always have these two rules in readiness; the one, to do only whatever the reason of the ruling and legislating faculty may suggest for the use of men; the other, to change thy opinion, if there is anyone at hand who sets thee right and moves thee from any opinion." --Marcus Aurelius, Meditations, Book 4'''
    # print(generate_response(q))
    # q = fetch_quote()
    app.run(debug=True)