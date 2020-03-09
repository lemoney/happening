from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, reverse
from .models import Service


class ServiceEditView(UpdateView):
    model = Service
    template_name_suffix = "_update_form"
    fields = ['name', 'description', 'public', 'enabled']

    def get_success_url(self):
        return reverse('dash:service_view', kwargs={'pk': self.object.id})


class ServiceView(DetailView):
    """View of a service"""
    template_name = "dashboard/service.html"
    model = Service
    initial = {}

    def post(self, req: HttpRequest, *args, **kwargs):
        form = self.form_class(req.POST)
        if form.is_valid():
            return redirect(Service.objects.get(id=form.id))
        return HttpResponse("hello", status=401)
