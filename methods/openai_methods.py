import os
from io import BytesIO
import requests

def get_response_from_model(client, question, historical_messages):
    """
    Obtém uma resposta do modelo de linguagem "gpt-4o" baseado em uma pergunta e histórico de mensagens.

    Args:
        client: O cliente da API que será usado para se comunicar com o modelo de linguagem.
        question (str): A pergunta que o usuário deseja fazer ao modelo.
        historical_messages (list): Uma lista de dicionários contendo o histórico de mensagens. 
                                    Cada dicionário deve ter as chaves "role" e "content".

    Returns:
        str: A resposta gerada pelo modelo de linguagem.
    """
    historical_messages.append({"role": "user", "content": question})
    messages_list = [
                {"role": m["role"], "content": m["content"]}
                for m in historical_messages
                ]
    print(messages_list)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages_list
        )
    response_text = response.choices[0].message.content
    historical_messages.append({"role": "assistant", "content": response_text})
    return response_text

def convert_speech_to_text(client, file_path):
    """
    Converte um arquivo de áudio em texto usando o modelo de transcrição de fala "whisper-1".

    Args:
        client: O cliente da API que será usado para se comunicar com o modelo de transcrição.
        file_path (str): O caminho para o arquivo de áudio que será transcrito.

    Returns:
        str: O texto transcrito do arquivo de áudio.
    """
    audio_file= open(file_path, "rb")
    transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
        )
    return transcription.text

def convert_text_to_speech(client, text):
    """
    Converte um texto em fala usando o modelo de síntese de voz "tts-1".

    Args:
        client: O cliente da API que será usado para se comunicar com o modelo de síntese de voz.
        text (str): O texto que será convertido em fala.

    Returns:
        bytes: Os dados de áudio gerados a partir do texto.
    """
    if text:
        speech_file_path = "speech.webm"
        response = client.audio.speech.create(
        model="tts-1",
        voice="echo",
        input=text
        )
        response.stream_to_file(speech_file_path)
        with open(speech_file_path, "rb") as audio_file:
            audio_data = audio_file.read()
        os.remove(speech_file_path)
        return audio_data

def generate_image(client, image_description):
    """
    Gera uma imagem com base em uma descrição usando o modelo de geração de imagens "dall-e-3".

    Args:
        client: O cliente da API que será usado para se comunicar com o modelo de geração de imagens.
        image_description (str): A descrição da imagem que será gerada.

    Returns:
        str: A URL da imagem gerada.
    """
    response = client.images.generate(
        model="dall-e-3",
        prompt=image_description,
        size="1792x1024",
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url

    image_response = requests.get(image_url)
    image_bytes = BytesIO(image_response.content)

    image_path = os.path.join('uploads', 'generate_image.png')
    with open(image_path, 'wb') as f:
        f.write(image_bytes.getbuffer())
    
    return image_url

def generate_blog_text(client, message):
    """
    Gera o texto de um blog personalizado para o empreendedor e uma descrição de imagem para a capa do blog usando o modelo de linguagem "gpt-4o".

    Args:
        client: O cliente da API que será usado para se comunicar com o modelo de linguagem.
        message (str): O tópico que será o tema do blog.

    Returns:
        tuple: Um par contendo o texto do blog em formato HTML e a descrição da imagem para a capa do blog.
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content":
                    """
                    Você é Stênio, um sistema gerador de artigos de blogs para uma plataforma educativa da Stone para pequenos empreendedores.
                    O blog deve ser escrito especialmente personalizado para o Francisco, dono de cafeteria em Tiradentes, e que representa o típico empreendedor brasileiro.
                    Você irá receber um tópico para ser o tema de um blog e você deve escrever um blog baseado nesse tópico.
                    O blog deve ser bem didático, com vários exemplos e ser personalizado para o Francisco. Use uma linguagem simples, clara, educativa, e divertida.
                    Tente vender produtos da Stone no decorrer do blog, quando surgir a oportunidade. Tente oferecer crédito, por exemplo.
                    Além disso, o blog está junto de uma plataforma que inclui um chatbot por voz e um dashboard. Sempre que possível, recomende que o Francisco
                    veja suas métricas através do dashboard.
                    Além disso, suponha que você tem os dados do Francisco, de fluxo de caixa, vendas, entradas e saídas na conta bancária, etc. Aproveite esses 
                    dados para personalizar o blog com dados reais de Francisco, comparando-os com a média do setor.
                    Gere o conteúdo do artigo no blog como o body de um arquivo html (sem a tag <body>) no seguinte formato:
                    Faça o título com a tag <h1> com a classe
                    tituloBlog, subtítulos com <h3> e com a classe subtituloBlog, e em seguinte o texto em <p> com classe textoBlog.
                    Você pode adicionar textos em negritos com a tag <strong> ao longo do texto em títulos e tópicos.
                    Assine o blog como Stênio.
                    Gere um documento mais ou menos nesse formato:

                    <h1 class="tituloBlog">Título</h1>

                    <h3 class="subtituloBlog">Subtítulo</h3>
                    <p class="textoBlog">Conteúdo</p>

                   ...

                    <h3 class="subtituloBlog">Subtítulo/h3>
                    <p class="textoBlog"></p>

                    <p class="textoBlog">Até a próxima,</p>

                    <p class="textoBlog"><strong>Stênio</strong></p>
                    """
            },
            {
                "role": "user", "content": message
            },
        ]
        )
    blog_text = response.choices[0].message.content

    response_image = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content":
                    """
                    Você é um sistema gerador de descrição de uma imagem adequada para ser a capa de um artigo de blog.
                    Você recebe um artigo no blog e gera uma descrição de uma imagem adequada para ser a capa desse artigo.
                    Descreva o cenário de uma forma que seria adequado para uma entrada para um modelo de
                    stable diffusion image generation AI, DALL·E. Devolva somente esse prompt.
                    As imagens que vão ser geradas devem ser simples, educativas, e divertidas.
                    """
            },
            {
                "role": "user", "content": blog_text
            },
        ]
        )
    
    image_description = response_image.choices[0].message.content
    
    return blog_text, image_description