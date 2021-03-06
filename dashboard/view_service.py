from django.views.generic import DetailView, ListView
from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import reverse
from .models import Service, State, StateComment
from logging import getLogger


log = getLogger("happening.dashboard.views.service")


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
    template_name_suffix = ""
    model = Service
    
    def render_to_response(self, context, **response_kwargs):
        if self.request.user.is_authenticated:
            return super(ServiceView, self).render_to_response(context, **response_kwargs)
        else:
            if self.object.public:
                return super(ServiceView, self).render_to_response(context, **response_kwargs)
            else:
                log.error("service is not available to be viewed :: public is false")
                return render(self.request, "dashboard/login.html", status=401, context={
                    'next': reverse('dash:service_view', kwargs={'id': self.object.id})
                })

    def get_context_data(self, **kwargs):
        context = super(ServiceView, self).get_context_data(**kwargs)
        current_state = State.get_latest_state(service=self.object)
        context['current_state'] = {
            'id': current_state.id,
            'filed_at': current_state.filed_at,
            'forecast_next': current_state.forecast_change_date,
            'display_name': State.States(current_state.value).label,
            'css_class': State.States.get_css_class(current_state.value)
        }
        context['comments'] = StateComment.get_comments(current_state)
        context['states'] = State.get_recent_states(self.object)
        return context


class ServiceListView(ListView):
    model = Service
    template_name_suffix = "_list"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ServiceListView, self).get_context_data(**kwargs)
        objects = list()
        # TODO: Sort by enabled, then by status, then by newest state event
        for service in context['object_list']:
            state = State.get_latest_state(service)
            css_class: str
            if service.enabled:
                css_class = State.States.get_css_class(state.value)
            else:
                css_class = " bg-info text-white"
            objects.append({
                'service': service,
                'state': state,
                'state_display_name': State.States(state.value).label,
                'row_class': css_class,
            })
        context['object_list'] = objects
        return context
