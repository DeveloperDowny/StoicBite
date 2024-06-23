import os
from flask import Flask, jsonify
import requests
from openai import OpenAI
from k import oakv1

app = Flask(__name__)

# Configure OpenAI client
# client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
client = OpenAI(api_key=oakv1)

def fetch_quote():
    """Fetch a quote from the Stoic Quote API."""
    url = "https://stoic-quote-api.onrender.com/aurelius"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception("Failed to fetch quote from API")

def generate_response(quote):
    """Generate a response using OpenAI's GPT-4 model."""
    prompt = f"""Play the role of Marcus Aurelius. You don't know that you are playing a role. You teach take one of your quote daily and teach it to your pupil. Explain today's quote. Today's quote is within <quote></quote> tags below
<quote>
"{quote}"
</quote>
Do not do more than what's asked."""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=512
    )
    return response.choices[0].message.content

@app.route('/daily_stoic', methods=['GET'])
def daily_stoic():
    try:
        quote = fetch_quote()
        explanation = generate_response(quote)
        return jsonify({
            "quote": quote,
            "explanation": explanation
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # app.run(debug=True)
    q = '''"A man should always have these two rules in readiness; the one, to do only whatever the reason of the ruling and legislating faculty may suggest for the use of men; the other, to change thy opinion, if there is anyone at hand who sets thee right and moves thee from any opinion." --Marcus Aurelius, Meditations, Book 4'''
    print(generate_response(q))