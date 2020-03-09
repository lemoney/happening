from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import reverse
from .models import Service, State


class StateNewView(CreateView):
    model = State
    fields = ['value', 'forecast_change_date']
    template_name_suffix = "_create_form"


class StateEditView(UpdateView):
    model = State
    fields = ['value', 'forecast_change_date']
    template_name_suffix = "_update_form"


class StateView(DetailView):
    model = State
    template_name = 'dashboard/state.html'
