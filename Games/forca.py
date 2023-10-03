from discord.ext import commands
from Games.palavras import pick_word

class Forca(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        self.word = ''
        self.letters = []
        self.hp = 5


    @commands.command()
    #inicia um jogo de forca
    async def forca(self, ctx):

        if (self.word == ''):
            await ctx.send("Bem vindo(a) ao jogo da forca. Use !letra <letra> para chutar!")

            self.word = pick_word()

            self.word = self.word.rstrip()

            self.letters = ['*'] * len(self.word)

            self.word = list(self.word)
        
        else:
            await ctx.send("Já existe um jogo em andamento!")
        await ctx.send("Tente adivinhar qual é a palavra: ")
        await ctx.send(' '.join(self.letters))

    @commands.command()
    #inicia um jogo de forca
    async def letra(self, ctx, letter):
        if(self.word != ''):
            letter = letter.lower()
            #se a letra existe na palavra a ser adivinhada
            if (letter in self.word and letter not in self.letters):
                for c in range(len(self.word)):
                    if(self.word[c] == letter):
                        self.letters[c] = letter

                await ctx.send("Temos sim a letra {}".format(letter))
                await ctx.send(' '.join(self.letters))
            else:
                self.hp -=1
                await ctx.send("Não temos a letra {}".format(letter))
                await ctx.send("Você agora só tem {} vidas".format(self.hp))
    
            #fim de jogo
            if (not '*' in self.letters):
                await ctx.send("Você venceu! A palavra era {}".format(''.join(self.word)))
            elif(self.hp == 0):
                await ctx.send("Você não tem mais vidas :(")
                await ctx.send("A palavra era {}".format(''.join(self.word)))

                self.word = ''
                self.letters = []
                self.hp = 5

        else:
            await ctx.send("Não há um jogo em andamento, crie um com !forca")


async def setup(bot):
    await bot.add_cog(Forca(bot))
