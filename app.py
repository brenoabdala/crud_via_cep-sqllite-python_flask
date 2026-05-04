import sqlite3
import requests
from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

def get_db_connection():
    """Cria uma conexão com o banco SQLite local"""
    conn = sqlite3.connect('dados_cep.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Cria a tabela se não existir - Pilar de Idempotência"""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS stg_enderecos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cep TEXT,
            logradouro TEXT,
            bairro TEXT,
            localidade TEXT,
            uf TEXT,
            data_carga TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buscar/<cep>', methods=['GET'])
def buscar_cep(cep):
    """Consome a API externa ViaCEP"""
    url = f"https://viacep.com.br/ws/{cep}/json/"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if "erro" in data:
                return jsonify({"erro": "CEP não encontrado"}), 404
            return jsonify(data)
        return jsonify({"erro": "Erro na API externa"}), 500
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@app.route('/salvar', methods=['POST'])
def salvar_no_banco():
    """Insere os dados de forma incremental - Pilar de Carga de Dados"""
    dados = request.json
    try:
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO stg_enderecos (cep, logradouro, bairro, localidade, uf, data_carga)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            dados['cep'], 
            dados['logradouro'], 
            dados['bairro'], 
            dados['localidade'], 
            dados['uf'], 
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        conn.commit()
        conn.close()
        return jsonify({"mensagem": "Endereço salvo com sucesso no SQLite!"}), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    init_db()  # Executa a criação da tabela ao iniciar o app
    app.run(debug=True)
