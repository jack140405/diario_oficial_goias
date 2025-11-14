import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from core.downloader import baixar_diarios
from core.pdf_utils import buscar_palavra_no_pdf
from core.email_utils import enviar_arquivos_por_smtp

app = Flask(__name__)
CORS(app)

TEMP_DIR = os.path.join(os.path.dirname(__file__), 'temp')
os.makedirs(TEMP_DIR, exist_ok=True)

@app.route('/', methods=['GET'])
def home():
    return "API Diário Oficial - OK"

@app.route('/buscar', methods=['POST'])
def buscar():
    data = request.get_json() or {}
    palavra = data.get('palavra')
    quantidade = int(data.get('quantidade', 5))
    email = data.get('email')
    if not palavra or not email:
        return jsonify({'erro': 'palavra e email obrigatórios'}), 400
    arquivos = baixar_diarios(quantidade, pasta_temp=TEMP_DIR)
    arquivos_para_enviar = []
    resultados = []
    for arquivo in arquivos:
        paginas, filtrado = buscar_palavra_no_pdf(arquivo, palavra)
        resultados.append({'arquivo': os.path.basename(arquivo), 'paginas': paginas})
        if paginas and filtrado:
            arquivos_para_enviar.append(filtrado)
    enviado = False
    if arquivos_para_enviar:
        enviado = enviar_arquivos_por_smtp(email, f"Resultados: {palavra}", f"Encontradas {len(arquivos_para_enviar)} edições.", arquivos_para_enviar)
    # remove todos os PDFs (originais e filtrados)
    for f in os.listdir(TEMP_DIR):
        try:
            os.remove(os.path.join(TEMP_DIR, f))
        except Exception:
            pass
    return jsonify({'enviado': enviado, 'resultados': resultados})

if __name__ == '__main__':
    app.run(debug=True)
