from flask import Blueprint, Flask, redirect, request, render_template, url_for, current_app, send_file
import os, json

professor = Blueprint('professor', __name__)

CADASTROS_JSON = "cadastros.json"

def get_user_info():
    with open(CADASTROS_JSON, encoding='utf-8') as file:
        cadastros = json.load(file)
        for usuario in cadastros:
            if usuario['RA'] == current_app.config['RA_SESSION']:
                return usuario
    return {}

def pegar_atestado(id):
    usuario = get_user_info()
    for atestado in usuario.keys():
        if 'atestado' in atestado and usuario[atestado]['id'] == id:
            return atestado

@professor.route('/index', methods=['GET', 'POST'])
def index():
    usuarios = []
    with open(CADASTROS_JSON, 'r', encoding='UTF-8') as file:
        usuarios = json.load(file)
    if request.method == 'POST':
        pesquisa = request.form['Pesquisar']
        for usuario in usuarios:
            if not pesquisa in usuario['RA']:
                usuarios.remove(usuario)


    return render_template("area_professor.html", usuarios = usuarios)

@professor.route('/abrir_pdf/<path:pdf>')
def abrir_pdf(pdf):
    return send_file(pdf, mimetype='application/pdf', as_attachment=False)
