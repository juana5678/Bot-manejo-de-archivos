import tgcrypto
import os
from pyrogram import Client , filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from os.path import exists
import shutil
import asyncio
from os import mkdir
from os import unlink
import platform


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

#inicio
@bot.on_message(filters.command("start", prefixes="/") & filters.private)
async def start(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
	try:await get_messages()
	#except:await send_config()
	if comprobacion_de_user(username) == False:
		await send("⛔ 𝑵𝒐 𝒕𝒊𝒆𝒏𝒆 𝒂𝒄𝒄𝒆𝒔𝒐")
		return
	else:pass
	#zipps = str(Configs[username]["z"])
	#auto = Configs[username]["t"]
	#total = shutil.disk_usage(os.getcwd())[0]
	#used = shutil.disk_usage(os.getcwd())[1]
	#free = shutil.disk_usage(os.getcwd())[2]	
	#uname = platform.uname()
	#svmem = psutil.virtual_memory()
	#a = await client.send_message(username,'**Por Favor Espere...**')
        #msg = f"Hola☺️⚡🤖\n"
	msg = f"**ADM BoT 🤖@Stvz20🤖**\n"
	#msg += f"➣𝘡𝘪𝘱𝘴 𝘤𝘰𝘯𝘧𝘪𝘨𝘶𝘳𝘢𝘥𝘰𝘴 𝘢: **{zipps}MB**\n"	    
	#msg += "➣𝘌𝘴𝘵𝘢𝘥𝘰 𝘥𝘦𝘭 𝘣𝘰𝘵: "+ Configs["s"] +"\n"
	#if auto == "y":
	#	msg += "➣𝘈𝘶𝘵𝘰𝘮𝘢𝘵𝘪𝘤 𝘜𝘱: **On**\n\n"
	#else:
	#	msg += "➣𝘈𝘶𝘵𝘰𝘮𝘢𝘵𝘪𝘤 𝘜𝘱: **Off**\n\n"
	if Configs[username]["a"] == "l":
		mode = "☁️Subida☁️ ➥ **UVS.LTU**\n"
	elif Configs[username]["a"] == "h":
		mode = "☁️ Subida ☁️ ➥ **GTM**\n"
	elif Configs[username]["a"] == "d":
		mode = "☁️ 𝓝𝓾𝓫𝓮 𝓟𝓮𝓻𝓼𝓸𝓷𝓪𝓵 ☁️\n\n"
	elif Configs[username]["a"] == "a":
		mode = "➣𝘜𝘤𝘭𝘷 ➥ **Directs Links (Procfile)**\n"
	else:
		mode = "**☁️ Enlaces de Descaga Directa ☁️**\n"
	#msg += "**Bienvenido A este Maravilloso Sistema de Descaga, De Ante mano Gracias por utilizar Nuestros Servicios❤️**\n"
	#msg += f"➣𝘚𝘺𝘴𝘵𝘦𝘮: **{uname.system}**\n"
	#msg += f"➣𝘔𝘢𝘤𝘩𝘪𝘯𝘦: **{uname.machine}**\n\n"
	#msg += "**📈Info CPU📈**\n"
	#msg += f"**Procesadores Lógicos**: **{psutil.cpu_count(logical=False)}**"
	#msg += f"\n➣𝘛𝘰𝘵𝘢𝘭 𝘤𝘰𝘳𝘦𝘴: **{psutil.cpu_count(logical=True)}**"
	#msg += f"\n**📉CPU Usado📉**: **{psutil.cpu_percent()}%**\n\n"
	#msg += "**Info Memoria RAM**\n"
	#msg += f"**⚙️Total: **{sizeof_fmt(svmem.total)}**\n"
	#msg += f"**⚙️Libre: {sizeof_fmt(svmem.available)}**\n"
	#msg += f"** Usado: {sizeof_fmt(svmem.used)}**\n"
	#msg += f"**Memoria RAM Usada: **{sizeof_fmt(svmem.percent)}%**\n\n"
	#msg += f"**Usa el Comando:\n/uvs > Para usar La Nube uvs.ltu\n/gtm > Para Usar La Nube GTM**\n"
	#msg += f"➣𝘛𝘰𝘵𝘢𝘭 𝘴𝘵𝘰𝘳𝘢𝘨𝘦: **{sizeof_fmt(used)}** / **{sizeof_fmt(total)}**\n"
	#msg += f"➣𝘍𝘳𝘦𝘦 𝘴𝘵𝘰𝘳𝘢𝘨𝘦: **{sizeof_fmt(free)}**\n\n"
        msg = f"**Joder Tío, Esto funciona**\n"
	msg += mode
	await a.edit(msg)

#Funciones BoT
async def get_messages():
	msg = await bot.get_messages(Channel_Id,message_ids=3)
	Configs.update(loads(msg.text))
async def send_config():
	try:
		await bot.edit_message_text(Channel_Id,message_id=3,text=dumps(Configs,indent=4))
	except:
		pass
def comprobacion_de_user(username):
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
	else:
		return False

print("started")
bot.start()
bot.send_message(5416296262,'**BoT Iniciado**')
bot.loop.run_forever()
