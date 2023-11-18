# Prompt tool for GPT
This leverages Three Tiers: client, server, and storage
Create Database - Run createDB.py using python3 createDB.py
This creates prompts.db
Now run python3 index.py and hit the routes
the route localhost:3000/createPrompt allows you to create a prompt 
and send it to GPT model davinci
The response is all prompt details are saved in the database
and displayed in the web page.

