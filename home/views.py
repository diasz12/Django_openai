from django.shortcuts import render, redirect
from .models import Video
from .utils import Trascricao, gerar_resumo

def home(request):
    resumo = None  # Inicializa resumo como None

    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        video = request.FILES.get('video')
        custom_prompt = request.POST.get('custom_prompt', '')  # Captura o prompt personalizado

        # Salva o vídeo no banco de dados
        video_upload = Video(titulo=titulo, video=video)
        video_upload.save()

        # Realiza a transcrição do vídeo
        transcricao = Trascricao(video_upload.video.path)
        transcript = transcricao.trascrever()

        # Gera o resumo usando o transcript e o custom_prompt
        video_upload.transcricao = transcript
        video_upload.resumo = gerar_resumo(transcript, custom_prompt)  # Passa os dois argumentos
        video_upload.save()

        # Armazena o resumo na sessão para exibição após o redirecionamento
        request.session['resumo'] = video_upload.resumo

        # Redireciona para evitar duplicação ao recarregar a página
        return redirect('home')

    # Recupera o resumo da sessão (se existir) e limpa a sessão
    resumo = request.session.pop('resumo', None)

    return render(request, 'home.html', {'resumo': resumo})