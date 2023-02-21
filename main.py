
import telebot
import requests
import json
from telebot import types


# Token API do bot
bot = telebot.TeleBot(token="BOT TOKEN")


# chave API da OpenAI
API_KEY = 'OPENAI API TOKEN'
# modelo da IA
MODEL = 'text-davinci-003'

def CEP(prompt):
    try:
         cep = int(prompt)
         request = requests.get("https://viacep.com.br/ws/{}/json".format(str(cep)))
         if request.status_code == 200:
             dict = json.loads(request.content.decode('utf-8'))
             print(dict)
             return  """
             🔎 Dados 🔎
             CEP: {},
             Logradouro {}, 
             Complemento: {},
             Bairro: {}, 
             Localidade: {},
             UF: {}, 
             IBGE: {}, 
             GIA: {}, 
             DDD: ( {} ),
             SIAFI: {}
             """.format(dict['cep'],dict['logradouro'],'🚫' if dict['complemento'] == '' else dict['complemento'] ,dict['bairro'], dict['localidade'], dict['uf'], dict['ibge']    ,   dict['gia'],   dict['ddd'] ,   dict['siafi']),     
             
         else:
             return " 🚫 CEP Informado está incorreto"
    except:
        return " 🚫 CEP Informado está inválido"
def getCEP(prompt):
    try:
         cep = int(prompt.text)
         request = requests.get("https://viacep.com.br/ws/{}/json".format(str(cep)))
         if request.status_code ==  200:
             dict = json.loads(request.content.decode('utf-8'))
             print(dict)
             markup = types.InlineKeyboardMarkup()
             markup.add(types.InlineKeyboardButton("⬅️ Voltar",callback_data="/voltar"))
             msg = """
          🔎 Dados 🔎
             CEP: {},
             Logradouro {}, 
             Complemento: {},
             Bairro: {}, 
             Localidade: {},
             UF: {}, 
             IBGE: {}, 
             GIA: {}, 
             DDD: ( {} ),
             SIAFI: {}
             """         
             bot.send_message(chat_id=prompt.from_user.id, text=msg.format(dict['cep'],dict['logradouro'],'🚫' if dict['complemento'] == '' else dict['complemento'] ,dict['bairro'], dict['localidade'], dict['uf'], dict['ibge']    ,   dict['gia'],   dict['ddd'] ,   dict['siafi']), reply_markup=markup)
             
             
         else:
             print('error')
             print(request.status_code)
             markup = types.InlineKeyboardMarkup()
             markup.add(types.InlineKeyboardButton("⬅️ Voltar",callback_data="/voltar"))
             bot.send_message(chat_id=prompt.from_user.id, text=' 🚫 CEP Informado não encontrado', reply_markup=markup)
         
         
    except Exception as e:
          print(e)
          markup = types.InlineKeyboardMarkup()
          markup.add(types.InlineKeyboardButton("⬅️ Voltar",callback_data="/voltar"))
          bot.send_message(chat_id=prompt.from_user.id, text=' 🚫 CEP Informado está inválido', reply_markup=markup)
               
def getImg(prompt):      
         res = MinervaImage(prompt.text)
         bot.send_photo(prompt.chat.id,res) 


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
           elif "/cep" in message.text:
               prompt = message.text.replace("/cep", "")
               print(prompt)
               res = CEP(prompt)
               bot.reply_to(message,res)  
               
           elif "/start" in message.text:
              
              markup = types.InlineKeyboardMarkup()
              markup.add(types.InlineKeyboardButton("Website", url="https://arcangello.com"),types.InlineKeyboardButton("Gerar imagem",callback_data="/imagem"),types.InlineKeyboardButton("Buscar CEP",callback_data="/cep"),row_width=1),
              bot.send_message(chat_id=message.from_user.id, text=f'Olá, bem vindo {message.from_user.first_name}.Sou Minerva, sua Inteligência artificial modelada com a OpenAI, de prontidão para lhe ajudar e assistir no seu cotidiano. Me pergunte qualquer coisa que vou lhe responder, ou me peça para desenhar alguma coisa ou use o comando /img que irei gerar uma ilustração para você. Bot desenvolvido por Henry Arcangelo. Visite meu website! ^^ ', reply_to_message_id=message.message_id,reply_markup=markup)
              
              
                  
           else:
                        print(message.text)
                        res = MinervaText(f"{message.text}")
                        bot.reply_to(message,res)
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    
       if call.data == "/imagem":
         bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        
         markup = types.InlineKeyboardMarkup()
         markup.add(types.InlineKeyboardButton("⬅️ Voltar",callback_data="/voltar"))
         bot.send_message(chat_id=call.from_user.id, text='🎨 Escreva o que você gostaria que eu desenhasse que vou gerar uma ilustração para você!', reply_markup=markup)
         print(call)
         bot.register_next_step_handler(call.message,getImg)
         
         
       if call.data == "/voltar":
           bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
           
           
           markup = types.InlineKeyboardMarkup()
           markup.add(types.InlineKeyboardButton("Website", url="https://arcangello.com"),types.InlineKeyboardButton("Gerar imagem",callback_data="/imagem"),types.InlineKeyboardButton("Buscar CEP",callback_data="/cep"),row_width=1),
           bot.send_message(chat_id=call.from_user.id, text=f'Olá, bem vindo {call.from_user.first_name}.Sou Minerva, sua Inteligência artificial modelada com a OpenAI, de prontidão para lhe ajudar e assistir no seu cotidiano. Me pergunte qualquer coisa que vou lhe responder, ou me peça para desenhar alguma coisa ou use o comando /img que irei gerar uma ilustração para você. Bot desenvolvido por Henry Arcangelo. Visite meu website! ^^ ',reply_markup=markup)
           
           
       if call.data == "/cep":
            bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("⬅️ Voltar",callback_data="/voltar"))
            bot.send_message(chat_id=call.from_user.id, text="Digite um CEP para eu buscar para você", reply_markup=markup)
            bot.register_next_step_handler(call.message,getCEP)
            
            
bot.polling()

