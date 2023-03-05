import tgcrypto
import os
from pyrogram import Client , filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from os.path import exists
from os import mkdir
from os import unlink
from os import unlink

#BoT Configuration Variables
api_id = 9910861
api_hash = "86e927460a8998ba6d84e9c13acfda95"
bot_token = "6281846554:AAEQ97AM-d289ADS-bhJdAEpBvnHhF2crYY"
Channel_Id = -1001804018431
bot = Client("bot",api_id=api_id,api_hash=api_hash,bot_token=bot_token)
boss = ['UHTRED_OF_BEBBANBURG','Stvz20']#usuarios supremos
Configs = {"uclv":'',"gtm":"","uvs":"","ltu":"a816210ff41853b689c154bad264da8e", 
			"ucuser": "", "ucpass":"","uclv_p":"", "gp":'socks5://190.15.159.152:10089', "s":"On", 
			'UHTRED_OF_BEBBANBURG': {'z': 99,"m":"u","a":"c","t":"y"}, 
			'Stvz20': {'z': 99,"m":"u","a":"c","t":"y"}, 
			'Locura05': {'z': 99,"m":"u","a":"c","t":"y"}, 
			'mcfee2828': {'z': 99,"m":"u","a":"c","t":"y"}
			}

Urls = {} #urls subidos a educa
Urls_draft = {} #urls para borrar de draft
Config = {} #configuraciones privadas de moodle
id_de_ms = {} #id de mensage a borrar con la funcion de cancelar
root = {} #directorio actual
downlist = {} #lista de archivos descargados
procesos = 0 #numero de procesos activos en el bot

#Acceso de Uso al BoT
def acceso(username):
     if username in Config or username in boss:
         if exists('downloads/'+str(username)+'/'):pass
         else:os.makedirs('downloads/'+str(username)+'/')	
         try:Urls[username]
         except:Urls[username] = []
         try:Config[username]
         except:Config[username] = {"username":"","password":"","repoid":"","host":""}
         try:id_de_ms[username]
         except:id_de_ms[username] = {"msg":"","proc":""}
         try:root[username]
         except:root[username] = {"actual_root":f"downloads/{str(username)}"}
         try:downlist[username]
         except:downlist[username] = []
     else:return False
     
#Conf User
async def send_config():
    try:await bot.edit_message_text(Channel_Id,message_id=3,text=dumps(Configs,indent=4))
    except:pass

#inicio
@bot.on_message(filters.command("start", prefixes="/") & filters.private)
async def start(client, message):
    username = message.from_user.username
    send = message.reply
    try:await get_messages()
    except:await send_config()
    if acceso(username) == False:
        await send("⛔ 𝑵𝒐 𝒕𝒊𝒆𝒏𝒆 𝒂𝒄𝒄𝒆𝒔𝒐")
        return
    else:pass
    await send("Tines Acceso ")

bot.start()
bot.send_message(5416296262,'**BoT Iniciado**')
bot.loop.run_forever()
