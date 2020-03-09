from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .models import Service
from django.contrib.auth import login, logout


# Create your views here.
def index(req: HttpRequest) -> HttpResponse:
    # sort the capability set
    capabilities = sorted(Service.get_homepage_capabilities(logged_in=req.user.is_authenticated),
                          key=lambda i: i['name'])
    return render(req, 'dashboard/index.html',
                  {'page_name': 'Happening!',
                   'capabilities': capabilities})


def user_login(req: HttpRequest) -> HttpResponse:
    # TODO: User login
    return HttpResponse('<a href="/">TODO!</a>', status=501)


def user_logout(req: HttpRequest) -> HttpResponse:
    logout(req)
    return redirect('dash:homepage')


def search(req: HttpRequest) -> HttpResponse:
    # TODO: Search URL
    return HttpResponse('<a href="/">TODO!</a>', status=501)
