from flask import Flask, request, jsonify
import methods.openai_methods
from flask_cors import CORS, cross_origin
import os
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI
import base64
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


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

@app.route('/getResponseText', methods=['POST'])
@cross_origin()
def get_response_text():
    data = request.get_json()
    prompt = data.get('prompt')

    textmodel_response = methods.openai_methods.get_response_from_model(client, prompt, historical_messages)

    audio_data = methods.openai_methods.convert_text_to_speech(client, textmodel_response)

    file_content_base64 = base64.b64encode(audio_data).decode('utf-8')

    # audio_falado = "resposta_modelo_falada.webm"
    # file_path = f"./uploads/{audio_falado}"

    # with open(file_path, 'wb') as f:
    #     f.write(audio_data)

    response = {
        'model_responde_text': textmodel_response,
        'model_responde_audio': file_content_base64
    }

    return jsonify(response)

@app.route('/getResponseAudio', methods=['POST'])
@cross_origin()
def get_response_audio():
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo foi enviado na requisicao'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'Nenhum arquivo selecionado'}), 400

    file_content = file.read()

    file_path = f"./uploads/{file.filename}"
    with open(file_path, 'wb') as f:
        f.write(file_content)
    
    converted_text_openai = methods.openai_methods.convert_speech_to_text(client, file_path)

    textmodel_response = methods.openai_methods.get_response_from_model(client, converted_text_openai, historical_messages)
    
    audio_data = methods.openai_methods.convert_text_to_speech(client, textmodel_response)

    file_content_base64 = base64.b64encode(audio_data).decode('utf-8')

    response = {
        'model_responde_text': textmodel_response,
        'model_responde_audio': file_content_base64
    }

    return jsonify(response)

@app.route('/deleteHistory', methods=['POST'])
@cross_origin()
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
@cross_origin()
def get_history():
    response = {
        'resposta': historical_messages
    }
    return jsonify(response)

@app.route('/uploadAudio', methods=['POST'])
def upload_audio():
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo foi enviado na requisicao'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'Nenhum arquivo selecionado'}), 400

    file_content = file.read()

    file_path = f"./uploads/{file.filename}"
    with open(file_path, 'wb') as f:
        f.write(file_content)

    return jsonify({'message': 'Arquivo de aúdio carregado no servidor com sucesso. Contéudo (primeiros 100 bytes:)' + file_content[:100]}), 200

@app.route('/transcribeAudio', methods=['POST'])
@cross_origin()
def transcribe_audio():
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo foi enviado na requisicao'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'Nenhum arquivo selecionado'}), 400

    file_content = file.read()

    file_path = f"./uploads/{file.filename}"
    with open(file_path, 'wb') as f:
        f.write(file_content)
    
    converted_text_openai = methods.openai_methods.convert_speech_to_text(client, file_path)

    return jsonify({'message': 'Texto transcrito do áudio: ' + converted_text_openai}), 200

@app.route('/verbalizeText', methods=['POST'])
@cross_origin()
def verbalize_text():
    data = request.get_json()
    text = data.get('prompt')

    audio_data = methods.openai_methods.convert_text_to_speech(client, text)

    audio_falado = "audio_falado.webm"
    file_path = f"./uploads/{audio_falado}"

    file_content_base64 = base64.b64encode(audio_data).decode('utf-8')

    with open(file_path, 'wb') as f:
        f.write(audio_data)
    
    return jsonify({'message': 'Arquivo de aúdio carregado no servidor com sucesso. Contéudo (primeiros 100 bytes:)' + str(audio_data[:100]),
                    'file_content': file_content_base64
                    }), 200

if __name__ == '__main__':
    app.run(debug=True)
