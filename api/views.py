from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


# Create your views here.
def health(req: HttpRequest) -> HttpResponse:
    return HttpResponse('Healthy', status=200)
