from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import reverse
from .models import Service, State


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

    def get_context_data(self, **kwargs):
        context = super(ServiceView, self).get_context_data(**kwargs)
        current_state = State.get_latest_state(service=self.object)
        context['current_state'] = {
            'filed_at': current_state.filed_at,
            'forecast_next': current_state.forecast_change_date,
            'display_name': State.States(current_state.value).label,
            'css_class': State.States.get_css_class(current_state.value)
        }
        context['states'] = State.get_recent_states(self.object)
        return context
