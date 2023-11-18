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
list = {"assistant":" ","message": "", "thread": ''}
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
# set the url for static
app.static_url_path = 'static/'
print(f'static url path {app.static_url_path}')
# add data to database
# this is where we read from the database
@app.route('/')
def index():
    #list = cursor.execute("SELECT * FROM prompts").fetchall()
    #assistant = create_assistant(client)
    list = {"assistant": 'asst_pZB7ll8Nm6DJ7JLCRstb9XIf', "message": '', "thread": 'thrd_2Q2QQ2'}
    return render_template('actions.html', list = list )

@app.route('/create_thread',methods=['POST'])
def create_thread():
    print("Button Clicked Create Thread")
    list = {"message": 'xxx', "thread": 'thrd_2Q2QQ2'}
    return render_template('/actions.html',list = list)

@app.route('/create_message',methods=['POST'])
def create_message():
    data = request.form['message']
    list = {"message": data, "thread": 'thrd_2Q2QQ2'}
    return render_template('/actions.html',list = list)    


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