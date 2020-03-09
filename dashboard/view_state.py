from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import reverse
from .models import Service, State


class StateNewView(CreateView):
    model = State


class StateEditView(UpdateView):
    model = State


class StateView(DetailView):
    model = State
