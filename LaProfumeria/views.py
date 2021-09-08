from django.shortcuts import render


def Base(request):
    return render(request, 'homepage.html')
