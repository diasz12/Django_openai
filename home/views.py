# filepath: c:\Users\guilherme.dias\OneDrive - Via Laser Serviços Estéticos SA\Documentos\projetos\django_openai\home\views.py
from django.shortcuts import render
from . models import Video
from django.http import HttpResponse
from . utils import Trascricao, gerar_resumo

def home(request):
    if request.method == 'GET':
        return render(request, 'home.html')
    elif request.method == 'POST':
        titulo = request.POST.get('titulo')
        video = request.FILES.get('video')

        video_upload = Video(titulo=titulo, video=video)
        video_upload.save()

        transcricao = Trascricao(video_upload.video.path)
        transcript = transcricao.trascrever()

        video_upload.transcricao = transcript
        video_upload.resumo = gerar_resumo(transcript)
        video_upload.save()
        return HttpResponse('Video enviado com sucesso!')   