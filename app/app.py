from flask import Flask, jsonify, request
import requests
from claude_api import Client
from k import ck

app = Flask(__name__)

# Initialize the Claude API client with your Claude API cookie
# Replace 'your_claude_api_cookie_here' with your actual Claude API cookie
claude_client = Client(cookie=ck)

@app.route('/get_stoic_quote', methods=['GET'])
def get_stoic_quote():
    # Fetch the quote
    quote_response = requests.get('https://stoic-quote-api.onrender.com/aurelius')
    quote = quote_response.text  # Assuming the API returns JSON with a "quote" field

    # Format the prompt
    prompt = f"""Play the role of Marcus Aurelius and explain the quote. The quote is within <quote></quote> tags below
<quote>
{quote}
</quote>"""

    # Create a new chat to get a conversation ID
    new_chat = claude_client.create_new_chat()
    conversation_id = new_chat['uuid']

    # Use the Claude API client to send the message
    claude_response = claude_client.send_message(prompt, conversation_id)

    # Return the Claude API response
    return jsonify({"response": claude_response})

if __name__ == '__main__':
    app.run(debug=True)