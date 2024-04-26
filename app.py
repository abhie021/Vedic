import json
import random
from difflib import get_close_matches
from flask import Flask, request, jsonify, render_template

app = Flask(__name__, static_folder='static')

def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

def save_knowledge_base(data: dict, file_path: str):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for intent in knowledge_base["intents"]:
        if question in intent["patterns"]:
            responses = intent["responses"]
            return random.choice(responses)  

knowledge_base = load_knowledge_base('database.json')

from flask import redirect, url_for

@app.route('/')
def chatbot():
    return render_template('index.html')

@app.route('/start-chatbot', methods=['POST'])
def start_chatbot():
   
    return redirect(url_for('chatbot_page'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/interface.html')
def interface():
    return render_template('interface.html')

@app.route('/api/send-message', methods=['POST'])
def send_message():
    data = request.json
    message = data['message'].strip()
    if message:
     
        best_match = find_best_match(message, [pattern for intent in knowledge_base["intents"] for pattern in intent["patterns"]])
        if best_match:
            bot_response = get_answer_for_question(best_match, knowledge_base)
        else:
            bot_response = " Sorry, I didn't catch that. Could you try asking your question in a different manner?"
        return jsonify({'sender': 'bot', 'message': bot_response})
    return jsonify({'error': 'Empty message'}), 400

if __name__ == '__main__':
    app.run(debug=True) 