# import everything
import requests
import json
import discord
import tomllib
import ollama
import os
import base64  # Added for Base64 encoding

# LOAD VARIABLES FROM config.toml
with open("config.toml", 'rb') as f:
    config_data = tomllib.load(f)

TOKEN = config_data['discord']['token']
API_URL = 'http://localhost:11434/api/chat'
HISTORY_FILE_PATH = "history.json"

def load_conversation_history():
    if os.path.exists(HISTORY_FILE_PATH):
        with open(HISTORY_FILE_PATH, 'r') as file:
            return json.load(file)
    return []

def save_conversation_history():
    with open(HISTORY_FILE_PATH, 'w') as file:
        json.dump(conversation_history, file)

conversation_history = load_conversation_history()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Modified to accept images
def generate_response(prompt, images=None):
    # Append user message with images
    user_message = {"role": "user", "content": prompt}
    if images:
        user_message["images"] = images
    
    conversation_history.append(user_message)
    save_conversation_history()

    data = {
        "model": config_data['ollama']['model'],
        "messages": conversation_history,
        "stream": False
    }

    response = requests.post(API_URL, json=data)
    try:
        response_data = response.json()
        assistant_message = response_data['message']['content']
        
        conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        return assistant_message
    except requests.exceptions.JSONDecodeError:
        return "Error: Invalid API response"

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user or message.author.bot:
        return
    
    prompt = f"{message.author.display_name} says: {message.content}"
    images = []
    
    # Process image attachments
    for attachment in message.attachments:
        if attachment.content_type.startswith('image/'):
            image_data = await attachment.read()
            base64_image = base64.b64encode(image_data).decode('utf-8')
            images.append(base64_image)
    
    try:
        async with message.channel.typing():
            response = generate_response(prompt, images)
            await message.channel.send(response)
    except discord.errors.Forbidden:
        print(f"Error: Bot can't send messages in {message.channel.name}")

client.run(TOKEN)