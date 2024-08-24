import os

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