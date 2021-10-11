import discord
from discord.ext import commands, tasks
from discord.ext.commands.core import after_invoke
import musicPlayer as mp

client = commands.Bot(command_prefix='!', description="IlarilarilarieOOO")

@client.event
async def on_ready():
    print('Logado como {0.user}'.format(client))

musicQueue = []
musicChannel = []

async def nextSong():
    global musicQueue, musicChannel

    ctx = musicChannel    

    if ctx != [] and musicQueue != []:
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        if not voice.is_playing():

            music = musicQueue.pop(0)
            
            await ctx.send("Tocando {}".format(music[1]))
            ctx.voice_client.play(music[0])

        else:
            pass

#Plays music
@client.command()
async def play(ctx, *,Music):
    global musicQueue, musicChannel

    #Connecting to a voice channel
    if ctx.voice_client == None:
        try:
            await ctx.author.voice.channel.connect()
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


    #Extracting the audio
    data = await mp.Youtube.ExtractAudio(url)

    #Actually playing or adding to queue
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    musicQueue.append([data[0], data[1]])
    if not voice.is_playing():
        musicChannel = ctx
        await nextSong()
    else:
        await ctx.send("Música adicionada à fila!")

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
    if ctx.channel.id == 864553084956049418:
        await ctx.send("Lista de comandos: \n!play <NomeDaMusica ou URL> -> Reproduz a música escolhida ou adiciona na fila se uma já estiver tocando" +
                    "\n\n!pause -> Pausa a música que está tocando \n\n!unpause -> Despausa a música \n\n!stop -> Para de reproduzir áudio \n\n!next -> Passa para a próxima música" +
                    "\n\n!leave -> Faz o bot sair do canal de voz")

@tasks.loop(seconds=10)
async def updateQueue():
    await nextSong()


updateQueue.start()

#Escondendo o token
f = open("C:/Users/Thomaz/Desktop/F/PythonProjects/discordBotTokens.txt", "r")
tokens = f.read().splitlines()
f.close()

client.run(tokens[1])
