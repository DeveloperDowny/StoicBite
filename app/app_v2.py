from flask import Flask, jsonify
import requests
from gpt4_openai import GPT4OpenAI
from k import llm_k

app = Flask(__name__)

# Replace 'my_session_token' with the actual session token from chat.openai.com
gpt4_client = GPT4OpenAI(token=llm_k, headless=True, model='gpt-4')

# session_token = os.getenv('GPT4_SESSION_TOKEN', 'default_fallback_token') #ideally

@app.route('/get_stoic_quote', methods=['GET'])
def get_stoic_quote():
    # Fetch the quote
    quote_response = requests.get('https://stoic-quote-api.onrender.com/aurelius')
    # quote = quote_response.json()['quote']  # Adjusted to extract quote from JSON response
    quote = quote_response.text

    # Format the prompt
    prompt = f"Play the role of Marcus Aurelius and explain the quote: '{quote}'"

    # Use GPT-4 to process the prompt
    response = gpt4_client(prompt)

    # Return the response
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)