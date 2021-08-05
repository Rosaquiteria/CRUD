class Carros:
    def __init__(self, marca, modelo, cor, ano, combustivel , id= None ):
        self.marca= marca
        self.modelo= modelo
        self.cor= cor
        self.ano= ano
        self.combustivel= combustivel
        self.id = id

class Usuario:
    def __init__(self, id, nome, senha):
        self.id= id
        self.nome= nome
        self.senha= senha
