# import everything
import json
import requests
import discord
import ollama


# api info for ollama
TOKEN = ''  # dont share this with anyone
API_URL = 'http://localhost:11434/api/generate'

# set what the bot is allowed to listen to
intents = discord.Intents.default()
intents.message_content = True  # Allow reading message content
client = discord.Client(intents=intents)


# Variable used to store past 15 messages (There's probably a better way to do this, but oh well)
msg_hist = []

# Function to send a request to the Ollama API and get a response
def generate_response(prompt):
    # prevent the bot from attempting to mention itself by stripping its @ from
    # the prompt the user provides
    prompt = prompt.replace(f"<@!{client.user.id}>", "").strip()
    full_prompt = '\n'.join(msg_hist) + "\n" + prompt  # Add the new user prompt to the history

    data = {
        "model": "llama2-uncensored",  # Adjust this if you want to use a different model
        "prompt": full_prompt,
        "stream": False
    }

    response = requests.post(API_URL, json=data)
    if response.status_code == 200:
        response_data = response.json()
        return response_data.get("response", "Sorry, I couldn't generate a response.")
    else:
        return "There was an error with the API."

# When the bot is ready
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

# When the bot detects a new message
@client.event
async def on_message(message):
    # make msg_hist global so this piece of code can work
    global msg_hist
    # Don't let the bot reply to itself
    if message.author == client.user:
        return

    # Check if the bot was mentioned
    if client.user.mentioned_in(message):
        prompt = message.content.replace(f"<@!{client.user.id}>", "").replace(f"<@{client.user.id}>", "").strip()  # Remove the mention part so it doesnt attempt to ping itself.

        # using try and except to prevent it from generating stuff when it doesnt have permission to send in a channel
        try:
            # Attempt to show typing indicator, generate response and send response, if not; throw an error to the console
            async with message.channel.typing():
                # Generate response and send it
                response = generate_response(prompt).replace(f"{client.user.display_name}:", "").strip()
                await message.channel.send(response)

            # Basic memory system
            msg_hist.append(f"{message.author.display_name}: {message.content}")
            msg_hist.append(f"{client.user.display_name}: {response}")

            # Keep the history within the limit
            if len(msg_hist) > 15:
                msg_hist.pop(0)

        except discord.errors.Forbidden:
            # Catch Forbidden error and log it (do not send any further messages to the channel)
            print(f"Error: Bot does not have permission to send messages in {message.channel.name}")
            return


# Run the bot
client.run(TOKEN)
