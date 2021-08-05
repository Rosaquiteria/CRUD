from models import Carros, Usuario
import psycopg2.extras

SQL_DELETA_CARROS = 'delete from carro where id = %s'
SQL_CARRO_POR_ID = 'SELECT id, marca, modelo, cor, ano, combustivel from carro where id = %s'
SQL_USUARIO_POR_ID = 'SELECT id, nome, senha from usuario where id = %s'
SQL_ATUALIZA_CARROS = 'UPDATE Carro SET marca=%s, modelo=%s, ano=%s, cor=%s, combustivel=%s where id = %s'
SQL_BUSCA_CARROS = 'SELECT id, marca, modelo, cor, ano, combustivel from Carro'
SQL_CRIA_CARROS = 'INSERT into Carro (marca, modelo, cor, ano, combustivel) values (%s, %s, %s, %s,%s) RETURNING id'
SQL_CRIA_USUARIO = 'INSERT into usuario (id, nome, senha) values (%s, %s, %s)'
SQL_ATUALIZA_USUARIO = 'UPDATE usuario SET id=%s, nome=%s, senha=%s where id = %s'
SQL_AUTENTICAR_USUARIO = 'SELECT id, nome, senha from usuario where id = %s AND senha = %s'

class CarroDao:
    def __init__(self, db):
        self.__db=db

    def Salvar(self, carro):
        cursor= self.__db.cursor()
        if (carro.id):
            cursor.execute(SQL_ATUALIZA_CARROS, (carro.marca, carro.modelo, carro.cor, carro.ano, carro.combustivel, carro.id))
        else:
            cursor.execute(SQL_CRIA_CARROS, (carro.marca, carro.modelo, carro.cor, carro.ano, carro.combustivel))
            carro.id= cursor.fetchone()[0]
        self.__db.commit()
        cursor.close()
        return carro

    def Listar(self):
        cursor = self.__db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(SQL_BUSCA_CARROS)
        Carrodao= cursor.fetchall()
        return Carrodao

    def Buscar_por_id(self, id):
        cursor = self.__db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(SQL_CARRO_POR_ID, (id, ))
        tupla = cursor.fetchone()
        cursor.close()
        return Carros(tupla[1], tupla[2], tupla[3], tupla[4], tupla[5], id=tupla[0])

    def Excluir(self, id):
        cursor = self.__db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(SQL_DELETA_CARROS, (id, ))
        self.__db.commit()
        cursor.close()
class UsuarioDao:
    def __init__(self, db):
        self.__db= db
    def Buscar_por_id(self, id):
        cursor = self.__db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(SQL_USUARIO_POR_ID, (id,))
        dados = cursor.fetchone()
        usuario = traduz_usuario(dados) if dados else None
        return usuario

    def autenticar(self, id, senha):
        cursor = self.__db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(SQL_AUTENTICAR_USUARIO, (id, senha))
        dados = cursor.fetchone()
        usuario = traduz_usuario(dados) if dados else None
        return usuario

    def Salvar( self, usuario):
        cursor = self.__db.cursor()

        #if (usuario.id):
            # cursor.execute(SQL_ATUALIZA_USUARIO, (usuario.id, usuario.nome, usuario.senha))
        #else:
        cursor.execute(SQL_CRIA_USUARIO, (usuario.id, usuario.nome, usuario.senha))
        self.__db.commit()
        cursor.close()
        return usuario

def traduz_usuario(tupla):
    return Usuario(tupla[0], tupla[1], tupla[2])


def Traduz_Carros(Carros):
    def Criar_Carros_com_tupla(tupla):
        return Carros(tupla[1], tupla[2], tupla[3], tupla[4], tupla[5], id=tupla[0])
    return list(map(Criar_Carros_com_tupla, Carros))


