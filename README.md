# DiscordLLM (Experimental)

> **⚠️ Warning:** This branch is experimental. It may be insecure, unstable, or undergo breaking changes. Use at your own risk.

DiscordLLM is a self-hostable Discord chatbot that brings the power of local LLMs to your server using **Ollama** and **MongoDB**.

---

## Features

* **Local Inference:** Powered by Ollama, no expensive API keys required.
* **Memory:** Utilizes MongoDB to store conversation history for contextual responses.
* **Extensible:** Built with Python and designed for easy setup and tinkering.

## Prerequisites

Before starting, ensure you have the following installed and running:

* [Ollama](https://ollama.ai/) (Local LLM runner)
* [MongoDB](https://www.mongodb.com/) (For chat history)
* Python 3.11+

## Installation

### 1. Clone & Install Dependencies

```bash
git clone -b experimental https://github.com/zyphixor/simple-discord-ai.git
cd simple-discord-ai
pip install -r requirements.txt

```

### 2. Configuration

Copy the example config (if applicable) or edit `config.toml` directly with your Discord Token and MongoDB credentials:

```toml
# MongoDB Connection Settings
[mongodb]
host = "localhost:27017"
name = "DiscordLLM" 
user = ""      # Optional: Recommended for production
password = ""  # Optional: Recommended for production
msgLimit = 50  # Number of past messages the LLM remembers (Hardware dependent)

# Local LLM Settings (via Ollama)
[ollama]
host = "http://localhost:11434"
model = "llama3.2"
sysPrompt = """

You are a Discord chatbot. 
Do not explain your reasoning, thoughts or internal analysis. Only output the final response to the user.

"""
# Discord Bot Credentials
[discord]
# KEEP THIS PRIVATE. Do not share this with anyone EVER!
token = "YOUR_DISCORD_BOT_TOKEN_HERE"

```

### 3. Run the Bot

```bash
python3 run.py

```

---

## Usage

1. Invite the bot to your server using the Discord Developer Portal.
2. Ensure the bot has **Read/Write** and **Message Content Intent** permissions.
3. Start chatting! The bot responds to messages in any channel it can access.

---

## Roadmap (TODO)

* [ ] **Operation Modes:** Add "mention-only," "specific-channel," and "fast" modes.
* [ ] **Security:** Implement hashed passwords and encrypted token support in `config.toml`.
* [ ] **Docker Support:** Simplify deployment with a `docker-compose.yml` (Unconfirmed, still thinking about it).

## Support

This is a **personal project**.

* **No official support** is provided.
* I may help in my free time, but please do not expect immediate responses.
* Pull requests are welcome!