import moviepy as mp
from django.conf import settings
from pathlib import Path
from openai import OpenAI
import os

class Trascricao:
    def __init__(self, path_video):
        self.path_video = path_video
        self.video = mp.VideoFileClip(path_video)
        self.client = OpenAI(
            api_key=settings.SECRET_KEY
        )

    @property
    def path_audio(self):
        return f'{settings.BASE_DIR / "audio_file" / Path(self.path_video).stem}.mp3'

    def save_temfile(self):
        self.video.audio.write_audiofile(self.path_audio)  

    def trascrever(self):
        self.save_temfile()

        try:
            with open(self.path_audio, 'rb') as audio_file:
                trascript = self.client.audio.transcriptions.create(  # Corrigido de 'trascriptions' para 'transcriptions'
                    model="whisper-1",
                    file=audio_file,
                    response_format="text",
                    language="pt",
                )
        finally:
            os.remove(self.path_audio)

        return trascript
    
def gerar_resumo(texto):
    client = OpenAI(
        api_key=settings.SECRET_KEY
    )

    resposta = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um assistente que resume textos."},
            {"role": "user", "content": f"Resuma a transcrição a seguir, organizando os passos descritos em ordem lógica. Identifique as ferramentas mencionadas e associe cada etapa à ferramenta quando necessário: {texto}"}
        ]
    )

    # Acessando o conteúdo da resposta corretamente
    return resposta.choices[0].message.content.strip()



