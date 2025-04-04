import os
import requests
from flask import Flask, request, jsonify
from database import init_db, save_user
from bs4 import BeautifulSoup

app = Flask(__name__, static_folder='public', static_url_path='')

# Fetch website content at startup
def fetch_website_content(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, timeout=10, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract text from paragraphs and headings
        content = ' '.join([p.get_text() for p in soup.find_all(['p', 'h1', 'h2', 'h3'])])
        return content[:1000]  # Limit to 1000 characters
    except requests.RequestException as e:
        print(f"Failed to fetch website content: {e}")
        return "DigiDara Technologies offers courses in Python, Data Analysis, Data Science, GEN AI, Agentic AI, AI in Cloud Computing, AI digital Marketing and Agentic setups. We specialize in innovative tech solutions."

WEBSITE_CONTENT = fetch_website_content("https://digidaratechnologies.com")

# Ollama Function with phi4-mini
def run_ollama(prompt):
    try:
        # Fallback for weather-related queries
        if "weather" in prompt.lower():
            return "I’m sorry, I don’t have access to real-time weather data. Please check a weather app or website for the latest updates!"

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "phi4-mini",  # Using phi4-mini (likely phi-3-mini)
                "prompt": f"Act as a friendly, knowledgeable chatbot for DigiDara Technologies. Use this context: {WEBSITE_CONTENT}. Respond to: {prompt}",
                "stream": False
            }
        )
        if response.status_code == 200:
            return response.json()["response"].strip()
        else:
            return f"Error: Ollama returned status {response.status_code}"
    except requests.exceptions.ConnectionError:
        return "Error: Ollama server is not running. Please start it with 'ollama serve'."

# Initialize SQLite database
init_db()

# State management for conversation flow
user_state = {}

@app.route('/')
def serve_frontend():
    return app.send_static_file('index.html')

@app.route('/favicon.ico')
def favicon():
    return '', 204  # No content response

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_id = request.remote_addr  # Use IP as a simple user ID
    prompt = data.get('prompt', '').strip()  # Keep original case for user input
    state = user_state.get(user_id, {'step': 'welcome'})

    # Default response and quick replies
    response = ""
    quick_replies = None

    # Welcome step: Display welcome message
    if state['step'] == 'welcome':
        response = "Hi! Welcome to DigiDara Technologies. I’m here to assist you. Please type anything to get started."
        state['step'] = 'awaiting_input'

    # Awaiting input: Start collecting information after user types anything
    elif state['step'] == 'awaiting_input':
        response = "Great! May I have your name, please?"
        state['step'] = 'collect_name'

    # Collect user information step-by-step
    elif state['step'] == 'collect_name':
        state['name'] = prompt
        response = f"Thanks, {state['name']}! What’s your email?"
        state['step'] = 'collect_email'

    elif state['step'] == 'collect_email':
        state['email'] = prompt
        response = f"Almost there, {state['name']}! What’s your phone number?"
        state['step'] = 'collect_phone'

    elif state['step'] == 'collect_phone':
        state['phone'] = prompt
        courses = [
            "Python",
            "Data Analysis",
            "Data Science",
            "GEN AI",
            "Agentic AI",
            "AI in Cloud Computing",
            "AI digital Marketing",
            "Agentic setups"
        ]
        course_list = "\n\t".join(f"{i+1}. {course}" for i, course in enumerate(courses))
        response = f'''Thanks, {state['name']}! Which course are you interested in?
        \n\n We offer:\n1. Python\n\t2. Data Analysis\n\t3. Data Science\n\t4. GEN AI\n\t5. Agentic AI\n\t6. AI in Cloud Computing\n\t7. AI digital Marketing\n\t8. Agentic setups\nPlease type the course name or number.'''
        state['step'] = 'collect_course'

    elif state['step'] == 'collect_course':
        state['course'] = prompt
        response = f"Great choice, {state['name']}! What course duration are you looking for?\n1 month,\n\t2 months,\n\t3 months,\n\t6 months"
        state['step'] = 'collect_duration'

    elif state['step'] == 'collect_duration':
        state['course_duration'] = prompt
        # Save user information to the database
        save_user(state['name'], state['email'], state['phone'], state['course'], state['course_duration'], message='')
        response = f"Thanks, {state['name']}! Your information has been saved. Now I can assist you with any topic you'd like to discuss. If you have an enquiry, you can use the 'Enquire Now' button."
        state['step'] = 'free_chat'
        quick_replies = ['Enquire Now']  # Show Enquire Now button

    # Free chat mode: Respond to any topic
    elif state['step'] == 'free_chat':
        if prompt.lower() == 'enquire now':
            response = "Please type your enquiry message, and I’ll save it for you."
            state['step'] = 'collect_enquiry'
        else:
            response = run_ollama(prompt)
            quick_replies = ['Enquire Now']  # Always show Enquire Now button

    # Collect enquiry message
    elif state['step'] == 'collect_enquiry':
        # Save the enquiry message to the database
        save_user(state['name'], state['email'], state['phone'], state['course'], state['course_duration'], message=prompt)
        response = "Thank you! Your enquiry has been saved. I’ll get back to you soon. What else would you like to talk about?"
        state['step'] = 'free_chat'
        quick_replies = ['Enquire Now']  # Show Enquire Now button again

    user_state[user_id] = state
    return jsonify({'response': response, 'quickReplies': quick_replies})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)