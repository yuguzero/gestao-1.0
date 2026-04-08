from flask import Flask, request, jsonify, render_template, send_from_directory
import psycopg2
import os

app = Flask(__name__)

# 🔗 conexão PostgreSQL (Render usa DATABASE_URL)
DATABASE_URL = os.getenv("DATABASE_URL")

def conectar():
    return psycopg2.connect(DATABASE_URL)

# 🧱 criar tabela
def criar_tabela():
    conn = conectar()
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS brinquedos (
        id SERIAL PRIMARY KEY,
        nome TEXT,
        cliente TEXT,
        telefone TEXT,
        entrega TEXT,
        retirada TEXT,
        valor NUMERIC,
        status TEXT
    )
    """)
    conn.commit()
    c.close()
    conn.close()

criar_tabela()

# 🏠 home
@app.route("/")
def home():
    return render_template("index.html")

# 📱 manifest
@app.route("/manifest.json")
def manifest():
    return send_from_directory(".", "manifest.json")

# ⚙️ service worker
@app.route("/sw.js")
def sw():
    return send_from_directory(".", "sw.js")

# 📋 listar
@app.route("/brinquedos", methods=["GET"])
def listar():
    conn = conectar()
    c = conn.cursor()
    c.execute("SELECT id, nome, cliente, telefone, entrega, retirada, valor, status FROM brinquedos")
    dados = c.fetchall()
    c.close()
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
            "valor": float(d[6]) if d[6] else 0,
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
        VALUES (%s, %s, %s, %s, %s, %s, %s)
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
    c.close()
    conn.close()

    return {"ok": True}

# 🔄 status
@app.route("/status", methods=["POST"])
def status():
    data = request.json

    conn = conectar()
    c = conn.cursor()
    c.execute("UPDATE brinquedos SET status=%s WHERE id=%s", (data["status"], data["id"]))
    conn.commit()
    c.close()
    conn.close()

    return {"ok": True}

# 🗑️ deletar
@app.route("/deletar", methods=["POST"])
def deletar():
    data = request.json

    conn = conectar()
    c = conn.cursor()
    c.execute("DELETE FROM brinquedos WHERE id=%s", (data["id"],))
    conn.commit()
    c.close()
    conn.close()

    return {"ok": True}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
