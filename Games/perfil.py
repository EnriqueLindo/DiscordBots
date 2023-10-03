from discord.ext import commands
import discord
from Games.perfil6 import pickCard

class Perfil(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

        self.runningCard = False
        self.cardOwner = None

    @commands.command()
    async def perfil(self, ctx):
        if not self.runningCard:
            user = ctx.author.id

            self.cardOwner = user
            self.runningCard = True

            user = await self.bot.fetch_user(user)

            typ, name, quest = pickCard()

            await ctx.send("Quer uma cartinha? Tá na mão amigão")

            await user.send("=======================\nEu sou {}.\nDiga aos outros que sou um {}.".format(name, typ))

            await user.send('\n'.join(quest))
        else:
            await ctx.send("Já existe uma carta em andamento, o dono é <@{}>".format(self.cardOwner))

    @commands.command()
    async def perfilWin(self, ctx, winner:discord.Member, points):
        if self.runningCard:
            if ctx.author.id == self.cardOwner:
                await ctx.send("Dei {} pontos a <@{}> !".format(points, winner.id))
                self.runningCard = False
            else:
                await ctx.send("Você não pode dar a pontuação pois não é o dono da carta!")
        else:
            await ctx.send("Não existe uma carta em andamento, pegue uma com !perfil")


async def setup(bot):
    await bot.add_cog(Perfil(bot))