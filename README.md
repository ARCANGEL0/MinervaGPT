# MinervaGPT
Projeto simples com python de um bot para telegram fazendo uso da IA da OpenAI, que consulta CEP, gera imagems com base em texto e responder qualquer pergunta feita prlo usuário.

# Uso 
Clone o repositorio 
```bash
git clone https://github.com/ARCANGEL0/MinervaGPT
cd MinervaGPT
```
instale as dependências do projeto com pip
```bash
pip install -r requirements.txt
```
Altere as variáveis globais e insira suaa tokens do bot do telegram e a chave API da OpenAI
```python
...

# Token API do bot
bot = telebot.TeleBot(token="BOT TOKEN")


# chave API da OpenAI
API_KEY = 'OPENAI API TOKEN'
...
```
Depois, rode o arquivo main.py e teste seu bot!
```bash
python main.py
```

# Demo
Uma demonstração do bot pode ser feita através do meu bot pessoal [aqui](https://t.me/MinervaGPTBOT)
