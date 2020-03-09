from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import reverse
from .models import Service


class ServiceNewView(CreateView):
    model = Service
    fields = ['name', 'description', 'public', 'enabled', 'is_capability']
    template_name_suffix = "_create_form"
    initial = {
        'enabled': True,
        'public': False,
    }

    def get_success_url(self):
        return reverse('dash:service_view', kwargs={'pk': self.object.id})


class ServiceEditView(UpdateView):
    model = Service
    template_name_suffix = "_update_form"
    fields = ['name', 'description', 'public', 'enabled', 'is_capability']

    def get_success_url(self):
        return reverse('dash:service_view', kwargs={'pk': self.object.id})


class ServiceView(DetailView):
    """View of a service"""
    template_name = "dashboard/service.html"
    model = Service
    initial = {'enabled': True, 'public': False}

    def get_context_data(self, **kwargs):
        context = self.initial
        context.update(super().get_context_data(**kwargs))
        return context
