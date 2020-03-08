from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .models import Service, State


# Create your views here.
def index(req: HttpRequest) -> HttpResponse:
    services = Service.objects.filter(is_capability=True, enabled=True)[:5]
    capabilities = list()
    for service in services:
        state = State.objects.filter(service=service.id).order_by('-filed_at').first()
        if state is None:
            state = State.UP.title()
        capabilities.append({
            'name': service.name,
            'state': state
        })
    return render(req, 'dashboard/index.html', {'page_name': 'Happening!', 'capabilities': capabilities})
