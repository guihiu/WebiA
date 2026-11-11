from django.shortcuts import render


def home(request):
    return render(request, "home.html")


def treinamento(request):
    return render(request, "treinamento.html")
