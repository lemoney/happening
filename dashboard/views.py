from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .models import Service


# Create your views here.
def index(req: HttpRequest) -> HttpResponse:
    # sort the capability set
    capabilities = sorted(Service.get_homepage_capabilities(logged_in=req.user.is_authenticated),
                          key=lambda i: i['name'])
    return render(req, 'dashboard/index.html',
                  {'page_name': 'Happening!',
                   'capabilities': capabilities})


def search(req: HttpRequest) -> HttpResponse:
    # TODO: Search URL
    return HttpResponse('<a href="/">TODO!</a>', status=501)
