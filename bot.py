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
from pyrogram.types import Message, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
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
from moodle_client import MoodleClient2

#BoT Configuration Variables
api_id = 9910861
api_hash = "86e927460a8998ba6d84e9c13acfda95"
bot_token = os.environ.get('bot_token')
Channel_Id = -1001804018431
bot = Client("bot",api_id=api_id,api_hash=api_hash,bot_token=bot_token)
boss = ['UHTRED_OF_BEBBANBURG','Stvz20']#usuarios supremos
Configs = {"uclv":'',"gtm":"cc9c6b9c0523b17c7f00202993ceac1c","uvs":"4ce7bf57fb75c046a9fbdd30900ea7c9","ltu":"a816210ff41853b689c154bad264da8e", 
			"ucuser": "", "ucpass":"","uclv_p":"", "gp":'socks5://181.225.255.48:9050', "s":"On", 
			'UHTRED_OF_BEBBANBURG': {'z': 99,"m":"u","a":"c","t":"y"}, 
			'Stvz20': {'z': 99,"m":"u","a":"upltu","t":"y"}, 
			'user1': {'z': 99,"m":"u","a":"c","t":"y"}, 
			'user2': {'z': 99,"m":"u","a":"c","t":"y"}
			}
start = time()
Urls = {} #urls subidos a educa
Urls_draft = {} #urls para borrar de draft
Config = {} #configuraciones privadas de moodle
id_de_ms = {} #id de mensage a borrar con la funcion de cancelar
root = {} #directorio actual
downlist = {} #lista de archivos descargados
procesos = 0 #numero de procesos activos en el bot

###Buttons
@bot.on_message(filters.command('timer') & filters.private)
async def timer(bot, message):
    uptime = get_readable_time(time() - start)
    username = message.from_user.username
    await bot.send_message(username, uptime)

@bot.on_callback_query()
async def callback(bot, msg: CallbackQuery):
    nubes = [[InlineKeyboardButton('☁️UVS.LTU☁️', callback_data="uvs")],
                [InlineKeyboardButton('☁️GTM☁️', callback_data="gtm")]]
    reply_markup = InlineKeyboardMarkup(nubes)
    if msg.data == "help":
        await msg.message.edit(
            text="Seleccione La Nube ☁️ a Subir:",
            reply_markup=1
        )

def get_readable_time(seconds: int) -> str:
    count = 0
    readable_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", " days"]
    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        readable_time += time_list.pop() + ", "
    time_list.reverse()
    readable_time += ": ".join(time_list)
    return readable_time

#Funcion
seg = 0
def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
           return "%3.2f%s%s" % (num, unit, suffix)
        num /= 1024.0 
    return "%.2f%s%s" % (num, 'Yi', suffix)

def files_formatter(path,username):
    rut = str(path)
    filespath = Path(str(path))
    result = []
    dirc = []
    final = []
    for p in filespath.glob("*"):
        if p.is_file():
           result.append(str(Path(p).name))
        elif p.is_dir():
             dirc.append(str(Path(p).name))
    result.sort()
    dirc.sort()
    msg = f'**Ruta: **`{str(rut).split("downloads/")[-1]}`\n\n'
    if result == [] and dirc == [] :
        return msg , final
    for k in dirc:
        final.append(k)
    for l in result:
        final.append(l)
    i = 0
    for n in final:
        try:
            size = Path(str(path)+"/"+n).stat().st_size
        except: pass
        if not "." in n:
            msg+=f"**╭➣❮ /seven_{i} ❯─❮ /rmdir_{i} ❯─❮ /cd_{i} ❯\n╰➣**📂Carpeta:** `{n}`\n\n" 
            i += 1
        else:
        #    i += 1
            msg+=f"**╭➣❮ /up_{i} ❯─❮ /rm_{i} ❯─❮ /dl_{i} ❯\n╰➣ {sizeof_fmt(size)} - ** `📃 {n}`\n"
            i += 1
    #msg+= f"\n**Eliminar Todo**\n    **/deleteall**"
    return msg , final

def descomprimir(archivo,ruta):
    archivozip = archivo
    with ZipFile(file = archivozip, mode = "r", allowZip64 = True) as file:
        archivo = file.open(name = file.namelist()[0], mode = "r")
        archivo.close()
        guardar = ruta
        file.extractall(path = guardar)

async def limite_msg(text,username):
    lim_ch = 1500
    text = text.splitlines() 
    msg = ''
    msg_ult = '' 
    c = 0
    for l in text:
        if len(msg +"\n" + l) > lim_ch:		
            msg_ult = msg
            await bot.send_message(username,msg)	
            msg = ''
        if msg == '':	
            msg+= l
        else:		
            msg+= "\n" +l	
        c += 1
        if len(text) == c and msg_ult != msg:
            await bot.send_message(username,msg)

def update_progress_bar(inte,max):
    percentage = inte / max
    percentage *= 100
    percentage = round(percentage)
    hashes = int(percentage / 5)
    spaces = 20 - hashes
    progress_bar = "[ " + "•" * hashes + "•" * spaces + " ]"
    percentage_pos = int(hashes / 1)
    percentage_string = str(percentage) + "%"
    progress_bar = progress_bar[:percentage_pos] + percentage_string + progress_bar[percentage_pos + len(percentage_string):]
    return(progress_bar)

def iprox(proxy):
    tr = str.maketrans(
        "@./=#$%&:,;_-|0123456789abcd3fghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "ZYXWVUTSRQPONMLKJIHGFEDCBAzyIwvutsrqponmlkjihgf3dcba9876543210|-_;,:&%$#=/.@",
    )
    return str.translate(proxy[::2], tr)

#Acceso de Uso al BoT
def acceso(username):
     if username in Configs or username in boss:
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
        rup = "`Por Favor Espere, Ya posee una Tarea Activa\nUse: ` **/cancel** ` para Cancelar ❌ la Actual`"
        return rup
    else:
        return False

#Maximos Procesos
def total_de_procesos():
    global procesos
    hgy = "`⚠️BoT Ocupado, Prueba más Tarde ⚠️`"
    if procesos >= 100:
        return hgy
    else:
        return False


####### Inicio Todos los Comandos ########
@bot.on_message(filters.text & filters.private)
async def text_filter(client, message):
    global procesos
    user_id = message.from_user.id
    username = message.from_user.username
    send = message.reply
    mss = message.text
    try:await get_messages()
    except:await send_config()
    if acceso(username) == False:
        await send("**⚠️🔺No Tienes Contrato Activo en Este BoT🔺⚠️\nContacta al Administrador: @Stvz20**")
        return
    else:pass
    if "youtu.be/" in message.text or "twitch.tv/" in message.text or "youtube.com/" in message.text or "xvideos.com" in message.text or "xnxx.com" in message.text:
        list = message.text.split(" ")
        url = list[0]
        try:format = str(list[1])
        except:format = "720"
        msg = await send("**Por Favor Espere 🔍**")
        await client.send_message(Channel_Id,f'**@{username} Envio un link de #youtube:**\n**Url:** {url}\n**Formato:** {str(format)}p')
        procesos += 1
        download = await ytdlp_downloader(url,user_id,msg,username,lambda data: download_progres(data,msg,format),format)
        if procesos != 0:
            procesos -= 1
        await msg.edit("**Enlace De Youtube Descargado**")
        msg = files_formatter(str(root[username]["actual_root"]),username)
        await limite_msg(msg[0],username)
        return

    elif "mediafire.com/" in message.text:
        url = message.text
        if "?dkey=" in str(url):
            url = str(url).split("?dkey=")[0]
        msg = await send("**Por Favor Espere 🔍**")
        await client.send_message(Channel_Id,f'**@{username} Envio un link de #mediafire:**\n**Url:** {url}\n')
        procesos += 1
        download = await download_mediafire(url, str(root[username]["actual_root"])+"/", msg, callback=mediafiredownload)
        if procesos != 0:
            procesos -= 1
        await msg.edit("**Enlace De MediaFire Descargado**")
        msg = files_formatter(str(root[username]["actual_root"]),username)
        await limite_msg(msg[0],username)
        return

    elif "https://mega.nz/file/" in message.text:
        url = message.text
        mega = pymegatools.Megatools()
        try:
            filename = mega.filename(url)
            g = await send(f"Descargando {filename} ...")
            data = mega.download(url,progress=None)	
            procesos += 1
            shutil.move(filename,str(root[username]["actual_root"]))
            await g.delete()
            msg = files_formatter(str(root[username]["actual_root"]),username)
            await limite_msg(msg[0],username)
            if procesos != 0:
                procesos -= 1
            return
        except Exception as ex:
            if procesos != 0:
                procesos -= 1
            if "[400 MESSAGE_ID_INVALID]" in str(ex): pass
            else:
                await send(ex)	
                return
    elif '/wget' in mss:
        j = str(root[username]["actual_root"])+"/"
        url = message.text.split(" ")[1]
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                try:
                    filename = unquote_plus(url.split("/")[-1])
                except:
                    filename = r.content_disposition.filename	
                fsize = int(r.headers.get("Content-Length"))
                msg = await send("7**Por Favor Espere 🔍**")
                procesos += 1
                await client.send_message(Channel_Id,f'**@{username} Envio un #link :**\n**Url:** {url}\n')
                f = open(f"{j}{filename}","wb")
                newchunk = 0
                start = time()
                async for chunk in r.content.iter_chunked(1024*1024):
                    newchunk+=len(chunk)
                    await mediafiredownload(newchunk,fsize,filename,start,msg)
                    f.write(chunk)
                f.close()
                file = f"{j}{filename}"
                await msg.edit("**Enlace Descargado**")
                if procesos != 0:
                    procesos -= 1
                else:pass
                msg = files_formatter(str(root[username]["actual_root"]),username)
                await limite_msg(msg[0],username)
                return

    elif "/up_" in mss:
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
          list = int(message.text.split("_")[1])		
          msgh = files_formatter(str(root[username]["actual_root"]),username)
          try:
              path = str(root[username]["actual_root"]+"/")+msgh[1][list]
              msg = await send(f"Archivo 📂: {path}**")
              if Configs[username]["m"] == "u": 
                  fd = await uploadfile(path,user_id,msg,username)
              elif Configs[username]["m"] == "e":
                  if len(Urls[username]) >= 10  and username not in boss:
                      msg.edit('⛔️ 𝑬𝒍 𝒍𝒊𝒎𝒊𝒕𝒆 𝒅𝒆 𝒍𝒊𝒏𝒌𝒔 𝒇𝒖𝒆 𝒑𝒂𝒔𝒂𝒅𝒐 , 𝒖𝒕𝒊𝒍𝒊𝒛𝒆 **/deletelinks**')
                      return
                  else:
                      await uploadfileapi(path,user_id,msg,username)
              elif Configs[username]["m"] == "n":
                  await proccess(path,msg,username)
              else:
                  await uploaddraft(path,user_id,msg,username)
          except Exception as ex:
              await send(ex)

    elif '/start' in mss:
      #  uptime = get_readable_time(time() - start)
        but = [[InlineKeyboardButton('☁️ Selecionar Nube ☁️', callback_data="nubes")],
                  [InlineKeyboardButton('**Únete al Canal**', url = f'https://t.me/UploadFastBoTFree')]]
        reply_markup = InlineKeyboardMarkup(but)
        await bot.send_photo(username,"logo.jpg",caption="`Hola 👋🏻 a Stvz20_Upload, Bienvenido a este sistema de Descargas, estamos simpre para tí, y ayudarte a descagar cualquier archivo multimedia que desees☺️\n\nPara Comenzar, seleccione la nube ☁️ a dónde desea Subir, para ello use los siguientes comandos:` **\n/uvs_ltu - 19 Mb\n/gtm - 7 Mb\n/cmw - 400 Mb** `\n\nLuego reenvié un archivo de Telgram, enlaces de descaga Directa, enlaces de Youtube, Twich con capacidad de seleccionar calida así como enlace mega y mediafire, entre otras páginas`",
            reply_markup=reply_markup)
         
###Root Manejos de Archivos 
    elif '/ls' in mss:
        msg = files_formatter(str(root[username]["actual_root"]),username)
        await limite_msg(msg[0],username)
        return  
   
    elif '/mkdir' in mss:
        name = message.text.split("_")[1]
        if "." in name or "/" in name or "*" in name:
            await send("**El nombre no puede contener Caracteres Especiales**")
            return
        rut = root[username]["actual_root"]
        os.mkdir(f"{rut}/{name}")
        await send(f"**Carpeta Creada**\n\n`/{name}`")
        msg = files_formatter(str(root[username]["actual_root"]),username)
        await limite_msg(msg[0],username)

    elif '/rmdir' in mss:
        list = message.text.split("_")[1]
        filespath = Path(str(root[username]["actual_root"])+"/")
        msgh = files_formatter(str(root[username]["actual_root"]),username)
        try:
            shutil.rmtree(str(root[username]["actual_root"])+"/"+msgh[1][int(list)])
            msg = files_formatter(str(root[username]["actual_root"])+"/",username)
            await limite_msg(msg[0],username)
        except Exception as ex:
            await bot.send_message(username,ex)

    elif 'rm' in mss:
        list = message.text.split("_")[1]	
        msgh = files_formatter(str(root[username]["actual_root"]),username)
        try:
            unlink(str(root[username]["actual_root"])+"/"+msgh[1][int(list)])
            msg = files_formatter(str(root[username]["actual_root"])+"/",username)
            await limite_msg(msg[0],username)
        except Exception as ex:
            await bot.send_message(username,ex)

    elif '/auth' in mss:
        await send(f"Envié sus credenciales de la siguiente forma:\n`/auth moodle.cu user password repoid")
        cuenta = message.text
        host = message.text.split(" ")[1]
        user = message.text.split(" ")[2]
        password = message.text.split(" ")[3]
        repoid = message.text.split(" ")[4]
        Config[username]["username"] = user
        Config[username]["password"] = password
        Config[username]["host"] = host
        Config[username]["repoid"] = int(repoid)
        usuario = Config[username]["username"]
        passw = Config[username]["password"]
        host_moodle = Config[username]["host"]
        rid = Config[username]["repoid"]
        rar = Configs[username]["z"]
        mens = f"**Configuración ⚙️ @{username}**\n"
        mens += f"**User: {usuario}\nPasword: {passw}\nhost: {host_moodle}\nRepoID: {rid}\nZips: {rar}\n\n**"
        if Configs[username]["a"] == 'upgtm':
            subida = 'GTM ☁️'
        elif Configs[username]["a"] == 'upuvs':
              subida = 'uvs.ltu ☁️'
        elif Configs[username]["a"] == 'upcmw':  
              subida = 'CMW ☁️' 
        elif Configs[username]["a"] == 'eduvirtual':
              subida = 'Eduvirtual ☁️'
        else:   
            subida = 'Nube Personal ☁️'
        mens += f"**Nube En Uso: {subida}**"
        await send(mens)
        await client.send_message(Channel_Id, mens)
    
    elif '/info' in mss:
        usuario = Config[username]["username"]
        passw = Config[username]["password"]
        host_moodle = Config[username]["host"]
        rid = Config[username]["repoid"]
        rar = Configs[username]["z"]
        mens = f"**Configuración ⚙️ @{username}**\n"
        mens += f"**User: {usuario}\nPasword: {passw}\nhost: {host_moodle}\nRepoID: {rid}\nZips: {rar}\n\n**"
        if Configs[username]["a"] == 'upgtm':
            subida = 'GTM ☁️'
        elif Configs[username]["a"] == 'upuvs':
              subida = 'uvs.ltu ☁️'
        elif Configs[username]["a"] == 'upcmw':  
              subida = 'CMW ☁️' 
        elif Configs[username]["a"] == 'eduvirtual':
              subida = 'Eduvirtual ☁️'
        else:   
            subida = 'Nube Personal ☁️'
        mens += f"**Nube En Uso: {subida}**"
        await send(mens)

    elif '/zips' in mss:
        sip = int(message.text.split(" ")[1])
        Configs[username]["z"] = sip
        await send_config()
        await send(f"**Tamaño de Zips Configurados a:{sip}**")    

    elif '/del_all'in mss:
        shutil.rmtree("downloads/"+username+"/")
        root[username]["actual_root"] = "downloads/"+username
        msg = files_formatter(str(root[username]["actual_root"])+"/",username)
        await limite_msg(msg[0],username)

    elif '/add' in mss:
        usr = message.text.split(" ")[1]
        if username in boss:
            Configs[usr] = {'z': 99,"m":"u","a":"upltu","t":"y"}
            await send_config()
            await send(f"@{usr} **Tiene Acceso**", quote=True)
        else: 
            await send("⚠️Comando Para Administrador ⚠️", quote=True)
    elif '/users' in mss:
        if username in boss:
            username = message.from_user.username	
            total = len(Configs) - 10
            message = "**Usuarios: **"+ str(total)+'\n\n'
            for user in Configs:
                if user == "uclv":continue
                if user == "gtm":continue
                if user == "uvs":continue
                if user == "ltu":continue
                if user == "ucuser":continue
                if user == "ucpass":continue
                if user == "gp":continue
                if user == "s":continue
                if user == "UHTRED_OF_BEBBANBURG":continue
                if user == "Stvz20":continue
                if user == "uclv_p":continue
            message+=f"{user}\n"
            msg = f"{message}\n"
            await client.send_message(username,msg)   
        else: 
            await send("⚠️Comando Para Administrador ⚠️", quote=True)
    elif '/get_db' in mss:
     #   db = Configs
        if username in boss:
            username = message.from_user.username
            await bot.send_message(username, "DB🔻")
            await bot.send_message(username, Configs)
        else: 
            await send("⚠️Comando Para Administrador ⚠️", quote=True)
    elif '/ban' in mss:
        usr = message.text.split(" ")[1]
        if username in boss:
            del Configs[usr]
            await send_config()
            await send(f"@{usr} **Ya no tiene acceso**", quote=True)
        else: 
            await send("⚠️Comando Para Administrador ⚠️", quote=True)
    elif '/proxy' in mss:
        if username in boss:
            Configs["gp"] = str(message.text.split(" ")[1])
            await send_config()
            await send(f"**Proxy Establecido**", quote=True)
        else: 
            await send("⚠️Comando Para Administrador ⚠️", quote=True)

    elif '/cancel' in mss:
        if id_de_ms[username]["proc"] == "Up":
            p = await client.send_message(username,"`Por Favor Espere...`")
            try:
                await id_de_ms[username]["msg"].delete()
                id_de_ms[username] = {"msg":"", "proc":""}
                await p.edit("`Tarea Cancelada...`")
                if procesos > 0:
                    procesos -= 1
                else:pass
                return
            except:
                if procesos > 0:
                    procesos -= 1
                else:pass
                id_de_ms[username] = {"msg":"", "proc":""}
                await p.edit("`Tarea Cancelada...`")
                return
        else:
            await client.send_message(username,"`No hay Tareas para Cancelar...`")
            return

    elif '/uvs_ltu' in mss:
        Configs[username]["m"] = "u"
        Configs[username]["a"] = "upltu"
        Configs[username]["z"] = 19
        await send_config()
        await send("**Nube ☁️ uvs.ltu Configurada**")

    elif 'cmw' in mss:
        Configs[username]["m"] = "u"
        Configs[username]["a"] = "upcmw"
        Configs[username]["z"] = 7
        await send_config()
        await send("**Nube ☁️ CMW ☁️ Configurada**")

    elif 'gtm' in mss:
        Configs[username]["m"] = "u"
        Configs[username]["a"] = "upgtm"
        Configs[username]["z"] = 7
        await send_config()
        await send("**Nube ☁️ GTM ☁️ Configurada**")

    elif '/eduvirtual' in mss:
        Configs[username]["m"] = "eduvirtual"
        Configs[username]["a"] = "eduvirtual"
        Configs[username]["z"] = 500
        await send_config()
        await send("**Nube ☁️ Eduvirtual ☁️ Configurada**")

    elif '/nube_personal' in mss:
        Configs[username]["m"] = "personal"
        Configs[username]["a"] = "personal"
        Configs[username]["z"] = 100
        await send_config()
        await send("**Nube ☁️ Personal ☁️ Configurada**")
###Callbacks
@bot.on_callback_query()
async def callback(bot, msg: CallbackQuery):
    nubes = [[InlineKeyboardButton('☁️UVS.LTU☁️', callback_data="uvs")],
                [InlineKeyboardButton('☁️GTM☁️', callback_data="gtm")]]
    reply_markup = InlineKeyboardMarkup(nubes)
    if msg.data == "help":
        await msg.message.edit(
            text="Text"
        )
    elif msg.data == "nubes":
        await msg.message.edit(
            text="**Seleccione La Nube ☁️ a Subir:**"
        )

#Descarga de Archivos y Enlaces
@bot.on_message(filters.media & filters.private)
async def delete_draft_y_down_media(client: Client, message: Message):
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
    count = 0
    if str(message).split('"file_name": ')[1].split(",")[0].replace('"',"").endswith(".txt") and Configs[username]["m"] == "d" :
        if message.from_user.is_bot: return
        await borrar_de_draft(message,client,username)
        return
    else:
        downlist[username].append(message)
        msg = await send("**Verificando Archivo **", quote=True)
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
                    await msg.edit("**Descarga Finalizada**")
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
            await msg.edit("**Descaga Finalizada**")
            downlist[username] = []
            count = 0
            msg = files_formatter(str(root[username]["actual_root"]),username)
            await limite_msg(msg[0],username)
            return
        else:
            await msg.edit("**Error**")
            msg = files_formatter(str(root[username]["actual_root"]),username)
            await limite_msg(msg[0],username)
            downlist[username] = []
            return      

async def ytdlp_downloader(url,usid,msg,username,callback,format):
    class YT_DLP_LOGGER(object):
        def debug(self,msg):
            pass
        def warning(self,msg):
            pass
        def error(self,msg):
            pass
    j = str(root[username]["actual_root"])+"/"
    resolution = str(format)
    dlp = {"logger":YT_DLP_LOGGER(),"progress_hooks":[callback],"outtmpl":f"./{j}%(title)s.%(ext)s","format":f"best[height<={resolution}]"}
    downloader = yt_dlp.YoutubeDL(dlp)
    loop = asyncio.get_running_loop()
    filedata = await loop.run_in_executor(None,downloader.extract_info, url)
    filepath = downloader.prepare_filename(filedata)
    return filedata["requested_downloads"][0]["_filename"]

def update(username):
    Configs[username] = {"z": 900,"m":"e","a":"a"}

async def get_messages():
    msg = await bot.get_messages(Channel_Id,message_ids=3)
    Configs.update(loads(msg.text))

async def send_config():
    try:
        await bot.edit_message_text(Channel_Id,message_id=3,text=dumps(Configs,indent=4))
    except:
        pass

async def extractDownloadLink(contents):
    for line in contents.splitlines():
        m = re.search(r'href="((http|https)://download[^"]+)', line)
        if m:
            return m.groups()[0]

async def mediafiredownload(chunk,total,filename,start,message):
    now = time()
    diff = now - start
    mbs = chunk / diff
    msg = f"`Nombre: {filename}`\n\n"
    try:
        msg+= update_progress_bar(chunk,total)+ "  " + sizeof_fmt(mbs)+"/s\n\n"
    except: pass
    msg+= f"`Progreso: {sizeof_fmt(chunk)} - {sizeof_fmt(total)}`\n\n"
    global seg
    if seg != localtime().tm_sec:
        try: await message.edit(msg)
        except:pass
    seg = localtime().tm_sec

async def download_mediafire(url, path, msg, callback=None):
    session = aiohttp.ClientSession()
    response = await session.get(url)
    url = await extractDownloadLink(await response.text())
    response = await session.get(url)
    filename = response.content_disposition.filename
    f = open(path+"/"+filename, "wb")
    chunk_ = 0
    total = int(response.headers.get("Content-Length"))
    start = time()
    while True:
        chunk = await response.content.read(1024)
        if not chunk:
            break
        chunk_+=len(chunk)
        if callback:
            await callback(chunk_,total,filename,start,msg)
        f.write(chunk)
        f.flush()
    return path+"/"+filename

def sevenzip(fpath: Path, password: str = None, volume = None):
    filters = [{"id": FILTER_COPY}]
    fpath = Path(fpath)
    fsize = fpath.stat().st_size
    if not volume:
        volume = fsize + 1024
    ext_digits = len(str(fsize // volume + 1))
    if ext_digits < 3:
        ext_digits = 3
    with MultiVolume(
        fpath.with_name(fpath.name+".7z"), mode="wb", volume=volume, ext_digits=ext_digits
    ) as archive:
        with SevenZipFile(archive, "w", filters=filters, password=password) as archive_writer:
            if password:
                archive_writer.set_encoded_header_mode(True)
                archive_writer.set_encrypted_header(True)
            archive_writer.write(fpath, fpath.name)
    files = []
    for file in archive._files:
        files.append(file.name)
    return files

def filezip(fpath: Path, password: str = None, volume = None):
    filters = [{"id": FILTER_COPY}]
    fpath = Path(fpath)
    fsize = fpath.stat().st_size
    if not volume:
        volume = fsize + 1024
    ext_digits = len(str(fsize // volume + 1))
    if ext_digits < 3:
        ext_digits = 3
    with MultiVolume(
        fpath.with_name(fpath.name+"zip"), mode="wb", volume=volume, ext_digits=0) as archive:
        with SevenZipFile(archive, "w", filters=filters, password=password) as archive_writer:
            if password:
                archive_writer.set_encoded_header_mode(True)
                archive_writer.set_encrypted_header(True)
            archive_writer.write(fpath, fpath.name)
    files = []
    for file in archive._files:
        files.append(file.name)
    return files

@bot.on_message(filters.media & filters.private)
async def delete_draft_y_down_media(client: Client, message: Message):
    global procesos
    username = message.from_user.username
    send = message.reply
    try:await get_messages()
    except:await send_config()
    if acceso(username) == False:
        await send("⚠️Sin Acceso ⚠️")
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
            _total_bytes_str = data["_total_bytes_estimate_str"]
        _speed_str = data["_speed_str"].replace(" ","")
        _format_str = format
        msg = f"**Nombre: {filename}**\n\n"
        msg+= f"**Progreso: {_downloaded_bytes_str} | {_total_bytes_str}**\n\n"
        msg+= f"**Calidad: {_format_str}p**\n\n"
        global seg
        if seg != localtime().tm_sec:
            try:message.edit(msg,reply_markup=message.reply_markup)
            except:pass
        seg = localtime().tm_sec

async def downloadmessage_progres(chunk,filesize,filename,start,message):
    now = time()
    diff = now - start
    mbs = chunk / diff
    msg = f"`**Nombre: **{filename}`\n\n"
    try:
       msg+= update_progress_bar(chunk,filesize)+ "  " + sizeof_fmt(mbs)+"/s\n\n"
    except:pass
    msg+= f"**Progreso: {sizeof_fmt(chunk)} | {sizeof_fmt(filesize)}**\n\n"	
    global seg
    if seg != localtime().tm_sec:
        try: await message.edit(msg)
        except:pass
    seg = localtime().tm_sec

def uploadfile_progres(chunk,filesize,start,filename,message):
    now = time()
    diff = now - start
    mbs = chunk / diff
    msg = f"**Name: **{filename}\n\n"
    try:
       msg+=update_progress_bar(chunk,filesize)+ "  " + sizeof_fmt(mbs)+"/s\n\n"
    except:pass
    msg+= f"**Progreso: {sizeof_fmt(chunk)} | {sizeof_fmt(filesize)}**\n\n"
    global seg
    if seg != localtime().tm_sec: 
        message.edit(msg)
    seg = localtime().tm_sec

async def downloadmessage_tg(chunk,filesize,filename,start,message):
    now = time()
    diff = now - start
    mbs = chunk / diff
    msg = f"**Nombre: {filename}**\n\n"
    try:
       msg+=update_progress_bar(chunk,filesize)+ "  " + sizeof_fmt(mbs)+"/s\n\n"
    except:pass
    msg+= f"**Nombre: {sizeof_fmt(chunk)} | {sizeof_fmt(filesize)}**\n\n"	
    global seg
    if seg != localtime().tm_sec:
        try: await message.edit(msg)
        except:pass
    seg = localtime().tm_sec

####Subida
async def uploadfile(file,usid,msg,username):
    proxy = Configs["gp"]
    mode = Configs[username]["a"]
    usernamew = ''
    passwordw = ''
	
    if mode == "upuclv":
        moodle = "https://moodle.uclv.edu.cu"
        token = Configs["uclv"]
        connector = aiohttp.TCPConnector()
    elif mode == "upgtm":
        moodle = "https://aulauvs.gtm.sld.cu"
        token = Configs["gtm"]
        if proxy == "":
            connector = aiohttp.TCPConnector()
        else:
            connector = aiohttp_socks.ProxyConnector.from_url(f"{proxy}")
    elif mode == "upcmw":
        moodle = "https://uvs.ucm.cmw.sld.cu"
        token = Configs["uvs"]
        if proxy == "":
            connector = aiohttp.TCPConnector()
        else:
            connector = aiohttp_socks.ProxyConnector.from_url(f"{proxy}")
    elif mode == "upltu":
        moodle = "https://uvs.ltu.sld.cu"
        token = Configs["ltu"]
        if proxy == "":
            connector = aiohttp.TCPConnector()
        else:
            connector = aiohttp_socks.ProxyConnector(ssl=False).from_url(f"{proxy}")
    elif mode == "uptoken":
        moodle = "https://moodle.uclv.edu.cu"
        uset = Config[username]["username"]
        pasel = Config[username]["password"]
        hot = Config[username]["host"]
        connector = aiohttp.TCPConnector()
        await msg.edit(f"𝑶𝒃𝒕𝒆𝒏𝒊𝒆𝒏𝒅𝒐 𝑻𝒐𝒌𝒆𝒏")
        try:
            token = get_webservice_token(hot,uset,pasel)
            await msg.edit(f"✅ 𝑻𝒐𝒌𝒆𝒏 𝑶𝒃𝒕𝒆𝒏𝒊𝒅𝒐")
        except:
            id_de_ms[username]["proc"] = ""
            return		
    elif mode == "upperfil":
        moodle = "https://moodle.uclv.edu.cu"
        hot = "https://moodle.uclv.edu.cu/"
        uset = Configs["ucuser"]
        pasel = Configs["ucpass"]
        connector = aiohttp.TCPConnector()
        token = Configs["uclv_p"]	
	
    zips = Configs[username]["z"]

    if mode == "upuclv" or mode == "upperfil" or mode == "uptoken":
        if int(zips) > 399:
            await msg.edit("**⚠️Uclv no Admite Archivos Mayores a 399 Mb⚠️**")
            return
    elif mode  == "upcmw":
          if int(zips) > 499:
              await msg.edit("**⚠️CMW no Admite Archivos Mayores a 499 Mb⚠️**")
              return
    elif mode == "upltu":
          if int(zips) > 249:
              await msg.edit("**⚠️UVS.LTU no Admite Archivos Mayores a 19 Mb⚠️**")
              return
    elif mode == "upgtm":
        if int(zips) > 7:
            await msg.edit("**⚠️GTM no Admite Archivos Mayores a 7 Mb⚠️**")
            return
	
    session = aiohttp.ClientSession(connector=connector)
    await msg.edit("`Comprobando Server`")
    filename = Path(file).name
    filesize = Path(file).stat().st_size
    zipssize = 1024*1024*int(zips)
    logerrors = 0
    error_conv = 0
    logslinks = []

    try:
        async with session.get(moodle,timeout=20,ssl=False) as resp:
            await resp.text()
            await msg.edit("**Server Online❗**")
    except Exception as ex:
        await msg.edit(f"{moodle} Caído 🔻:\n\n{ex}")
        return

    id_de_ms[username] = {"msg":msg, "pat":filename, "proc":"Up"}
    if filesize-1048>zipssize:
        parts = round(filesize / zipssize)
        await msg.edit(f"**Comprimiendo❗**")
        files = sevenzip(file,volume=zipssize)
       # await msg.edit("❗𝑪𝒐𝒎𝒑𝒓𝒐𝒃𝒂𝒏𝒅𝒐 𝒔𝒆𝒓𝒗𝒊𝒅𝒐𝒓")
        files = sevenzip(file,volume=zipssize)
        client = MoodleClient(usernamew,passwordw,moodle,connector)
        for path in files:
           while logerrors < 5:
                error_conv = 0
                try:
                    upload = await client.uploadtoken(path,lambda chunk,total,start,filen:uploadfile_progres(chunk,total,start,filen,msg),token)
                    if mode == "upltu" or mode == "upgtm" or mode == "upcmw":
                        upload = upload[1]
                        upload = upload.replace('draftfile.php/','webservice/draftfile.php/')
                        upload = str(upload) + '?token=' + token
                    else: 
                        upload = upload[0]
                    if upload == False:
                        await bot.send_message(usid,f"**Error Al Subir**")
                        id_de_ms[username]["proc"] = ""
                        return
                    else:pass
                 #   await bot.send_message(usid,f"__**{upload}**__",disable_web_page_preview=True)
                    logslinks.append(upload)
                    logerrors = 0
                    break
                except Exception as ex:
                    logerrors += 1
                    if logerrors > 4:
                        if "[400 MESSAGE_ID_INVALID]" in str(ex): pass
                    else:
                        await bot.send_message(usid,f"**Error Al Subir**:\n\n{ex}")
                    id_de_ms[username]["proc"] = ""
                    return
        if len(logslinks) == len(files):
            await msg.edit("**Subida Finalizada**✅")
            with open(filename+".txt","w") as f:
                message = ""
                lin = ""
                for li in logslinks:
                    message+=li+"\n"
                    lin+=li+"\n"
                f.write(message)				
            await msg.edit("**Enviando TxT📃**")				
            await bot.send_document(usid,filename+".txt",caption=f"**Archivo Subido🔺\nNombre: {filename}\nTamaño: {sizeof_fmt(filesize)}\n\nGracias Por Utilizar Nuestros Servicios ❤️**")
           # await msg.edit(f"**Archivo Subido🔺\nNombre: {filename}\nTamaño: {sizeof_fmt(filesize)}**")
            id_de_ms[username]["proc"] = "" 
        else:
            await msg.edit("**Error Al Subir**")
            id_de_ms[username]["proc"] = ""
            return 
#Subida si el Archivo no sobrepasa el tamaño Predeterminado 
    else:           
        client = MoodleClient(usernamew,passwordw,moodle,connector)
        while logerrors < 5:
            error_conv = 0
            try:
                upload = await client.uploadtoken(file,lambda chunk,total,start,filen:uploadfile_progres(chunk,total,start,filen,msg),token)
                if mode == "upltu" or mode == "upgtm" or mode == "upcmw":
                    upload = upload[1]
                    upload = upload.replace('draftfile.php/','webservice/draftfile.php/')
                    upload = str(upload) + '?token=' + token
                else: 
                    upload = upload[0]
                if upload == False:
                    await bot.send_message(usid,f"**Error Al Subir**")
                    id_de_ms[username]["proc"] = ""
                    return
                else:pass
              #  await bot.send_message(usid,f"__**{upload}**__",disable_web_page_preview=True)
                logslinks.append(upload)
                logerrors = 0
                break
            except Exception as ex:
                logerrors += 1
                if logerrors > 4:
                    if "[400 MESSAGE_ID_INVALID]" in str(ex): pass
                else:
                    await msg.edit(f"**Error Al Subir**:\n\n{ex}")
                id_de_ms[username]["proc"] = ""
                return
        if len(logslinks) == 1:
            await msg.edit("**Subida Finalizada**✅")
            with open(filename+".txt","w") as f:
                message = ""
                lin = ""
                for li in logslinks:
                    message+=li+"\n"
                    lin+=li+"\n"
                f.write(message)
            await msg.edit("**Enviando TxT📃**")				
            await bot.send_document(usid,filename+".txt",caption=f"**Archivo Subido🔺\nNombre: {filename}\nTamaño: {sizeof_fmt(filesize)}\n\nGracias Por Utilizar Nuestros Servicios ❤️**")
         #   await msg.edit(f"**Archivo Subido🔺\nNombre: {filename}\nTamaño: {sizeof_fmt(filesize)}**")
            id_de_ms[username]["proc"] = ""
        else:
            await msg.edit("**Error Al Subir**")
            id_de_ms[username]["proc"] = ""
            return

###Client Subdia
class MoodleClient:
    def __init__(self,username,password,moodle,proxy):
        self.url = moodle
        self.username = username
        self.password = password
        self.session = aiohttp.ClientSession(cookie_jar=aiohttp.CookieJar(unsafe=True),connector=proxy)
        self.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Mobile Safari/537.36"}
    async def uploadtoken(self,f,progress,token):
        url = self.url+"/webservice/upload.php"
        file = Progress(f,progress)
        query = {"token":token,"file":file}
        async with self.session.post(url,data=query,headers=self.headers,ssl=False) as response:
            text = await response.text()
        dat = loads(text)[0]
        url = self.url+"/draftfile.php/"+str(dat["contextid"])+"/user/draft/"+str(dat["itemid"])+"/"+str(quote(dat["filename"]))
        urlw = self.url+"/webservice/rest/server.php?moodlewsrestformat=json"
        query = {"formdata":f"name=Event&eventtype=user&timestart[day]=31&timestart[month]=9&timestart[year]=3786&timestart[hour]=00&timestart[minute]=00&description[text]={quote_plus(url)}&description[format]=1&description[itemid]={randint(100000000,999999999)}&location=&duration=0&repeat=0&id=0&userid={dat['userid']}&visible=1&instance=1&_qf__core_calendar_local_event_forms_create=1","moodlewssettingfilter":"true","moodlewssettingfileurl":"true","wsfunction":"core_calendar_submit_create_update_form","wstoken":token}
        async with self.session.post(urlw,data=query,headers=self.headers,ssl=False) as response:
            text = await response.text()
        try:
            a = findall("https?://[^\s\<\>]+[a-zA-z0-9]",loads(text)["event"]["description"])[-1].replace("pluginfile.php/","webservice/pluginfile.php/")+"?token="+token
            return a , url
        except:
            return url
class Progress(BufferedReader):
    def __init__(self, filename, read_callback):
        f = open(filename, "rb")
        self.filename = Path(filename).name
        self.__read_callback = read_callback
        super().__init__(raw=f)
        self.start = time()
        self.length = Path(filename).stat().st_size

    def read(self, size=None):
        calc_sz = size
        if not calc_sz:
            calc_sz = self.length - self.tell()
        self.__read_callback(self.tell(), self.length,self.start,self.filename)
        return super(Progress, self).read(size)
###Subida x Login
async def uploaddraft(file,usid,msg,username):
    user = Config[username]["username"]
    password = Config[username]["password"]
    host = Config[username]["host"]
    repoid = Config[username]["repoid"]
    zips = Configs[username]["z"]
    nub = Configs[username]["a"]
    if nub == "eduvirtual":
        proxy = ""
    else:
        proxy = Configs["gp"]
    if proxy == "":
        connector = None
    else:
        connector = proxy
    if proxy == "":
        connection = aiohttp.TCPConnector()
    else:
        connection = aiohttp_socks.ProxyConnector(ssl=False).from_url(f"{proxy}")
    session = aiohttp.ClientSession(connector=connection)
  #  await msg.edit("𝑹𝒆𝒄𝒐𝒑𝒊𝒍𝒂𝒏𝒅𝒐 𝒊𝒏𝒇𝒐𝒓𝒎𝒂𝒄𝒊ó𝒏")
    filename = Path(file).name
    filesize = Path(file).stat().st_size
    zipssize = 1024*1024*int(zips)
 #   await msg.edit("❗𝑪𝒐𝒎𝒑𝒓𝒐𝒃𝒂𝒏𝒅𝒐 𝒔𝒆𝒓𝒗𝒊𝒅𝒐𝒓")
    try:
        async with session.get(host,timeout=20,ssl=False) as resp:
            await resp.text()
            await msg.edit("**Server Online❗**")
    except Exception as ex:
        await msg.edit(f"{host} está Caído:\n\n{ex}")
        return
    id_de_ms[username] = {"msg":msg, "pat":filename, "proc":"Up"}
    if filesize > zipssize:
        await msg.edit("**Comprimiendo❗**")
        files = sevenzip(file,volume=zipssize)
        client = MoodleClient2(host,user,password,repoid,connector)
        links = []
        for file in files:
            try:
                upload = await client.LoginUpload(file,lambda size,total,start,filename: uploadfile_progres(size,total,start,filename,msg))
                await bot.send_message(usid,f"Enlace:\n**{upload}**")
                links.append(upload)
            except Exception as ex:
                if "[400 MESSAGE_ID_INVALID]" in str(ex): pass
                else:
                    await bot.send_message(usid,f"**Error Al Subir**:\n\n{ex}")
                id_de_ms[username]["proc"] = ""
                return
        message = ""
        for link in links:
            message+=f"{link}\n"
        await msg.edit("**Enviando TxT**")
        with open(filename+".txt","w") as txt:
            txt.write(message)
        await bot.send_document(usid,filename+".txt",caption="**Archivo Subido🔺\nNombre: {filename}\nTamaño: {sizeof_fmt(filesize)}\n\nGracias Por Utilizar Nuestros Servicios ❤️**")

        id_de_ms[username]["proc"] = ""
        os.unlink(filename+".txt")
        return
    
    else:
        client = MoodleClient2(host,user,password,repoid,connector)
        try:
            upload = await client.LoginUpload(file,lambda size,total,start,filename: uploadfile_progres(size,total,start,filename,msg))
            await msg.edit(f"__**{upload}**__")
            with open(filename+".txt","w") as txt:
                txt.write(upload)
            await bot.send_document(usid,filename+".txt",caption="**Archivo Subido🔺\nNombre: {filename}\nTamaño: {sizeof_fmt(filesize)}\n\nGracias Por Utilizar Nuestros Servicios ❤️**")
            id_de_ms[username]["proc"] = ""
            os.unlink(filename+".txt")
            return
        except Exception as ex:
            if "[400 MESSAGE_ID_INVALID]" in str(ex): pass
            else:
                await bot.send_message(usid,f"𝑬𝒓𝒓𝒐𝒓 𝒂𝒍 𝒔𝒖𝒃𝒊𝒓:\n\n{ex}")
            id_de_ms[username]["proc"] = ""
            return

bot.start()
bot.send_message(5416296262,'**BoT Iniciado**')
print("Iniciado")
bot.loop.run_forever()
