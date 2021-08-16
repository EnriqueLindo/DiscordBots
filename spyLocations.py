import random

locations = ["Avião", "Escola", "Oficina de Carro", "Banco", "Supermercado",
            "Hospital", "Hotel", "Submarino", "Navio Pirata", "Circo",
            "Teatro", "Delegacia", "Restaurante", "Boate", "Estação Espacial",
            "Parque de Diversões", "Base Militar", "Museu", "Biblioteca", "Zoológico"]

jobs = {"Avião" : ["Piloto", "Co-Piloto", "Aeromoça", "Passageiro"],
        "Escola" : ["Professor", "Diretor", "Aluno", "Zelador"],
        "Oficina de Carro" : ["Mecânico", "Cliente", "Gerente"],
        "Banco" : ["Gerente", "Cliente", "Ladrão", "Recepcionista"],
        "Supermercado" : ["Caixa", "Gerente", "Cliente", "Açougueiro"],
        "Hospital" : ["Médico", "Enfermeira", "Paciente", "Recepcionista"],
        "Hotel" : ["Porteiro", "Hóspede", "Gerente", "Recepcionista"],
        "Submarino" : ["Capitão", "Cozinheiro", "Tripulante", "Escrivão"],
        "Navio Pirata" : ["Capitão", "Prisioneiro", "Cozinheiro", "Músico"],
        "Circo" : ["Palhaço", "Acrobata", "Mágico", "Adestrador de Animais"],
        "Teatro" : ["Ator", "Músico", "Diretor", "Suporte Tecnico"],
        "Delegacia" : ["Policial", "Detento", "Detetive", "Sargento"],
        "Restaurante" : ["Garçom", "Cliente", "Recepcionista", "Cheff"],
        "Boate" : ["Stripper", "Barman", "Dançarino", "Segurança"],
        "Estação Espacial" : ["Astronauta", "Alienígena", "Técnico"],
        "Parque de Diversões" : ["Cliente", "Funcionário de uma Atração", "Zelador", "Dono de uma loja de lanches"],
        "Base Militar" : ["General", "Soldado", "Visitante", "Sargento"],
        "Museu" : ["Guia", "Turista", "Ladrão de arte", "Artista"],
        "Biblioteca" : ["Bibliotecario", "Estudante", "Pesquisador"],
        "Zoológico" : ["Zelador", "Cuidador", "Gerente", "Turista"]}

def chooseLocation():
    return random.choice(locations)

def chooseJob(location):
    return random.choice(jobs[location])
