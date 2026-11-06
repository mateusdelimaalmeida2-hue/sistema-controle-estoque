from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def conectar():
    conexao = sqlite3.connect("estoque.db")         
    return conexao

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    mensagem = ""
    if request.method == "POST":
        nome = request.form["nome"]
        codigo = request.form["codigo"]
        quantidade = request.form["quantidade"]
        preco = request.form["preco"]
        id_categoria = request.form["id_categoria"]
        if nome == "" or codigo == "":           
            mensagem = "Todos os campos são obrigatórios."                 
        else:
            conexao = conectar()
            conexao.execute(
                "INSERT INTO produto (nome, codigo, quantidade, preco, id_categoria) VALUES (?, ?, ?, ?, ?)",
                (nome, codigo, quantidade, preco, id_categoria)
            )
            conexao.commit()
            conexao.close()
            mensagem = "Produto cadastrado com sucesso."                 

    conexao = conectar()
    categorias = conexao.execute("SELECT id_categoria, nome FROM categoria").fetchall()
    conexao.close()
    return render_template("cadastro.html", categorias=categorias, mensagem=mensagem)

@app.route("/consultar", methods=["GET"])
def consultar():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT p.codigo, p.nome, c.nome, p.quantidade, p.preco 
        FROM produto p 
        JOIN categoria c ON p.id_categoria = c.id_categoria
    """)
    produtos = cursor.fetchall()
    conexao.close()
    return render_template("consulta.html", produtos=produtos)

if __name__ == "__main__":
    app.run(debug=True)
