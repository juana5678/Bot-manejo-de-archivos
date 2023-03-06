@bot.on_message(filters.command("deleteall", prefixes="/")& filters.private)
async def delete_all(client: Client, message: Message):
    username = message.from_user.username
    send = message.reply
    try:await get_messages()
    except:await send_config()
    if acceso(username) == False:
        await send("⛔ 𝑵𝒐 𝒕𝒊𝒆𝒏𝒆 𝒂𝒄𝒄𝒆𝒔𝒐")
        return
    else:pass
    shutil.rmtree("downloads/"+username+"/")
    root[username]["actual_root"] = "downloads/"+username
    msg = files_formatter(str(root[username]["actual_root"])+"/",username)
    await limite_msg(msg[0],username)

@bot.on_message(filters.command("up", prefixes="/") & filters.private)
async def up(client: Client, message: Message):	
    username = message.from_user.username
    send = message.reply
    user_id = message.from_user.id
    try:await get_messages()
    except:await send_config()
    if acceso(username) == False:
        await send("⛔ 𝑵𝒐 𝒕𝒊𝒆𝒏𝒆 𝒂𝒄𝒄𝒆𝒔𝒐")
        return
    else:pass
    if username not in boss and Configs["s"] == "Off":
        await client.send_message(username,'⛔𝑬𝒔𝒕𝒂 𝒇𝒖𝒏𝒄𝒊𝒐𝒏 𝒆𝒔𝒕𝒂 𝒂𝒑𝒂𝒈𝒂𝒅𝒂')
        return
    else: pass	
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
    list = message.text.split("_")[1]		
    msgh = files_formatter(str(root[username]["actual_root"]),username)
    try:
        path = str(root[username]["actual_root"]+"/")+msgh[1][list]
        msg = await send(f"Archivo 📂: {path}**")
        if Configs[username]["m"] == "u": 
            fd = await uploadfile(path,user_id,msg,username)
        elif Configs[username]["m"] == "e":
              if len(Urls[username]) >= 10  and username not in boss:
                  await msg.edit('⛔️ 𝑬𝒍 𝒍𝒊𝒎𝒊𝒕𝒆 𝒅𝒆 𝒍𝒊𝒏𝒌𝒔 𝒇𝒖𝒆 𝒑𝒂𝒔𝒂𝒅𝒐 , 𝒖𝒕𝒊𝒍𝒊𝒛𝒆 **/deletelinks**')
                  return
              else:
                  await uploadfileapi(path,user_id,msg,username)
        elif Configs[username]["m"] == "n":
	    await proccess(path,msg,username)
        else:
            await uploaddraft(path,user_id,msg,username)
    except Exception as ex:
        await send(ex)
