from pyrogram import Client , filters 
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

#Datos
api_id = 9910861
api_hash = "86e927460a8998ba6d84e9c13acfda95"
bot_token = '6281846554:AAEQ97AM-d289ADS-bhJdAEpBvnHhF2crYY'
#Channel_Id = chanel_id
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

#inicio
@bot.on_message(filters.command("uclv", prefixes="/")& filters.private)
async def uclv(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
	try:await Client.get_messages()
	except:await send_config()
	if comprobacion_de_user(username) == False:
		await send("⛔ 𝑵𝒐 𝒕𝒊𝒆𝒏𝒆 𝒂𝒄𝒄𝒆𝒔𝒐")
		return
	else:pass
	Configs[username]["m"] = "u"
	Configs[username]["a"] = "c"
	Configs[username]["z"] = 399
	await send_config()
	await send("✅ 𝑫𝒐𝒏𝒆")




print("started")
bot.start()
bot.send_message(5416296262,'BoT Iniciado')
bot.loop.run_forever()
