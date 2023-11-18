# -----------------------
# you to install flask
#   pip install Flask
# -----------------------

# imports
from flask import Flask, render_template, request, redirect,jsonify
import openai
import sqlite3
import json
from openai import OpenAI
from pathlib import Path


# connect to db and get cursor
#connection = sqlite3.connect("data/prompts.db", check_same_thread=False)
#cursor = connection.cursor()

# read key from json file
# check if file exists locally
data = {}
try:
    with open('openai_key.json') as f:
        print(f'file exists locally')
        data = json.load(f) 
except IOError:
    print('file does not exist locally')

    
client = OpenAI(api_key=data['OPENAI_API_KEY'])
assistant = None
def create_assistant(client):
    assistant = client.beta.assistants.create(
    name="Math Tutor",
    instructions="You are a personal math tutor. Write and run code to answer math questions.",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4-1106-preview"
    )
    return assistant


def create_file(client):
# Use the client.files.create method
# check that file exists locally
    try:
        with open('test.txt') as f:
            print(f'file exists locally')
    except IOError:
        print('file does not exist locally')
# check if filename exists on openai server

        file = client.files.create(file = open("test.txt","rb"), purpose = "assistants")
        file_id = file.id
    return file_id


# web application
app = Flask(__name__)
# add data to database
# this is where we read from the database
@app.route('/')
def index():
    #list = cursor.execute("SELECT * FROM prompts").fetchall()
    #assistant = create_assistant(client)

    return render_template('actions.html', assistant_id = 'asst_pZB7ll8Nm6DJ7JLCRstb9XIf')

@app.route('/create_thread',methods=['POST'])
def create_thread():
    print("Button Clicked Create Thread")
    return render_template('/actions.html',thread_id = 'thrd_2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2Q2')

@app.route('/create_message',methods=['POST'])
def create_message():
    data = request.form['message']
    print(f'Button Clicked Create Message{data}')
    return render_template('/actions.html',message_id = data)


# this is where we read from the database
@app.route('/createPrompt',methods=['GET'])
def create():
    msg = {"gptResponse":"Waiting for input"}
    return render_template('create.html', msg = msg)

@app.route('/sendGPT', methods=['POST'])
def ask_openai():
    # read api key from file openai_key.json
    with open('openai_key.json') as f:
        data = json.load(f)
    client = OpenAI(api_key = data['OPENAI_API_KEY'])

    # get parameters from request
    style = 'formal'
    #tone = request.args.get('tone')
    tone = 'friendly'
    language = 'English'
    print(f'request form {request.form }')
    topic = request.form['message']
    
    prompt = "I am a " + style + " writer. I write in " + language + " and my tone is " + tone + ". I want to write a paragraph about " + topic + "."
    completion = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {
            "role": "user",
            "content": prompt,
        },
        ],
    )
    print(completion.choices[0].message.content)
    answer = completion.choices[0].message.content
    msg = {"gptResponse":answer}
    #write_to_db(topic, style, tone, language, prompt, answer)
    return render_template('create.html', msg = msg)



    
if __name__ == '__main__':
    app.run(debug=True, port=3000)