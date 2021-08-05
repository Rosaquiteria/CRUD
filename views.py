from flask import render_template, request, redirect, session, flash, url_for
from carroCrud import app, db
from dao import CarroDao, UsuarioDao


carro_dao= CarroDao(db)
usuario_dao= UsuarioDao(db)

from models import Carros

@app.route('/')
def index():
    carros = carro_dao.Listar()
    return render_template('lista.html', titulo='Carros', carros=carros)


@app.route('/formulario')
def formulario():
    if 'usuario_logado' not in session or session['usuario_logado']== None:
        return redirect(url_for('login', proxima=url_for('formulario')))
    return render_template('formulario.html', titulo='Novo Carro')

@app.route('/criar', methods=['post',])
def criar():
    marca=request.form['f_marca']
    modelo = request.form['f_modelo']
    cor = request.form['f_cor']
    ano = request.form['f_ano']
    combustivel = request.form['f_combu']
    carro= Carros(marca, modelo, cor, ano, combustivel)
    carros= carro_dao.Salvar(carro)
    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', titulo='login', proxima=proxima)

@app.route('/autenticar', methods=['post',])
def autenticar():
    usuario = usuario_dao.autenticar(request.form['f_usuario'], request.form['f_senha'])
    if usuario:
        session['usuario_logado']=usuario.id
        flash(usuario.nome + 'Logado com Sucesso')
        proxima_pagina= request.form['proxima']
        return redirect(proxima_pagina)

    else:
        flash('Incorreto! tente novamente.')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum Usuário Logado')
    return redirect(url_for('index'))

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado']== None:
        return redirect(url_for('login', proxima=url_for('editar', id=id)))
    carro=carro_dao.Buscar_por_id(id)
    return render_template('editar.html', titulo='Editar Carro', carro=carro)

@app.route('/atualizar', methods=['post', ])
def atualizar():
    marca=request.form['f_marca']
    modelo = request.form['f_modelo']
    cor = request.form['f_cor']
    ano = request.form['f_ano']
    combustivel = request.form['f_combu']
    id= request.form['id']
    carro= Carros(marca, modelo, cor, ano, combustivel, id)
    carro_dao.Salvar(carro)
    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado']== None:
        return redirect(url_for('login', proxima=url_for('deletar', id=id)))
    carro_dao.Excluir(id)
    flash('O Carro foi removido com sucesso')
    return redirect(url_for('index'))

@app.route('/carro/<int:id>')
def carro(id):
    carros = carro_dao.Buscar_por_id(id)
    print(carros)
    return render_template('carro.html', titulo='Carro', carro=carros)