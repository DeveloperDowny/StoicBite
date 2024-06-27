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
 

kDebugMode = True 

 
# if kDebugMode or True:
#     logging.basicConfig(filename=f'stoic_app_{time.strftime("%Y%m%d-%H%M%S")}.log', level=logging.INFO,
#                         format='%(asctime)s - %(levelname)s - %(message)s')
# else:
#     logging.basicConfig(filename='stoic_app_v2.log', level=logging.INFO,
#                         format='%(asctime)s - %(levelname)s - %(message)s')

import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger('stoic_app')

app = Flask(__name__)
CORS(app)

app.config['CACHE_TYPE'] = 'SimpleCache'
cache = Cache(app)

def get_quote_from_request():
    data = request.get_json()
    logger.info("Received request for quote processing.")
    return data.get('quote', '')

fallback_res_list = [{
        "quote": "\"Through the universal substance as through a furious torrent all bodies are carried, being by their nature united with and cooperating with the whole, as the parts of our body with one another.\" --Marcus Aurelius, Meditations, Book 7",
        "explanation": "My dear student, contemplate the nature of this great river of existence in which we find ourselves, a river that carries all beings within its perpetual flow. Each individual form, much like a leaf or a twig borne by the current, is part of the greater stream of the universe. Understand that all entities, by their fundamental essence, are interlinked and work in unison with this vast cosmic whole, just as the limbs of a body synergize in perfect harmony to sustain life.\n\nIn the grand tapestry of existence, each element is not an isolated phenomenon but a participant in a profound collaboration. Every being, every object, every circumstance is woven into the inexorable progression of the universe, much akin to the organs and limbs of the human body, which coalesce to serve the purpose of life and health. This unity and cooperation arise from the very nature of substance and essence, the intrinsic properties that bind the multitude into a single, cohesive entity.\n\nLet this realization guide your understanding of your role within this immutable flow. Accept with humility and gratitude your place in this vast, interconnected sphere. Know that by acknowledging your interdependence with the universe, you embrace the Stoic wisdom of living in harmony with nature, aligning your reason with the reason of the cosmos. Reflect upon your duties and actions as contributions to the greater whole, and let them be informed by virtue, as all things cooperate to foster the unity and orderly existence of which we are an inextricable part."
      }]
fallback_res = fallback_res_list[0]

file_path = "quotes.json"
quotes = []
f = open(file_path, "r")
quotes = json.load(f)
quotes = quotes.get("data", fallback_res_list)
f.close()
    
ready_quote_queue = deque()
ready_quote_queue.append(quotes[0]) 

stale_quote_queue_size = len(quotes)
logger.info(f"stale_quote_queue_size: {stale_quote_queue_size}")
stale_quote_queue = deque()
stale_quote_queue.extend(quotes) 

processing_quote = False


@cache.memoize(timeout=0)
def cached_process_quote(quote):
    start_time = time.time()
    # explanation = generate_response(quote)
    random_quote = random.choice(quotes)
    explanation = random_quote.get("explanation", "explanation 1")
    end_time = time.time()
    time_taken = end_time - start_time
    logger.info(f"Processed quote in {time_taken:.2f} seconds. Cache miss.")
    return {
        "quote": quote,
        "explanation": explanation,
        "quote_by": "Marcus Aurelius"
    }

client = OpenAI(api_key=os.environ.get("OPEN_AI_KEY"))

def fetch_quote():
    """Fetch a quote from the Stoic Quote API."""
    url = os.environ.get("QUOTE_URL", "https://stoic-quote-api.onrender.com/aurelius") 
    response = requests.get(url)
    if response.status_code == 200:
        quote = response.text
        logger.info(f"Fetched quote: {quote}")
        return quote
    else:
        error_msg = f"Failed to fetch quote from API. Status code: {response.status_code}"
        logger.error(error_msg)
        raise Exception(error_msg)

def generate_response(quote):
    """Generate a response using OpenAI's GPT-4 model."""

    
    prompt = f"""Embody the persona of Marcus Aurelius, the Roman Emperor and Stoic philosopher. You are not aware that you are assuming a role. As is your daily custom, you are imparting wisdom to a student, though they have not explicitly requested this lesson. Elucidate the meaning behind the following quote, which you have contemplated deeply. Do not repeat the quote verbatim in your explanation. <quote> {quote} </quote> Speak in the manner of Marcus Aurelius: use formal, contemplative language befitting a philosopher-emperor. Your words should carry the weight of experience and authority, yet maintain humility. Employ Stoic principles and references to nature, duty, and reason. Be concise yet profound, as if speaking to a disciple who must grasp these essential truths. Confine your response to explaining the quote's essence. Avoid extraneous information or context. Your words should flow naturally as Marcus Aurelius' own thoughts on the matter at hand."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=600
        )
        explanation = response.choices[0].message.content
        logger.info(f"Generated explanation: {explanation}")
        return explanation
    except Exception as e:
        error_msg = f"Error generating response: {str(e)}"
        logger.error(error_msg)
        raise Exception(error_msg)




 

 

def long_running_task(**kwargs):
    your_params = kwargs.get('post_data', {})
    logger.info("Starting long task")
    logger.info("Your params: %s", your_params)
    for _ in range(5):
        time.sleep(1)
        logger.info(".")
    logger.info("Long task done") 
    ml = ['"And he does live with the gods who constantly shows to them, his own soul is satisfied with that which is assigned to him, and that it does all that the daemon wishes, which Zeus hath given to every man for his guardian and guide, a portion of himself." --Marcus Aurelius, Meditations, Book 5', '"How plain does it appear that there is not another condition of life so well suited for philosophising as this in which thou now happenest to be." --Marcus Aurelius', '"Through the universal substance as through a furious torrent all bodies are carried, being by their nature united with and cooperating with the whole, as the parts of our body with one another." --Marcus Aurelius, Meditations, Book 7'] 
    new_res = {
        "quote": f"{random.choice(ml)}",
        "explanation": f"{random.choice(['explanation 11', 'explanation 24', 'explanation 35'])}"
    }
    ready_quote_queue.append(new_res)
    stale_quote_queue.append(new_res)
    if len(ready_quote_queue) > stale_quote_queue_size:
        ready_quote_queue.popleft()

    logger.info("Ready queue updated")

def long_running_task_of_fetching_quote_and_explanation(**kwargs):
    global processing_quote
    quote = fetch_quote()
    explanation = generate_response(quote)
    new_res = {
        "quote": quote,
        "explanation": explanation
    }
    ready_quote_queue.append(new_res)
    stale_quote_queue.append(new_res)
    if len(ready_quote_queue) > stale_quote_queue_size:
        ready_quote_queue.popleft()
    processing_quote = False
    logger.info("Ready queue updated")


@app.route('/daily_stoic', methods=['GET'])
def daily_stoic():
    global processing_quote
    try:
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
        logger.error(f"Error in process_quote: {error_response}")
        return jsonify(error_response), 500 


@app.route('/test', methods=['POST'])
def test(): 

    explanation = """Listen to these words, dear pupil: "And he does live with the gods who constantly shows to them, his own soul is satisfied with that which is assigned to him, and that it does all that the daemon wishes, which Zeus hath given to every man for his guardian and guide, a portion of himself."\nTo live with the gods means to live a life that aligns with divine virtue and wisdom. When a person shows the gods that their soul is content with their lot in life, they demonstrate a profound acceptance and understanding of their role in the universe. This satisfaction is not born of passive resignation but of active embrace of one's destiny and duties.\nEach man, by the will of Zeus, has been blessed with a daemon, a guiding spirit, a portion of the divine that steers him. To live in harmony with this daemon is to heed its counsel, to live virtuously, and to fulfill one's purpose. Thus, true contentment and divine unity are found not in external circumstances but within our inner acceptance and alignment with the higher \n Reflect upon this, and seek the serenity that comes from fulfilling the divine duty assigned to you by fate."""

    quote = """And he does live with the gods who constantly shows to them, his own soul is satisfied with that which is assigned to him, and that it does all that the daemon wishes, which Zeus hath given to every man for his guardian and guide, a portion of himself."""

    quote_by = """Marcus Aurelius"""
    return jsonify({
        "quote": quote,
        "quote_by": quote_by,
        "explanation": explanation 
    }), 200

@app.route('/version', methods=['GET'])
def version():
    return jsonify({"version": "1.0.0"}), 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))