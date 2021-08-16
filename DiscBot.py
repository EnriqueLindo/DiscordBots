import discord
from discord.ext import commands
import random
import spyLocations as sp
import perfil6

client = commands.Bot(command_prefix='!', description="IlarilarilarieOOO")

#Quando iniciar o bot
@client.event
async def on_ready():
    print('Logado como {0.user}'.format(client))

#Scanner de mensagens
palavras_tristes = ['triste', 'depressão', 'depressivo', 'depressao']

@client.listen()
async def on_message(message):
    if message.author == client.user:
        return    

    if any(word in message.content for word in palavras_tristes):
        await message.channel.send("Tem alguem triste aqui? Toma uma mamada glub glub")

#Comandos

#00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
#Parte do jogo da forca

guessingWord = ''
lettersGuessed = []
hp = 5

@client.command()
#inicia um jogo de forca
async def forca(ctx):
    global guessingWord, lettersGuessed

    if (guessingWord == ''):
        await ctx.send("Bem vindo(a) ao jogo da forca. Use !letra <letra> para chutar!")
        f = open("palavras.txt", "r")
        n = random.randrange(106)

        for i in range(n):
            guessingWord = f.readline()

        f.close()

        guessingWord = guessingWord.rstrip()

        lettersGuessed = ['*'] * len(guessingWord)

        guessingWord = list(guessingWord)
     
    else:
        await ctx.send("Já existe um jogo em andamento!")
    await ctx.send("Tente adivinhar qual é a palavra: ")
    await ctx.send(' '.join(lettersGuessed))

@client.command()
#inicia um jogo de forca
async def letra(ctx, letter):
    global hp, guessingWord, lettersGuessed
    if(guessingWord != ''):
        letter = letter.lower()
        #se a letra existe na palavra a ser adivinhada
        if (letter in guessingWord and letter not in lettersGuessed):
            for c in range(len(guessingWord)):
                if(guessingWord[c] == letter):
                    lettersGuessed[c] = letter

            await ctx.send("Temos sim a letra {}".format(letter))
            await ctx.send(' '.join(lettersGuessed))
        else:
            hp -=1
            await ctx.send("Não temos a letra {}".format(letter))
            await ctx.send("Você agora só tem {} vidas".format(hp))
 
        #fim de jogo
        if (not '*' in lettersGuessed):
            await ctx.send("Você venceu! A palavra era {}".format(''.join(guessingWord)))
        elif(hp == 0):
            await ctx.send("Você não tem mais vidas :(")
            await ctx.send("A palavra era {}".format(''.join(guessingWord)))

            guessingWord = ''
            lettersGuessed = []
            hp = 5

    else:
        await ctx.send("Não há um jogo em andamento, crie um com !forca")


#00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
#Parte do tictactoe

player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

@client.command()
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    global count
    global player1
    global player2
    global turn
    global gameOver

    if gameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0

        player1 = p1
        player2 = p2

        # print the board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        # determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send("É turno de <@" + str(player1.id) + ">.")
        elif num == 2:
            turn = player2
            await ctx.send("É turno de <@" + str(player2.id) + ">.")
    else:
        await ctx.send("Já existe um jogo em andamento!")

@client.command()
async def place(ctx, pos: int):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
                board[pos - 1] = mark
                count += 1

                # print the board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                print(count)
                if gameOver == True:
                    await ctx.send(mark + " venceu!")
                elif count >= 9:
                    gameOver = True
                    await ctx.send("Empatou!")

                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                await ctx.send("Escolha um número e um espaço válido.")
        else:
            await ctx.send("Não é seu turno :P")
    else:
        await ctx.send("Não há um jogo em progresso, comece um com !tictactoe")

def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

@tictactoe.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Mencione 2 usuários no comando!")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Certifique-se de mencionar um usuário")

@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Digite no comando a posição que deseja marcar")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Use um numero de 1 a 9.")

#00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
#Parte do spyfall

spyfalling = False
spyfallPlaying = False
players = []
voters = []
guess = []
location = None
spy = 0

@client.command()
async def spyRules(ctx):
    await ctx.send("Spyfall é um jogo cujo objetivo é descobrir qual dos jogadores é o espião.\n" +
     "Ao iniciar um jogo 1 jogador será escolhido para ser o espião, e os outros jogadores receberão " + 
     "um local e sua profissão. O jogo começa com uma pessoa fazendo uma pergunta a outra, afim de "+
     "descobrir se aquela pessoa é ou não o espião. O jogo tem um tempo limite de 8 minutos e após isso "+
     "todos devem votar em quem eles acham que é o espião. Após todos os votos serem contabilizados o espião "+
     "é revelado, se os jogadores votaram na pessoa errada o espião vence. Porém, se os jogadores votaram na pessoa "+
     "certa, o espião ainda tem uma chance de ganhar o jogo tentando descobrir em que local eles se encontram, se ele "+
     "acertar, ele vence.")

@client.command()
async def spyfall(ctx):
    global spyfalling

    if not spyfalling:
        spyfalling = True
        
        await ctx.send("Começando um jogo de spyfall!\n Para participar use !spyJoin, para iniciar o jogo use !spyStart")

    else:
        await ctx.send("Já existe um jogo em andamento!")

@client.command()
async def spyJoin(ctx):
    global players

    if spyfalling and not spyfallPlaying:
        id = ctx.author.id
        if id not in players:
            players.append(id)
            await ctx.send("<@{}> entrou no jogo!".format(id))
        else:
            await ctx.send("<@{}> já está participando do jogo!".format(id))
    elif spyfallPlaying:
        await ctx.send("Já existe um jogo em andamento, espere ele acabar.")
    else:
        await ctx.send("Não existe um jogo em andamento, crie um com !spyfall")

@client.command()
async def spyLeave(ctx):
    global players

    #alterei
    if not spyfallPlaying:
        id = ctx.author.id
        if id in players:
            players.remove(id)
            await ctx.send("<@{}> saiu do jogo".format(id))
        else:
            await ctx.send("<@{}> não está participando do jogo".format(id))
    else:
        await ctx.send("O jogo está em andamento, você não pode sair agora.")

@client.command()
async def spyGuess(ctx, g:discord.Member):
    global guess, voters
    if spyfalling:
        id = g.id
        voter = ctx.author.id
        if id in players and voter not in voters:
            guess.append(id)
            voters.append(voter)

            await ctx.send("<@{}> seu voto foi computado!".format(voter))

            #Verificando se todo mundo votou, se sim termina o jogo
            if len(voters) == len(players):
                await ctx.send("Todos votaram! Computando os votos: ")

                mostVoted = []
                numVotes = 0

                for c in players:
                    n = guess.count(c)
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
                    if (mostVoted[0] == spy):
                        await ctx.send("Os inocentes acertaram! <@{}> era de fato o espião :spy:!".format(spy))
                        await ctx.send("Para o espião sair dessa furada ele deve adivinhar o local em que os inocentes estão!")
                        await ctx.send("Use !spreveal para mostart o local e terminar o jogo.")

                    else:
                        await ctx.send("Os inocentes erraram :( O espião era <@{}>".format(spy))
                        await spyReveal(ctx)

                else:
                    await(ctx.send("Os votos não chegaram a um consenso, portanto o espião vence!"))
                    await ctx.send("O espião era :spy: <@{}>".format(spy))
                    await spyReveal(ctx)

        elif voter in voters:
            await ctx.send("Não se pode votar mais de uma vez!")
        else:
            await ctx.send("<@{}> não está participando do jogo".format(id))
    else:
        await ctx.send("Não existe um jogo em andamento, crie um com !spyfall")

@client.command()
async def spyReveal(ctx):
    global spyfalling, players, guess, spyfallPlaying, location, voters, spy

    if spyfalling:
        spyfalling = False
        spyfallPlaying = False
        
        await ctx.send("O local era: {}".format(location))
        await ctx.send("Obrigado por jogar :D")

        guess = []
        voters = []
        location = None
        spy = 0

    else:
        await ctx.send("Não existe um jogo em andamento!")

@client.command()
async def spyStart(ctx):
    global location, spy, spyfallPlaying

    if spyfalling and len(players) >= 2:
        spyfallPlaying = True
        #Selecionando o spy
        spyIndex = random.randint(0, len(players)-1)
        spy = players[spyIndex]
        spyUser = await client.fetch_user(players[spyIndex])
        await spyUser.send("======================= \nVocê é o espião! :spy:\nLista de locais: ")
        await spyUser.send(sp.locations)

        #Selecionando o local e as profissoes dos outros jogadores
        location = sp.chooseLocation()

        for c in range(len(players)):
            if c != spyIndex:
                user = await client.fetch_user(players[c])

                await user.send("=======================")
                await user.send("Você é um inocente. O local é: {}. Seu trabalho é {}".format(location, sp.chooseJob(location)))

        await ctx.send("O jogo começou!\nAcione cronômetro de 6 minutos :alarm_clock:.")
        await ctx.send("Quando o tempo acabar, vote em quem você acha que é o espião usando !spguess @NomeDaPessoa")
        await ctx.send("<@{}> começa fazendo as perguntas.".format(random.choice(players)))

        #Relógio
        '''
        t60 = False #1 min
        t120 = False #2 min
        t180 = False #3 min
        t240 = False #4 min
        t300 = False #5 min
        t360 = False #6 min

        currTime = time.time()
        while time.time() - currTime <= 360:
            t = time.time() - currTime
            
            if t >= 360 and not t360:
                t360 = True
                await ctx.send(":alarm_clock: Já se passaram 6 minutos :alarm_clock:")
            elif t >= 300 and not t300:
                t300 = True
                await ctx.send(":alarm_clock: Já se passaram 5 minutos :alarm_clock:")
            elif t >= 240 and not t240:
                t240 = True
                await ctx.send(":alarm_clock: Já se passaram 4 minutos :alarm_clock:")
            elif t >= 180 and not t180:
                t180 = True
                await ctx.send(":alarm_clock: Já se passaram 3 minutos :alarm_clock:")
            elif t >= 120 and not t120:
                t120 = True
                await ctx.send(":alarm_clock: Já se passaram 2 minutos :alarm_clock:")
            elif t >= 60 and not t60:
                t60 = True
                await ctx.send(":alarm_clock: Já se passou 1 minuto    :alarm_clock:")

        await ctx.send("Acabou o tempo, vote em quem você acha que é o espião usando !spguess @NomeDaPessoa")
        '''
    elif not spyfalling:
        await ctx.send("Não existe um jogo em andamento, crie um com !spyfall")

    elif len(players) < 4:
        await ctx.send("Não existem players o suficiente!")

#00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
#Parte do perfil

runningCard = False
cardOwner = None

@client.command()
async def perfil(ctx):
    global runningCard, cardOwner

    if not runningCard:
        user = ctx.author.id

        cardOwner = user
        #runningCard = True

        user = await client.fetch_user(user)

        typ, name, quest = perfil6.pickCard()

        await ctx.send("Quer uma cartinha? Tá na mão amigão")

        await user.send("=======================\nEu sou {}.\nDiga aos outros que sou um {}.".format(name, typ))

        await user.send('\n'.join(quest))
    else:
        await ctx.send("Já existe uma carta em andamento, o dono é <@{}>".format(cardOwner))

@client.command()
async def perfilWin(ctx, winner:discord.Member, points):
    global runningCard, cardOwner

    if runningCard:
        if ctx.author.id == cardOwner:
            await ctx.send("Dei {} pontos a <@{}> !".format(points, winner.id))
            runningCard = False
        else:
            await ctx.send("Você não pode dar a pontuação pois não é o dono da carta!")
    else:
        await ctx.send("Não existe uma carta em andamento, pegue uma com !perfil")


@client.command()
async def comandos(ctx):
    if ctx.channel.id != 864553084956049418:
        await ctx.send("Lista de comandos: \n!forca -> Inicia um Jogo da Forca \n\n!perfil -> Inicia um jogo de Perfil \n\n!spyfall -> inicia um jogo de Spyfall " +
                       "\n\n!tictactoe <@Player1> <@Player2> -> inicia um Jogo da Velha")


@client.command()
async def teste(ctx):
    if ctx.channel.id == ctx.author.dm_channel.id:
        await ctx.send("Testado!")

#Escondendo o token
f = open("C:/Users/Thomaz/Desktop/F/PythonProjects/discordBotTokens.txt", "r")
tokens = f.read().splitlines()
f.close()

client.run(tokens[0])

#ODY3NDQzMDU3OTgwNjA0NDQ2.YPhLTQ.lefMXmapF6TNPSkG4XxSAuyaFJk
#ODYwOTI0NDUxNDM2ODg4MDc2.YOCUYA.1uEesI6_HaQEcbucSpy3dhwT_fo
