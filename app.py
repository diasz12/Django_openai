import streamlit as st
from home.utils import Trascricao, gerar_resumo  # Importa as funções do Django
from django.conf import settings
import os

# Configurações do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
import django
django.setup()

from home.models import Video  # Importa o modelo Video do Django

# Título da aplicação
st.title("Transcrição e Resumo de Vídeos 🎥")

# Formulário para upload de vídeo
st.header("Envie seu vídeo")
titulo = st.text_input("Título do vídeo", placeholder="Digite o título do vídeo")
custom_prompt = st.text_area("Prompt personalizado", placeholder="Digite seu prompt personalizado")
video_file = st.file_uploader("Faça o upload do vídeo", type=["mp4", "mov", "avi"])

# Botão para processar o vídeo
if st.button("Processar"):
    if not video_file or not titulo or not custom_prompt:
        st.error("Por favor, preencha todos os campos e envie um vídeo.")
    else:
        # Salva o vídeo no diretório "media/video"
        video_dir = "media/video"
        os.makedirs(video_dir, exist_ok=True)  # Cria o diretório, se não existir
        video_path = os.path.join(video_dir, video_file.name)

        # Salva o arquivo enviado pelo usuário
        with open(video_path, "wb") as f:
            f.write(video_file.read())

        # Verifica se o arquivo foi salvo corretamente
        if not os.path.exists(video_path):
            st.error(f"O arquivo de vídeo não foi encontrado no caminho: {video_path}")
        else:
            st.success(f"Arquivo salvo em: {video_path}")

        # Processa o vídeo
        try:
            st.info("Transcrevendo o vídeo...")
            transcricao = Trascricao(video_path)
            transcript = transcricao.trascrever()

            st.info("Gerando o resumo...")
            resumo = gerar_resumo(transcript, custom_prompt)

            # Salva os resultados no banco de dados
            video_upload = Video(titulo=titulo, video=video_path, transcricao=transcript, resumo=resumo)
            video_upload.save()

            # Exibe o resumo
            st.success("Processamento concluído!")
            st.subheader("Resumo gerado:")
            st.write(resumo)
        except Exception as e:
            st.error(f"Erro ao processar o vídeo: {e}")

# Exibe os vídeos processados anteriormente
st.header("Histórico de vídeos")
videos = Video.objects.all().order_by('-id')[:5]  # Mostra os últimos 5 vídeos
for video in videos:
    st.subheader(video.titulo)
    st.write(f"Resumo: {video.resumo}")
    st.write("---")