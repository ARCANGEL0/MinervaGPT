# MinervaGPT
Simple project with python of a bot for Telegram using AI from OpenAI, which queries CEP, generates images based on text and answers any question asked by the user.

# Usage
Clone the repo
```bash
git clone https://github.com/ARCANGEL0/MinervaGPT
cd MinervaGPT
```
Install project dependencies with pip
```bash
pip install -r requirements.txt
```
Change the global variables in main.py and insert your Telegram bot tokens and OpenAI API key
```python
...

# Token API ofn your bot
bot = telebot.TeleBot(token="BOT TOKEN")


# API key OpenAI
API_KEY = 'OPENAI API TOKEN'
...
```
Then, run the main.py file and test your bot!
```bash
python main.py
```
