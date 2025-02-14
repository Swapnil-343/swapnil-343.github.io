import os
from flask import Flask, render_template, request, jsonify
from google import genai

app = Flask(__name__)

# Read the API key from the text file
with open("api_key.txt", "r") as file:
    api_key = file.read().strip()

# Initialize the genai client
client = genai.Client(api_key=api_key)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_response():
    user_prompt = request.form['prompt']
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=user_prompt,
        )
        return jsonify({'response': response.text})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    # Change the port to dynamically use the environment variable on Heroku
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))