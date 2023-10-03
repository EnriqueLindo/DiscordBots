import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.members=True

client = commands.Bot(command_prefix='!', intents=intents)

cogs = ["Games.forca", "Games.perfil", "Games.spyfall"]



#Quando iniciar o bot
@client.event
async def on_ready():
    print('Logado como {0.user}'.format(client))

@client.event
async def on_member_join(member):
    channel = client.get_channel(1158762113888694385)
    await channel.send("Bem-vindo(a) ao servidor, {} :)".format(member.name))



async def load_extensions():
    for cog in cogs:
        await client.load_extension(cog)

async def main():
    f = open("../discordBotTokens.txt", "r")
    tokens = f.read().splitlines()
    f.close()

    async with client:
        await load_extensions()
        await client.start(tokens[0])

asyncio.run(main())