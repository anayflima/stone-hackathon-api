import os
from io import BytesIO
import requests

def get_response_from_model(client, question, historical_messages):
    historical_messages.append({"role": "user", "content": question})
    messages_list = [
                {"role": m["role"], "content": m["content"]}
                for m in historical_messages
                ]
    print(messages_list)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages_list
        )
    response_text = response.choices[0].message.content
    historical_messages.append({"role": "assistant", "content": response_text})
    return response_text

def convert_speech_to_text(client, file_path):
    audio_file= open(file_path, "rb")
    transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
        )
    return transcription.text

def convert_text_to_speech(client, text):
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

# def generate_image_from_short_description(client, message):
#     response = client.chat.completions.create(
#         model="gpt-4-0125-preview",
#         messages=[
#             {
#                 "role": "system",
#                 "content":
#                     """
#                     Você é um sistema de descrição de imagem que descreve imagens para um blog interativo e educativo para o Francisco, dono de uma cafeteria em Tiradentes,
#                     no Brasil. Ele é cliente da Stone, e o blog está sendo gerado pela Stone.
#                     Você recebe uma breve descrição em formato de legenda da imagem. Descreva o cenário de uma forma que seria adequado para uma entrada para um modelo de
#                     stable diffusion image generation AI, DALL·E. Devolva somente esse prompt. As imagens que vão ser geradas devem ser simples, educativas, e divertidas.
#                     """
#             },
#             {
#                 "role": "user", "content": message},
#             ]
#     )
#     image_description = response.choices[0].message.content
#     print(image_description)

#     response = client.images.generate(
#         model="dall-e-3",
#         prompt=image_description,
#         size="1792x1024",
#         quality="standard",
#         n=1,
#     )
    
#     image_url = response.data[0].url
#     return image_url

def generate_image(client, image_description):
    print('generate_image')
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
    print('generate_blog_text')

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
    print("blog_text")
    print(blog_text)

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
    print("image_description")
    print(image_description)
    
    return blog_text, image_description