import shutil
import asyncio
import tgcrypto
import aiohttp
import aiohttp_socks
import yt_dlp
import os
import aiohttp
import re
import requests
import json
import psutil
import platform
import pymegatools
from pyrogram import Client , filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from json import loads,dumps
from pathlib import Path
from os.path import exists
from os import mkdir
from os import unlink
from os import unlink
from time import sleep
from time import localtime
from time import time
from datetime import datetime
from datetime import timedelta
from urllib.parse import quote
from urllib.parse import quote_plus
from urllib.parse import unquote_plus
from random import randint
from re import findall
from yarl import URL
from bs4 import BeautifulSoup
from io import BufferedReader
from aiohttp import ClientSession
from py7zr import SevenZipFile
from py7zr import FILTER_COPY
from zipfile import ZipFile
from multivolumefile import MultiVolume

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

#Comprobacion de Procesos
def comprobar_solo_un_proceso(username):
    if id_de_ms[username]["proc"] == "Up" :
        rup = "𝒀𝒂 𝒕𝒊𝒆𝒏𝒆 𝒖𝒏 𝒑𝒓𝒐𝒄𝒆𝒔𝒐 𝒂𝒄𝒕𝒊𝒗𝒐. 𝑼𝒔𝒆 **/cancel** 𝒐 𝒆𝒔𝒑𝒆𝒓𝒆"
        return rup
    else:
        return False
#Maximos Procesos
def total_de_procesos():
    global procesos
    hgy = "𝑬𝒍 𝒃𝒐𝒕 𝒕𝒊𝒆𝒏𝒆 𝒅𝒆𝒎𝒂𝒔𝒊𝒂𝒅𝒐𝒔 𝒑𝒓𝒐𝒄𝒆𝒔𝒐𝒔 𝒂𝒄𝒕𝒊𝒗𝒐𝒔. 𝑷𝒓𝒖𝒆𝒃𝒆 𝒆𝒏 𝒖𝒏𝒐𝒔 𝒎𝒊𝒏𝒖𝒕𝒐𝒔."
    if procesos >= 15:
        return hgy
    else:
        return False


#inicio
@bot.on_message(filters.command("start", prefixes="/") & filters.private)
async def start(client, message):
    username = message.from_user.username
    send = message.reply
    try:await get_messages()
    except:await send_config()
    if acceso(username) == False:
        await send("**⚠️🔺No Tienes Contrato Activo en Este BoT🔺⚠️\nContacta al Administrador: @Stvz20**")
        return
    else:pass
    msg = 'Hola'
    if Configs[username]["a"] == "l":
        mode = "**Subida hacía uvs.ltu**\n"
    msg += mode
    await send(msg)

#Comfiguracion de Nubes
@bot.on_message(filters.command("uvs_ltu", prefixes="/") & filters.private)
async def uvs_ltu(client, message):
    username = message.from_user.username
    send = message.reply
    try:await get_messages()
    except:await send_config()
    if acceso(username) == False:
        await send("**⚠️🔺No Tienes Contrato Activo en Este BoT🔺⚠️\nContacta al Administrador: @Stvz20**")
        return
    else:pass
    Configs[username]["m"] = "u"
    Configs[username]["a"] = "l"
    Configs[username]["z"] = 19
    await send_config()
    await send("**Nube ☁️ uvs.ltu Configurada**")


#Descargas de Archivos Reenviados
@bot.on_message(filters.command("down", prefixes="/") & filters.private)
async def download_archive(client: Client, message: Message):
    global procesos
    username = message.from_user.username
    send = message.reply
    try:await get_messages()
    except:await send_config()
    if acceso(username) == False:
        await send("⛔ 𝑵𝒐 𝒕𝒊𝒆𝒏𝒆 𝒂𝒄𝒄𝒆𝒔𝒐")
        return
    else:pass
    comp = comprobar_solo_un_proceso(username) 
    if comp != False:
        await send(comp)
        return
    else:pass
    total_proc = total_de_procesos()
    if total_proc != False:
        await send(total_proc)
        return
    else:pass
    procesos += 1
    msg = await send("*Por Favor Espere 🔍")
    count = 0
    for i in downlist[username]:
        filesize = int(str(i).split('"file_size":')[1].split(",")[0])
        try:filename = str(i).split('"file_name": ')[1].split(",")[0].replace('"',"")	
        except:filename = str(randint(11111,999999))+".mp4"
        await bot.send_message(Channel_Id,f'**@{username} Envio un #archivo:**\n**Filename:** {filename}\n**Size:** {sizeof_fmt(filesize)}')	
        start = time()		
        await msg.edit(f"**Iniciando Descarga...**\n\n`{filename}`")
        try:
            a = await i.download(file_name=str(root[username]["actual_root"])+"/"+filename,progress=downloadmessage_progres,progress_args=(filename,start,msg))
            if Path(str(root[username]["actual_root"])+"/"+ filename).stat().st_size == filesize:
                await msg.edit("**Down Finish**")
            count +=1
        except Exception as ex:
                if procesos > 0:
                    procesos -= 1
                else:pass
                if "[400 MESSAGE_ID_INVALID]" in str(ex): pass		
                else:
                    await bot.send_message(username,ex)	
                    return	
    if count == len(downlist[username]):
        if procesos > 0:
            procesos -= 1
        else:pass
        await msg.edit("Finish Down All")
        downlist[username] = []
        count = 0
        msg = files_formatter(str(root[username]["actual_root"]),username)
        await limite_msg(msg[0],username)
        return
    else:
        await msg.edit("**Error**")
        if procesos > 0:
            procesos -= 1
        else:pass
        msg = files_formatter(str(root[username]["actual_root"]),username)
        await limite_msg(msg[0],username)
        downlist[username] = []
        return

#Descarga de Archivos y Enlaces 
@bot.on_message(filters.media & filters.private)
async def delete_draft_y_down_media(client: Client, message: Message):
    global procesos
    username = message.from_user.username
    send = message.reply
    try:await get_messages()
    except:await send_config()
    if acceso(username) == False:
        await send("⛔ 𝑵𝒐d 𝒕𝒊𝒆𝒏𝒆 𝒂𝒄𝒄𝒆𝒔𝒐")
        return
    else:pass
    if str(message).split('"file_name": ')[1].split(",")[0].replace('"',"").endswith(".txt") and Configs[username]["m"] == "d":
        if message.from_user.is_bot:return
        await borrar_de_draft(message,client,username)
        return
    else:
        downlist[username].append(message)
        await send("**/down Para Comenzar Descaga**", quote=True)
        return

#Mensajes De Progreso de Subida y Descaga
def download_progres(data,message,format):
    if data["status"] == "downloading":
        filename = data["filename"].split("/")[-1]
        _downloaded_bytes_str = data["_downloaded_bytes_str"]
        _total_bytes_str = data["_total_bytes_str"]
        if _total_bytes_str == "N/A":
            _speed_str = data["_speed_str"].replace(" ","")
            _total_bytes_str = data["_total_bytes_estimate_str"]
            _format_str = format
            msg = f"`Nombre: {filename}`\n\n"
            msg+= f"`Progreso: {_downloaded_bytes_str} - {_total_bytes_str}`\n\n"
            msg+= f"`Calidad: {_format_str}p`\n\n"
            global seg
            if seg != localtime().tm_sec:
                try:message.edit(msg,reply_markup=message.reply_markup)
                except:pass
            seg = localtime().tm_sec
async def downloadmessage_progres(chunk,filesize,filename,start,message):
    now = time()
    diff = now - start
    mbs = chunk / diff
    msg = f"`Nombre: {filename}`\n\n"
    try:
       msg+= update_progress_bar(chunk,filesize)+ "  " + sizeof_fmt(mbs)+"/s\n\n"
    except:pass
    msg+= f"`Progreso: {sizeof_fmt(chunk)} - {sizeof_fmt(filesize)}`\n\n"	
    global seg
    if seg != localtime().tm_sec:
        try: await message.edit(msg)
        except:pass
    seg = localtime().tm_sec
def uploadfile_progres(chunk,filesize,start,filename,message):
    now = time()
    diff = now - start
    mbs = chunk / diff
    msg = f"📦 𝐍𝐚𝐦𝐞: {filename}\n\n"
    try:
       msg+=update_progress_bar(chunk,filesize)+ "  " + sizeof_fmt(mbs)+"/s\n\n"
    except:pass
    msg+= f"▶️ 𝚄𝚙𝚕𝚘𝚊𝚍𝚒𝚗𝚐: {sizeof_fmt(chunk)} of {sizeof_fmt(filesize)}\n\n"
    global seg
    if seg != localtime().tm_sec: 
        message.edit(msg)
    seg = localtime().tm_sec
async def downloadmessage_tg(chunk,filesize,filename,start,message):
    now = time()
    diff = now - start
    mbs = chunk / diff
    msg = f"📦 𝐍𝐚𝐦𝐞: {filename}\n\n"
    try:
       msg+=update_progress_bar(chunk,filesize)+ "  " + sizeof_fmt(mbs)+"/s\n\n"
    except:pass
    msg+= f"▶️ 𝚄𝚙𝚕𝚘𝚊𝚍𝚒𝚗𝚐: {sizeof_fmt(chunk)} of {sizeof_fmt(filesize)}\n\n"	
    global seg
    if seg != localtime().tm_sec:
        try: await message.edit(msg)
        except:pass
    seg = localtime().tm_sec

bot.start()
bot.send_message(5416296262,'**BoT Iniciado**')
bot.loop.run_forever()
