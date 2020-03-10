from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import reverse
from .models import State, StateComment


# noinspection DuplicatedCode
class StateNewView(CreateView):
    model = State
    fields = ['value', 'forecast_change_date']
    template_name_suffix = "_create_form"

    def get_context_data(self, **kwargs):
        context = super(StateNewView, self).get_context_data(**kwargs)
        context['state_choices'] = list()
        for value, label in State.States.choices:
            context['state_choices'].append({
                'db_name': value,
                'common_name': label
            })
        context['current_state'] = {
            'db_name': State.States(self.object.value).value,
            'common_name': State.States(self.object.value).label
        }
        return context


# noinspection DuplicatedCode
class StateEditView(UpdateView):
    model = State
    fields = ['value', 'forecast_change_date']
    template_name_suffix = "_update_form"

    def get_context_data(self, **kwargs):
        context = super(StateEditView, self).get_context_data(**kwargs)
        context['state_choices'] = list()
        for value, label in State.States.choices:
            context['state_choices'].append({
                'db_name': value,
                'common_name': label
            })
        context['current_state'] = {
            'db_name': State.States(self.object.value).value,
            'common_name': State.States(self.object.value).label
        }
        return context


# noinspection DuplicatedCode
class StateView(DetailView):
    model = State
    template_name_suffix = ""

    def get_context_data(self, **kwargs):
        context = super(StateView, self).get_context_data(**kwargs)
        context['state_choices'] = list()
        for value, label in State.States.choices:
            context['state_choices'].append({
                'db_name': value,
                'common_name': label
            })
        context['current_state'] = {
            'db_name': State.States(self.object.value).value,
            'common_name': State.States(self.object.value).label
        }
        context['comments'] = StateComment.get_comments(self.object)
        return context


class StateCommentNewView(CreateView):
    model = StateComment
    fields = ['state', 'content']

    def get_success_url(self):
        return reverse('dash:state_view', kwargs={'service_id': self.object.state.service.id, 'pk': self.object.state.id})


class StateCommentUpdateView(UpdateView):
    model = StateComment
    fields = ['content']
