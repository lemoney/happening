from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .models import Service


# Create your views here.
def index(req: HttpRequest) -> HttpResponse:
    services = Service.objects.filter(is_capability=True)[:5]
    return render(req, 'dashboard/index.html', {'page_name': 'Happening!', 'capabilities': services})
