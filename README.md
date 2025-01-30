# simple-discord-ai
A self-hostable chatbot for Discord that utilizes ollama.

## Installation
1. [Install Ollama](https://ollama.com/download/)
2. `pip install discord.py ollama requests`
3. Open `run.py` and replace `TOKEN = ''` with `TOKEN = 'YOUR_BOT_TOKEN'`
4. Run `run.py`
- Note: if you want the bot to work without it being pinged/mentioned, use runNoMention.py (please note that it uses the old buggy memory system. it will stay like this for a bit until i have the time to fix it up)
- Note 2: if you dont want memories and just something simple, use runStable.py
## Usage
To use the bot, ping it via its username (e.g. @bot) or reply to it.

## Support

Discord coming soon

Any contributions to this would be greatly appreciated. 

## TODO
- Clean code up
- Squash some bugs
- have bot read display names
- (IDEALLY LAST) provide ability to save history to file for persistance
