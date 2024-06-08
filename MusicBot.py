import discord
from discord.ext import commands, tasks
from discord.ext.commands.core import after_invoke
import musicPlayer as mp

intents = discord.Intents.default()
intents.message_content = True
intents.members=True

client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print('Logado como {0.user}'.format(client))
    updateQueue.start()
    timeoutLeave.start()

musicQueue = []
musicChannel = None
timedOut = False

async def nextSong():
    global musicQueue, musicChannel

    ctx = musicChannel    

    if ctx != None and musicQueue != []:
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        if not voice.is_playing():

            music = musicQueue.pop(0)

            embed = discord.Embed(
                colour=discord.Colour.green(),
                title = "Atualmente tocando:",
                description = f"{music[1]}\n\nCortesia de <@{music[3]}>",
            )
            
            embed.set_thumbnail(url=music[2])
            
            await ctx.send(embed=embed)
            
            ctx.voice_client.play(music[0])

        else:
            pass

#Plays music
@client.command()
async def play(ctx, *, Music):
    global musicQueue, musicChannel, timedOut

    #Connecting to a voice channel
    if ctx.voice_client == None:
        try:
            channel = ctx.author.voice.channel
            await channel.connect()
        except:
            await ctx.send("Você não está conectado a nenhum canal de voz!")
            return
    
    #Checking if it is a name or a url
    link = Music.split(":")
    url = ''
    if link[0] == "https":
        url = Music
    else:
        try:
            url = await mp.Youtube.FindVideo(Music)
        except:
            await ctx.send("Verifique se o título da música não possui acentos e tente novamente.")

    await ctx.message.delete()

    #Extracting the audio
    data = await mp.Youtube.ExtractAudio(url)

    #Actually playing or adding to queue
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    musicQueue.append([data[0], data[1], data[2], ctx.author.id])
    timedOut = False
    if not voice.is_playing():
        musicChannel = ctx
        await nextSong()
    else:
        embed = discord.Embed(
            title = f"Música adicionada à fila!",
            description = f"A pedido de <@{ctx.author.id}>, teremos {data[1]}",
        )
        
        embed.set_thumbnail(url=data[2])
        
        await ctx.send(embed=embed)

@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("Não estou conectado a nenhum canal")

@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Ta maluco? Não tem nada tocando!")

@client.command()
async def unpause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()    
    else:
        await ctx.send("Ta surdo? Já tá tocando!")

@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()

@client.command()
async def next(ctx):
    await stop(ctx)
    await nextSong()

@client.command()
async def comandos(ctx):
    if ctx.channel.id == 1244791679257415691:
        await ctx.send("Lista de comandos: \n!play <NomeDaMusica ou URL> -> Reproduz a música escolhida ou adiciona na fila se uma já estiver tocando" +
                    "\n\n!pause -> Pausa a música que está tocando \n\n!unpause -> Despausa a música \n\n!stop -> Para de reproduzir áudio \n\n!next -> Passa para a próxima música" +
                    "\n\n!leave -> Faz o bot sair do canal de voz")

@tasks.loop(seconds=10)
async def updateQueue():
    await nextSong()

@tasks.loop(seconds=60)
async def timeoutLeave():
    global timedOut, musicQueue, musicChannel

    voice = discord.utils.get(client.voice_clients)
    if timedOut and musicChannel != None: # Se tava preparado pra sair e a lista ta vazia
        await musicChannel.voice_client.disconnect()
        musicChannel = None
    
    if voice != None:
        if musicQueue == [] and not voice.is_playing(): # Se a lista estiver vazia e não estiver tocando nada
            timedOut = True # Se prepara pra sair


    

#Escondendo o token
f = open("C:/Users/enriq/Documents/auth_disc.txt", "r")
tokens = f.read().splitlines()
f.close()

client.run(tokens[0])
