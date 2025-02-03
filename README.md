# simple-discord-ai
A self-hostable chatbot for Discord that utilizes ollama.

## Installation
1. [Install Ollama](https://ollama.com/download/)
2. Optional: Create virtual Environment `python -m venv venv` / activate Environment: `.\venv\Scripts\Activate`
3. `pip install -r requirements.txt`
4. Open `config.toml` and enter your model and bot token
5. Run `run.py`
- Note: if you want the bot to work without it being pinged/mentioned, use runNoMention.py
- Note 2: if you dont want memories and just something simple, use runStable.py
## Usage
To use the bot, ping it via its username (e.g. @bot) or reply to it.

## Support

Discord coming soon

Any contributions to this would be greatly appreciated. 

## TODO
- Clean code up
- Squash some bugs
- add history "cleaning" (cleans past lines to save on storage, ram, and vram)
