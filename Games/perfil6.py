import random
import os

types = ["animal", "lugar", "personagem", "coisa", "pessoa"]

possibleChoices = {"animal" : [], "lugar" : [], "personagem" : [], "coisa" : [], "pessoa" : []}

def pickCard():
    global possibleChoices

    name = ''
    questions = []

    ty = random.choice(types)

    f = open(os.getcwd()+"/Perfil/"+ty+".txt", "r", encoding="utf8")

    #Pegando a quantidade de objetos no arquivo
    size = int(f.readline())

    if possibleChoices[ty] == []:
        for c in range(size):
            possibleChoices[ty].append(c)

    num = random.choice(possibleChoices[ty])
    possibleChoices[ty].remove(num)

    #Achando a linha em que o objeto começa
    num *= 21

    #Navega até a linha do objeto
    for c in range(num):
        prov = f.readline()

    #Lê o nome do objeto
    name = f.readline()

    #Lê as 20 questões
    for c in range(20):
        questions.append(str(c+1) + "- " + f.readline())

    #Fecha o arquivo txt
    f.close()

    #Retorna o tipo, nome e as questoes
    return ty, name, questions
