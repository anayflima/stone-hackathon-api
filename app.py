from flask import Flask, request, jsonify, send_file, make_response
import io
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
from io import BytesIO
import requests


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key = OPENAI_API_KEY)

initial_prompt = """
        Você é o Stênio, um assistente de negócios da empresa Stone, feito para auxiliar a vida de empreendedores pequenos lojistas
        a encantar seus clientes e gerenciar seu negócio (pagamentos, vendas, conta bancária).
        Você está ajudando e conversando com o Francisco, dono de cafeteria em Tiradentes, e que representa o típico empreendedor brasileiro.
        Fale com ele somente em português. Responda a ele em uma linguagem amigável e acessível.
        O Francisco acabou de receber uma notificação sobre sua métrica de giro de caixa estar 42% menor do que a de seus concorrentes.
        Tente criar um relacionamento com ele.
        Se ele perguntar o valor de alguma métrica sua, responda um valor qualquer e fale que irá montar um dashboard personalizado para ele com a evolução temporal
        no dashboard dentro do aplicativo.
        Durante a conversa, quando surgir a oportunidade, tente oferecer crédito para ele, por meio de produtos da Stone.
        Responda para o Francisco em respostas curtas, com não mais de 50 palavras.
    """

historical_messages = [
    {"role": "assistant", "content": initial_prompt},
    ]

@app.route('/getResponse', methods=['POST'])
@cross_origin()
def get_response():
    data = request.get_json()
    prompt = data.get('prompt')

    textmodel_response = methods.openai_methods.get_response_from_model(client, prompt, historical_messages)
    
    response = {
        'model_response_text': textmodel_response,
    }

    return jsonify(response)

@app.route('/getResponseText', methods=['POST'])
@cross_origin()
def get_response_text():
    data = request.get_json()
    prompt = data.get('prompt')

    textmodel_response = methods.openai_methods.get_response_from_model(client, prompt, historical_messages)

    audio_data = methods.openai_methods.convert_text_to_speech(client, textmodel_response)

    response = {
        'model_response_text': textmodel_response
    }

    return send_file(
        io.BytesIO(audio_data),
        mimetype='audio/webm',
        as_attachment=False,
        download_name='response_audio.webm'
    ), 200, response

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

    response = {
        'model_response_text': textmodel_response
    }

    return send_file(
        io.BytesIO(audio_data),
        mimetype='audio/webm',
        as_attachment=False,
        download_name='response_audio.webm'
    ), 200, response


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


@app.route('/getBlog', methods=['GET'])
def get_blog():
    data = [
        {"id": 1, "name": "Item 1"},
    ]
    return jsonify(data)

@app.route('/getBlogs', methods=['GET'])
def get_blogs():
    data = [
        {"id": 1, "name": "Item 1"},
        {"id": 2, "name": "Item 2"},
        {"id": 3, "name": "Item 3"}
    ]
    return jsonify(data)

@app.route('/generateImage', methods=['POST'])
def generate_image_route():
    message = request.json.get('message')
    image_url = methods.openai_methods.generate_image(client, message)
    
    image_response = requests.get(image_url)
    image_bytes = BytesIO(image_response.content)

    image_path = os.path.join('uploads', 'generated_image.png')
    with open(image_path, 'wb') as f:
        f.write(image_bytes.getbuffer())
    
    return send_file(image_bytes, mimetype='image/png', as_attachment=True, download_name='generated_image.png')

@app.route('/generateBlogText', methods=['POST'])
def generate_blog_text():
    message = request.json.get('message')
    image_url = methods.openai_methods.generate_image(client, message)
    
    image_response = requests.get(image_url)
    image_bytes = BytesIO(image_response.content)

    image_path = os.path.join('uploads', 'generated_image.png')
    with open(image_path, 'wb') as f:
        f.write(image_bytes.getbuffer())
    
    return send_file(image_bytes, mimetype='image/png', as_attachment=True, download_name='generated_image.png')

@app.route('/getBlogPost', methods=['POST'])
def get_blog_post():
    data = request.get_json()
    topic = data.get('topic')
    blog_content, image_description = methods.openai_methods.generate_blog_text(client, topic)

    image_url = methods.openai_methods.generate_image(client, image_description)

    image_response = requests.get(image_url)
    image_bytes = BytesIO(image_response.content)

    # image_path = os.path.join('uploads', 'image_get_blog.png')
    # with open(image_path, 'wb') as f:
    #     f.write(image_bytes.getbuffer())
    
    response = make_response(send_file(image_bytes, mimetype='image/png', as_attachment=True, download_name='generated_image.png'))
    response.headers['Content-Disposition'] = 'attachment; filename=generated_image.png'
    response.data = blog_content
    
    return response


if __name__ == '__main__':
    app.run(debug=True)
