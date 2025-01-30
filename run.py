# TODO: make it remember conversations for a more "human" feel.
# maybe i could use SQLite or Redis for this..

# import everything
import discord
import ollama
import requests
import json

# api info for ollama
TOKEN = '' # dont share this with anyone
API_URL = 'http://localhost:11434/api/chat'

# Store conversation history in a list
conversation_history = []

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
    data = {
        "model": "llama2-uncensored",  # You can replace this with the desired model (e.g., llama3.2)
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

    # Check if the bot was mentioned
    if client.user.mentioned_in(message):
        prompt = message.content.replace(f"<@!{client.user.id}>", "").strip()  # Remove the mention part
        if prompt:
            response = generate_response(prompt)
            await message.channel.send(response)
        else:
            await message.channel.send("bing bop boom boom boom bop bam, the type of shit im on you wouldnt understand")

# Run the bot
client.run(TOKEN)