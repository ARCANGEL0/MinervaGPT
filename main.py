import telebot
import requests
import json
from telebot import types


# Token API do bot
bot = telebot.TeleBot(token='BOT TOKEN')


# chave API da OpenAI
API_KEY = 'OPEN AI API'
# modelo da IA
MODEL = 'text-davinci-003'




def MinervaText(prompt):
    #    requisicao para openAI
    response = requests.post(
        'https://api.openai.com/v1/completions',
        headers={'Authorization': f'Bearer {API_KEY}'},
        json={'model': MODEL, 'prompt': prompt, 'temperature': 0.8, 'max_tokens': 300}
    )

    result = response.json()

    return result['choices'][0]['text']
   


def MinervaImage(prompt):
    # requisicao para pegar imagem
    resp = requests.post(
        'https://api.openai.com/v1/images/generations',
        headers={'Authorization': f'Bearer {API_KEY}'},
        json={'prompt': prompt,'n' : 1, 'size': '1024x1024'}
    )
    response_text = json.loads(resp.text)
    print(response_text)
    return response_text['data'][0]['url']
    
    
@bot.message_handler(content_types=['text'])

def handler_text(message):
           if "Desenhe" in message.text:
               
               prompt = message.text.replace("Desenhe", "")
               res = MinervaImage(prompt)
              
               bot.send_photo(message.chat.id,res)
           elif "desenhe" in message.text:
               prompt = message.text.replace("desenhe", "")
               res = MinervaImage(prompt)
               bot.send_photo(message.chat.id,res)
           elif "/img" in message.text:
               prompt = message.text.replace("/img", "")
               res = MinervaImage(prompt)
               bot.send_photo(message.chat.id,res)
           elif "/start" in message.text:
              
              markup = types.InlineKeyboardMarkup()
              markup.add(types.InlineKeyboardButton("Website", url="https://arcangello.com")),
              bot.send_message(chat_id=message.from_user.id, text=f'Olá, bem vindo {message.from_user.first_name}.Sou Minerva, sua Inteligência artificial modelada com a OpenAI, de prontidão para lhe ajudar e assistir no seu cotidiano. Me pergunte qualquer coisa que vou lhe responder, ou me peça para desenhar alguma coisa ou use o comando /img que irei gerar uma ilustração para você. Bot desenvolvido por Henry Arcangelo. Visite meu website! ^^ ', reply_to_message_id=message.message_id,reply_markup=markup)
              
              
                  
           else:
                        print(message.text)
                        res = MinervaText(f"{message.text}")
                        bot.reply_to(message,res)
    
bot.polling()

