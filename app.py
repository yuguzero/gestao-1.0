from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# 🔌 conectar banco
def conectar():
    return sqlite3.connect("database.db")

# 🧱 criar tabela (se não existir)
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

@app.route("/")
def home():
    return render_template("index.html")

# 📋 listar
@app.route("/brinquedos", methods=["GET"])
def listar():
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
    data = request.json

    conn = conectar()
    c = conn.cursor()
    c.execute("""
        INSERT INTO brinquedos (nome, cliente, telefone, entrega, retirada, valor, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        data["nome"], data["cliente"], data["telefone"],
        data["entrega"], data["retirada"],
        data["valor"], data["status"]
    ))
    conn.commit()
    conn.close()

    return {"ok": True}

# 🔄 status
@app.route("/status", methods=["POST"])
def status():
    data = request.json

    conn = conectar()
    c = conn.cursor()
    c.execute("UPDATE brinquedos SET status=? WHERE id=?", (data["status"], data["id"]))
    conn.commit()
    conn.close()

    return {"ok": True}

# 🗑️ deletar
@app.route("/deletar", methods=["POST"])
def deletar():
    data = request.json

    conn = conectar()
    c = conn.cursor()
    c.execute("DELETE FROM brinquedos WHERE id=?", (data["id"],))
    conn.commit()
    conn.close()

    return {"ok": True}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
