from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Seu app tá rodando 🔥"

if __name__ == "__main__":
    app.run()