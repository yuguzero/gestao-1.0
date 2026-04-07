from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "segredo123"

# 🔐 login fixo (depois dá pra evoluir)
USUARIO = "admin"
SENHA = "1234"


# 🔌 conectar banco
def conectar():
    return sqlite3.connect("database.db")


# 🧱 criar tabela
def criar_tabela():
    conn = conectar()
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS brinquedos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        cliente TEXT,
        telefone TEXT,
        entrega TEXT,
        retirada TEXT,
        valor REAL,
        status TEXT
    )
    """)
    conn.commit()
    conn.close()


criar_tabela()


# 🔒 home protegida
@app.route("/")
def home():
    if not session.get("logado"):
        return redirect(url_for("login"))
    return render_template("index.html")


# 🔐 login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("usuario")
        senha = request.form.get("senha")

        if usuario == USUARIO and senha == SENHA:
            session["logado"] = True
            return redirect(url_for("home"))

        return render_template("login.html", erro="Usuário ou senha inválidos")

    return render_template("login.html")


# 🚪 logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# 📋 listar
@app.route("/brinquedos", methods=["GET"])
def listar():
    if not session.get("logado"):
        return jsonify({"erro": "não autorizado"}), 401

    conn = conectar()
    c = conn.cursor()
    c.execute("SELECT * FROM brinquedos")
    dados = c.fetchall()
    conn.close()

    resultado = []
    for d in dados:
        resultado.append({
            "id": d[0],
            "nome": d[1],
            "cliente": d[2],
            "telefone": d[3],
            "entrega": d[4],
            "retirada": d[5],
            "valor": d[6],
            "status": d[7]
        })

    return jsonify(resultado)


# ➕ adicionar
@app.route("/brinquedos", methods=["POST"])
def adicionar():
    if not session.get("logado"):
        return jsonify({"erro": "não autorizado"}), 401

    data = request.json

    conn = conectar()
    c = conn.cursor()
    c.execute("""
        INSERT INTO brinquedos (nome, cliente, telefone, entrega, retirada, valor, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get("nome"),
        data.get("cliente"),
        data.get("telefone"),
        data.get("entrega"),
        data.get("retirada"),
        data.get("valor"),
        data.get("status", "disponível")
    ))
    conn.commit()
    conn.close()

    return {"ok": True}


# 🔄 status
@app.route("/status", methods=["POST"])
def mudar_status():
    if not session.get("logado"):
        return jsonify({"erro": "não autorizado"}), 401

    data = request.json

    conn = conectar()
    c = conn.cursor()
    c.execute(
        "UPDATE brinquedos SET status=? WHERE id=?",
        (data["status"], data["id"])
    )
    conn.commit()
    conn.close()

    return {"ok": True}


# 🗑️ deletar
@app.route("/deletar", methods=["POST"])
def deletar():
    if not session.get("logado"):
        return jsonify({"erro": "não autorizado"}), 401

    data = request.json

    conn = conectar()
    c = conn.cursor()
    c.execute("DELETE FROM brinquedos WHERE id=?", (data["id"],))
    conn.commit()
    conn.close()

    return {"ok": True}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
