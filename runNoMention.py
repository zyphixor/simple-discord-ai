# import everything
import requests
import json
import discord
import tomllib
import ollama
import os # Don't panic!!! This is used to save the history file to the computer!

# LOAD VARIABLES FROM config.toml
with open("config.toml", 'rb') as f: # load config as f (f is short for file im just using slang, chat)
  config_data = tomllib.load(f)

# api info for ollama
TOKEN = config_data['discord']['token'] # Load token from config file
API_URL = 'http://localhost:11434/api/chat'



# Define the path for the conversation history file
HISTORY_FILE_PATH = "history.json"

# Load conversation history from a file if it exists
def load_conversation_history():
    if os.path.exists(HISTORY_FILE_PATH):
        with open(HISTORY_FILE_PATH, 'r') as file:
            return json.load(file)
    return []

# Save conversation history to a file
def save_conversation_history():
    with open(HISTORY_FILE_PATH, 'w') as file:
        json.dump(conversation_history, file)

# Store conversation history in a list
conversation_history = load_conversation_history()

# set what the bot is allowed to listen to
intents = discord.Intents.default()
intents.message_content = True  # Allow reading message content
client = discord.Client(intents=intents)

# Function to send a request to the Ollama API and get a response
def generate_response(prompt):
	# add user message to history
	conversation_history.append({
		"role": "user",
		"content": prompt
	})

	# Save the updated conversation history to the file
	save_conversation_history()

	data = {
		"model": config_data['ollama']['model'],  # load model name from config
		"messages": conversation_history, # Send the entire conversation history
		"stream": False  # Set stream to False or the program will start bitching
	}

	response = requests.post(API_URL, json=data)
	print("Raw Response Content:", response.text)  # This will print out the raw response for debug purposes.

	# try and except used for error catching
	try:
		# Attempt to parse the response as JSON
		response_data = response.json()
		assistant_message = response_data['message']['content']

		# Add the assistant's reply to the conversation history
		conversation_history.append({
			"role": "assistant",
			"content": assistant_message
		})

		return assistant_message
	except requests.exceptions.JSONDecodeError:
		return "Error: Invalid API response"

# When the bot is ready
@client.event
async def on_ready():
	print(f'Logged in as {client.user}')

# When the bot detects a new message
@client.event
async def on_message(message):
	# Don't let the bot reply to itself
	if message.author == client.user:
		return
	
	# Process every message, whether the bot is mentioned or not
	prompt = message.content  # Get the message content as the prompt
	prompt = f"{message.author.display_name} says: " + prompt
	# try and except are used to check if the bot has permission to send in the channel.
	try:
		#prompt = message.content.replace(f"<@!{client.user.id}>", "").strip()  # Remove the mention part
		async with message.channel.typing():
			if prompt:
				response = generate_response(prompt)
				await message.channel.send(response)
			else: # if prompt is empty
				response = generate_response(prompt)
				await message.channel.send(response)
	except discord.errors.Forbidden:
		# Handle Forbidden error for typing (bot can't show typing)
		print(f"Error: Bot does not have permission to type in {message.channel.name}")
		return

# Run the bot
client.run(TOKEN)
