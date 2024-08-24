from flask import Flask, request, jsonify
import methods.openai_methods

import os
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI

app = Flask(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key = OPENAI_API_KEY)

initial_prompt = """
        Você é o Stênio, um assistente de negócios da empresa Stone, feito para auxiliar a vida de empreendedores pequenos lojistas
        a encantar seus clientes e gerenciar seu negócio (pagamentos, vendas, conta bancária).
        Você está ajudando e conversando com o Francisco, dono de cafeteria em Tiradentes, e que representa o típico empreendedor brasileiro.
        Fale com ele somente em português. Responda a ele em uma linguagem amigável e acessível.
        Caso ele esteja perdido sobre como começar a melhorar o seu negócio, direcione a conversa para caixa de giro.
        Tente criar um relacionamento com ele, explicar bem sobre e deixar ele perguntar. Procure 
        Durante a conversa, quando surgir a oportunidade, tente oferecer crédito para ele, por meio de produtos da Stone.
        Responda para o Francisco em respostas curtas, com não mais de 50 palavras.
    """

historical_messages = [
    {"role": "assistant", "content": initial_prompt},
    ]

@app.route('/getResponse', methods=['POST'])
def get_response():
    data = request.get_json()
    prompt = data.get('prompt')

    textmodel_response = methods.openai_methods.get_response_from_model(client, prompt, historical_messages)

    response = {
        'resposta': textmodel_response
    }

    return jsonify(response)

@app.route('/deleteHistory', methods=['POST'])
def delete_history():
    global historical_messages
    historical_messages = [
        {"role": "assistant", "content": initial_prompt},
    ]

    response = {
        'resposta': "Histórico apagado com sucesso"
    }

    return jsonify(response)

@app.route('/getHistory', methods=['GET'])
def get_history():
    response = {
        'resposta': historical_messages
    }
    return jsonify(response)

@app.route('/uploadAudio', methods=['POST'])
def upload_audio():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    file_content = file.read()

    print(f"Conteúdo do arquivo (primeiros 100 bytes): {file_content[:100]}")

    file_path = f"./uploads/{file.filename}"
    with open(file_path, 'wb') as f:
        f.write(file_content)

    return jsonify({'message': 'Arquivo de aúdio carregado no servidor com sucesso'}), 200

if __name__ == '__main__':
    app.run(debug=True)

