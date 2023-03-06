async def uploadfile(file,usid,msg,username):
    proxy = Configs["pproxy"]
    mode = Configs[username]["updl"]
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
    await msg.edit("𝑹𝒆𝒄𝒐𝒑𝒊𝒍𝒂𝒏𝒅𝒐 𝒊𝒏𝒇𝒐𝒓𝒎𝒂𝒄𝒊ó𝒏")
    filename = Path(file).name
    filesize = Path(file).stat().st_size
    zipssize = 1024*1024*int(zips)
    logerrors = 0
    error_conv = 0
    logslinks = []

    try:
        async with session.get(moodle,timeout=20,ssl=False) as resp:
            await resp.text()
            await msg.edit("𝑺𝒆𝒓𝒗𝒊𝒅𝒐𝒓 𝑶𝒏𝒍𝒊𝒏𝒆 ✔")
    except Exception as ex:
        await msg.edit(f"{moodle} is Down:\n\n{ex}")
        return

    id_de_ms[username] = {"msg":msg, "pat":filename, "proc":"Up"}
