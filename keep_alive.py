from flask import Flask
from threading import Thread
import os

app = Flask('')

@app.route('/')
def home():
    return "Servidor rodando e bot online!"

def run():
    # O Render define a porta automaticamente, ou usamos a 8080 por padrão
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()