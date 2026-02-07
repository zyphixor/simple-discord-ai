#!/bin/python

# Following PEP 8, imports should be grouped in the following order:
# 1. Standard library imports
import asyncio
from datetime import datetime, timezone
import tomllib
import urllib.parse

# 2. Third-party imports
import discord
import pymongo
from ollama import Client

class DiscordLLM(discord.Client):
    def __init__(self, config_path="config.toml"):
        # Load configuration from a TOML file, so its easier to configure and
        # the code doesn't contain sensitive information like tokens and API keys
        with open(config_path, "rb") as f:
            self.config = tomllib.load(f)
        
        intents = discord.Intents.default()
        intents.message_content = True  # Enable message content intent
        super().__init__(intents=intents)

        
        self.chat_history, self.msgLimit = self._setup_mongodb()
        
        # I think it'll be easier and cleaner to basically
        # make this a custom client, so people can make remote LLM servers
        # According to ollama's documentation, we can make a client variable
        self.ollama_client = Client(host=self.config["ollama"]["host"])

    # MongoDB Setup. I hope I don't mess this up.
    def _setup_mongodb(self):
        cfg = self.config["mongodb"]
        host, db_name = cfg["host"], cfg["name"]
        # Prepare credentials if provided in the config file
        user, password = cfg.get("user", ""), cfg.get("password", "")

        if user and password:
            # Use authentication
            # Escaping user/pass in case they contain special characters
            u,p = urllib.parse.quote_plus(user), urllib.parse.quote_plus(password)
            uri = f"mongodb://{u}:{p}@{host}"
        else:
            # No authentication
            uri = f"mongodb://{host}"

        # Connect to DB
        client = pymongo.MongoClient(uri)
        db = client[db_name]        
        print(f"Connected to database '{db_name}' at '{host}'")
        return db["chatHistory"], cfg.get("msgLimit", 50)
    
    # Function to generate AI responses using Ollama
    def _llm_response(self, prompt):
        # this is probably the worst code I've ever written, but it works, so I'm not gonna change it.
        # Fetch the last 50 messages from the chat history for the given user and channel, sorted by newest to oldest
        memory_docs = list(self.chat_history.find().sort("timestamp", -1).limit(self.msgLimit))
        memory_docs.reverse()  # Reverse the list to have the oldest messages first for the AI to read in the correct order

        memory_messages = [{"role": doc["role"], "content": doc["content"]} for doc in memory_docs]
        
        messages = [
            {"role": "system", "content": self.config["ollama"]["sysPrompt"]},
            *memory_messages,  # Unpack the memory messages into the main messages list
            {"role": "user", "content": prompt}
        ]

    # Add predicting response so the AI actually works
        response = self.ollama_client.chat(model=self.config["ollama"]["model"], messages=messages)
        return response.message.content

    async def on_ready(self):
        print(f'Bot is successfully up as {self.user}')

    async def on_message(self, message):
        if message.author == self.user:
            return  # Ignore messages from the bot itself
        
        # Ignore messages from other bots to prevent potential infinite loops or unwanted interactions
        if message.author.bot:
            return

        # Grab user messages and display name so bot knows who said what, and can respond accordingly
        prompt = f"The user named {message.author.display_name} said: {message.content}"
        
        try:
            async with message.channel.typing():  # Show typing indicator while processing the response
                # Run slow llm call in a separate thread to avoid blocking the event loop
                response = await asyncio.to_thread(self._llm_response, prompt)
                await message.channel.send(response)  # Send the response back to Discord

                self.chat_history.insert_many([
                    {"role": "user", "content": prompt, "timestamp": datetime.now(timezone.utc)},
                    {"role": "assistant", "content": response, "timestamp": datetime.now(timezone.utc)}
                ])
                
                # Trim the DB to keep only the last 50 messages
                last_kept_docs = list(self.chat_history.find().sort("timestamp", -1).limit(self.msgLimit))
                if last_kept_docs:
                    oldest_kept_timestamp = last_kept_docs[-1]["timestamp"]
                    # Delete anything older than the oldest message we want to keep
                    self.chat_history.delete_many({"timestamp": {"$lt": oldest_kept_timestamp}})

        except Exception as e:
            await message.channel.send(f"Error generating AI response: {e}")    

# run bot
if __name__ == "__main__":
    bot = DiscordLLM()
    bot.run(bot.config["discord"]["token"])