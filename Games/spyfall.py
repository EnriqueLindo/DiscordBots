import random
from discord.ext import commands
import discord
import Games.spyLocations as sp

class SpyFall(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

        self.spyfalling = False
        self.spyfallPlaying = False
        self.players = []
        self.voters = []
        self.guess = []
        self.location = None
        self.spy = 0

    @commands.command()
    async def spyRules(self, ctx):
        await ctx.send("Spyfall é um jogo cujo objetivo é descobrir qual dos jogadores é o espião.\n\n" +
        "Ao iniciar um jogo, 1 jogador será escolhido para ser o espião e os outros jogadores receberão " + 
        "um local e sua profissão.\n\nO jogo começa com uma pessoa fazendo uma pergunta à outra, afim de "+
        "descobrir se aquela pessoa é ou não o espião.\n\nO jogo tem um tempo limite de 8 minutos e após isso "+
        "todos devem votar em quem eles acham que é o espião.\n\nApós todos os votos serem contabilizados, o espião "+
        "é revelado.\n\nse os jogadores votaram na pessoa errada o espião vence. Porém, se os jogadores votaram na pessoa "+
        "certa, o espião ainda tem uma chance de ganhar o jogo tentando descobrir em que local eles se encontram. Se ele "+
        "acertar, ele vence. Bom jogo :)")

    @commands.command()
    async def spyfall(self, ctx):
        if not self.spyfalling:
            self.spyfalling = True
            
            await ctx.send("Começando um jogo de spyfall!\n Para participar use !spyJoin, para iniciar o jogo use !spyStart")

        else:
            await ctx.send("Já existe um jogo em andamento!")

    @commands.command()
    async def spyJoin(self, ctx):
        if self.spyfalling and not self.spyfallPlaying:
            id = ctx.author.id
            if id not in self.players:
                self.players.append(id)
                await ctx.send("<@{}> entrou no jogo!".format(id))
            else:
                await ctx.send("<@{}> já está participando do jogo!".format(id))
        elif self.spyfallPlaying:
            await ctx.send("Já existe um jogo em andamento, espere ele acabar.")
        else:
            await ctx.send("Não existe um jogo em andamento, crie um com !spyfall")

    @commands.command()
    async def spyLeave(self, ctx):
        if not self.spyfallPlaying:
            id = ctx.author.id
            if id in self.players:
                self.players.remove(id)
                await ctx.send("<@{}> saiu do jogo".format(id))
            else:
                await ctx.send("<@{}> não está participando do jogo".format(id))
        else:
            await ctx.send("O jogo está em andamento, você não pode sair agora.")

    @commands.command()
    async def spyGuess(self, ctx, g:discord.Member):
        if self.spyfalling:
            id = g.id
            voter = ctx.author.id
            if id in self.players and voter not in self.voters:
                self.guess.append(id)
                self.voters.append(voter)

                await ctx.send("<@{}> seu voto foi computado!".format(voter))

                #Verificando se todo mundo votou, se sim termina o jogo
                if len(self.voters) == len(self.players):
                    await ctx.send("Todos votaram! Computando os votos: ")

                    mostVoted = []
                    numVotes = 0

                    for c in self.players:
                        n = self.guess.count(c)
                        if n > numVotes:
                            #Atualizando o num de votos
                            numVotes = n

                            #Limpando a lista
                            mostVoted = []
                            mostVoted.append(c)

                        elif n == numVotes:
                            mostVoted.append(c)

                    if (len(mostVoted) == 1):
                        await ctx.send("O mais votado foi <@{}>".format(mostVoted[0]))
                        #Se acertaram ou erraram
                        if (mostVoted[0] == self.spy):
                            await ctx.send("Os inocentes acertaram! <@{}> era de fato o espião :spy:!".format(self.spy))
                            await ctx.send("Para o espião sair dessa furada ele deve adivinhar o local em que os inocentes estão!")
                            await ctx.send("Use !spyReveal para mostrar o local e terminar o jogo.")

                        else:
                            await ctx.send("Os inocentes erraram :( O espião era <@{}>".format(self.spy))
                            await self.spyReveal(ctx)

                    else:
                        await(ctx.send("Os votos não chegaram a um consenso, portanto o espião vence!"))
                        await ctx.send("O espião era :spy: <@{}>".format(self.spy))
                        await self.spyReveal(ctx)

            elif voter in self.voters:
                await ctx.send("Não se pode votar mais de uma vez!")
            else:
                await ctx.send("<@{}> não está participando do jogo".format(id))
        else:
            await ctx.send("Não existe um jogo em andamento, crie um com !spyfall")

    @commands.command()
    async def spyReveal(self, ctx):
        if self.spyfalling:
            self.spyfalling = False
            self.spyfallPlaying = False
            
            await ctx.send("O local era: {}".format(self.location))
            await ctx.send("Obrigado por jogar :D")

            self.guess = []
            self.voters = []
            self.location = None
            self.spy = 0
        else:
            await ctx.send("Não existe um jogo em andamento!")

    @commands.command()
    async def spyStart(self, ctx):
        if self.spyfalling and len(self.players) >= 3:
            self.spyfallPlaying = True
            #Selecionando o spy
            spyIndex = random.randint(0, len(self.players)-1)
            self.spy = self.players[spyIndex]
            spyUser = await self.bot.fetch_user(self.players[spyIndex])
            await spyUser.send("======================= \nVocê é o espião! :spy:\nLista de locais: ")
            await spyUser.send(sp.locations)

            #Selecionando o local e as profissoes dos outros jogadores
            self.location = sp.chooseLocation()

            for c in range(len(self.players)):
                if c != spyIndex:
                    user = await self.bot.fetch_user(self.players[c])

                    await user.send("=======================")
                    await user.send("Você é um inocente. O local é: {}. Seu trabalho é {}".format(self.location, sp.chooseJob(self.location)))

            await ctx.send("O jogo começou!\nAcione cronômetro de 8 minutos :alarm_clock:.")
            await ctx.send("Quando o tempo acabar, vote em quem você acha que é o espião usando !spyGuess @NomeDaPessoa")
            await ctx.send("<@{}> começa fazendo as perguntas.".format(random.choice(self.players)))

            
        elif not self.spyfalling:
            await ctx.send("Não existe um jogo em andamento, crie um com !spyfall")

        elif len(self.players) < 3:
            await ctx.send("Não existem players o suficiente!")

async def setup(bot):
    await bot.add_cog(SpyFall(bot))
