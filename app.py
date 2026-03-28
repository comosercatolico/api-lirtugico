from flask import Flask, jsonify, request
from flask_cors import CORS

from extractor.ExtractorService import ExtractorService

app = Flask(__name__)
CORS(app)  # 🔥 libera CORS

# 🔁 resposta padrão (evita repetição)
def montar_resposta(fonte, dados):
    return jsonify({
        'objective': 'API para disponibilizar leituras diárias para evangelização.',
        'source': fonte,
        'today': dados
    })

# 📖 Liturgia por data (ou hoje)
@app.route('/')
def homepage():
    try:
        date = request.args.get('date')

        liturgy = ExtractorService.getScrapySagradaLiturgia(date)

        return montar_resposta('https://sagradaliturgia.com.br/', liturgy)

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


# 🎶 Canção Nova
@app.route('/cn')
def cancaoNova():
    try:
        liturgy = ExtractorService.getScrapyCancaoNova()

        return montar_resposta('Canção Nova', liturgy)

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


# 🙏 Santo do dia
@app.route('/santo-do-dia')
def santo():
    try:
        santo = ExtractorService.getScrapySantoCancaoNova()

        return montar_resposta('Canção Nova', santo)

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


# 🔧 garante CORS em qualquer situação
@app.after_request
def add_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    return response
