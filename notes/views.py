from django.shortcuts import render, redirect, get_object_or_404
from .models import Note, Tag
from .forms import NoteForm  # Importe seu formulário aqui

import random

def assign_tag_colors():
    tags = Tag.objects.all()
    colors = ["#b0c2f2", "#b0f2c2", "#fcb7af", "#d8f8e1", "#ffe4e1","#fdf9c4","#ffda9e","#b2e2f2","#cce5ff","#fabfb7","#f6d1de","#c3f9ea","#d0bdf6","#e4fbfb","#dfcae1","#ecd6c0"]
    
    for tag in tags:
        if not tag.color:
            tag.color = random.choice(colors)
            tag.save()


def index(request):
    if request.method == 'POST':
        title = request.POST.get('titulo')
        if title != "":
            content = request.POST.get('detalhes')
            tag_name = request.POST.get('tag_name')
            tag, created = Tag.objects.get_or_create(name=tag_name)

            assign_tag_colors()

            # Cria um novo objeto Note com os dados do formulário
            new_note = Note(title=title, content=content, tag=tag)
            # Salva o novo objeto no banco de dados
            new_note.save()
        return redirect('index')
    else:
        all_notes = Note.objects.all()
        return render(request, 'notes/index.html', {'notes': all_notes})

def delete_note(request, note_id):
    note = get_object_or_404(Note, pk=note_id)

    if request.method == 'POST':
        note.delete()
        return redirect('index')  # Redireciona para a lista de notas após a exclusão
    
    return render(request, 'notes/delete_note.html', {'note': note})


def edit_note(request, note_id):
    note = get_object_or_404(Note, pk=note_id)

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title and content:
            note.title = title
            note.content = content
            note.save()
            return redirect('index')  # Redireciona para a lista de notas após a edição

    return render(request, 'notes/edit_note.html', {'note': note})


def create_note(request):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            tag_name = form.cleaned_data["tag_name"]

            # Verifique se a tag já existe
            tag, created = Tag.objects.get_or_create(name=tag_name)

            # Crie a anotação associando à tag
            note = Note.objects.create(title=title, content=content, tag=tag)

            return redirect("list_notes")

    else:
        form = NoteForm()

    return render(request, "create_note.html", {"form": form})

def tag_list(request):
    tags = Tag.objects.all()
    return render(request, 'notes/tag_list.html', {'tags': tags})

def tag_detail(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    notes = Note.objects.filter(tag=tag)
    return render(request, 'notes/tag_detail.html', {'tag': tag, 'notes': notes})

from django.http import JsonResponse
from .models import Tag

def tag_suggestions(request):
    # Obtenha o texto de entrada da consulta AJAX
    input_text = request.GET.get('q', '')
    
    # Filtrar as tags com base no texto de entrada
    tags = Tag.objects.filter(name__istartswith=input_text)
    
    # Obtenha os nomes das tags correspondentes
    tag_names = [tag.name for tag in tags]
    
    return JsonResponse(tag_names, safe=False)
