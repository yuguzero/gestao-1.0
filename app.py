from flask import render_template
from flask import Flask, request, jsonify

app = Flask(__name__)

# "banco de dados" temporário (lista)
brinquedos = []

@app.route("/")
def home():
    return render_template("index.html")

# LISTAR brinquedos
@app.route("/brinquedos", methods=["GET"])
def listar_brinquedos():
    return jsonify(brinquedos)

# ADICIONAR brinquedo
@app.route("/brinquedos", methods=["POST"])
def adicionar_brinquedo():
    dados = request.json
    brinquedos.append(dados)
    return {"mensagem": "Brinquedo adicionado!"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)