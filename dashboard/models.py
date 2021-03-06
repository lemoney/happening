from django.db import models
from django.utils.translation import gettext_lazy as text
from django.conf import settings
from django.utils.timezone import make_aware
from django.contrib.auth.models import User
from .get_request import get_request

from typing import List, Dict, Union
from datetime import datetime
from logging import getLogger


log = getLogger("happening.dashboard.models")


# Create your models here.
class Service(models.Model):
    """a technical service that makes up a capability"""
    name = models.CharField("friendly name of a service", max_length=256)
    is_capability = models.BooleanField("if true makes the service a capability which is a business deliverable",
                                        default=False)
    description = models.CharField("what this service is responsible for", max_length=2048)
    enabled = models.BooleanField(default=True)
    public = models.BooleanField("if true will allow the service to be viewed if not authenticated", default=False)

    def __str__(self):
        return self.name

    @staticmethod
    def get_homepage_capabilities(logged_in: bool = False) -> List[Dict[str, str]]:
        """displays the most recent updates and all non-'good' services"""
        if logged_in:
            services = Service.objects.filter(is_capability=True, enabled=True)[:5]
        else:
            services = Service.objects.filter(is_capability=True, enabled=True, public=True)[:5]
        final = list()
        for service in services:
            state: State
            filed_time: datetime
            color: str
            state = State.get_latest_state(service)
            filed_time = state.filed_at
            color = State.States.get_css_class(state.value)
            final.append({
                'id': service.id,
                'name': service.name,
                'description': service.description,
                'state_id': state.id,
                'state': State.States(state.value).label,
                'filed_time': filed_time,
                'css_class': color
            })
        return final


class Relation(models.Model):
    """Maps a relationship between two entities"""

    class RelationTypes(models.TextChoices):
        DEPENDS_ON = 'depends_on', text("Depends On")
        DEPENDENT = 'dependent', text("Dependent")

    origin = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='origin_service')
    destination = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='destination_service')
    relation_type = models.CharField(choices=RelationTypes.choices, default=RelationTypes.DEPENDS_ON, max_length=128)

    def __str__(self):
        direction: str
        if self.relation_type == self.RelationTypes.DEPENDENT:
            direction = "<-<"
        elif self.relation_type == self.RelationTypes.DEPENDS_ON:
            direction = ">->"
        else:
            direction = "<->"
        return f"{self.origin.name} {direction} {self.destination.name}"


class State(models.Model):
    """a state is a way a service could be, like 'DOWN' or 'UP'"""

    class States(models.TextChoices):
        UP = 'up', text("Up")
        DOWN = 'down', text("Down")
        MAINTENANCE_PLANNED = 'planned_maintenance', text("Planned Maintenance")
        MAINTENANCE_UNPLANNED = 'unplanned_maintenance', text("Unplanned Maintenance")
        DEGRADED_WARNING = 'degraded_warning', text("Degraded - Warning")
        DEGRADED_CRITICAL = 'degraded_critical', text("Degraded - Critical")

        @staticmethod
        def get_css_class(state) -> str:
            if state == State.States.UP.value:
                return getattr(settings, "STATES_UP_COLOR", "success")
            elif state == State.States.DOWN.value:
                return getattr(settings, "STATES_DOWN_COLOR", "danger")
            elif state == State.States.MAINTENANCE_PLANNED.value:
                return getattr(settings, "STATES_MAINTENANCE_PLANNED_COLOR", "secondary")
            elif state == State.States.MAINTENANCE_UNPLANNED.value:
                return getattr(settings, "STATES_MAINTENANCE_UNPLANNED_COLOR", "info")
            elif state == State.States.DEGRADED_WARNING.value:
                return getattr(settings, "STATES_DEGRADED_WARNING_COLOR", "warning")
            elif state == State.States.DEGRADED_CRITICAL.value:
                return getattr(settings, "STATES_DEGRADED_CRITICAL_COLOR", "dark")
            else:
                raise ValueError(f"unknown State.States value: {state}")

    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    value = models.CharField(choices=States.choices, default=States.UP, max_length=128)
    filed_at = models.DateTimeField(auto_created=True)
    forecast_change_date = models.DateTimeField("Time this state is expected to change", null=True, blank=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.filed_at is None and self.id is None:
            self.filed_at = make_aware(datetime.utcnow())
        if self.id is not None:
            origin = State.objects.get(id=self.id)
            if origin is not None:
                # means that the service exists already and something is changing
                if self.service.id != origin.service.id:
                    StateChange(state=self, change_type=StateChange.ChangeTypes.SERVICE_CHANGE, old_value=origin.service.id, new_value=self.service.id).save()
                if self.value != origin.value:
                    StateChange(state=self, change_type=StateChange.ChangeTypes.VALUE_CHANGE, old_value=origin.value, new_value=self.value).save()
                if self.filed_at != origin.filed_at:
                    StateChange(state=self, change_type=StateChange.ChangeTypes.FILED_AT, old_value=origin.filed_at, new_value=self.filed_at).save()
                if self.forecast_change_date != origin.forecast_change_date:
                    StateChange(state=self, change_type=StateChange.ChangeTypes.FORECAST, old_value=origin.forecast_change_date, new_value=self.forecast_change_date).save()
        return super(State, self).save(force_insert=force_update, using=using, update_fields=update_fields)

    def __str__(self):
        return f"[{self.filed_at}] {self.service.name} is [{self.value}]"

    @staticmethod
    def get_latest_state(service: Service) -> Union['State', None]:
        """attempts to get the latest state for a service"""
        latest = State.objects.filter(service=service.id, filed_at__lte=make_aware(datetime.utcnow())).order_by(
            '-filed_at').first()
        if latest is None:
            latest = State(service=service, filed_at=make_aware(datetime.utcnow()), value=State.States.UP)
            log.warning(f"no state filed for [{service}] yet")
            latest.save()
        return latest

    @staticmethod
    def get_recent_states(service: Service, limit: int = 5) -> List['State']:
        """returns recent states for a service"""
        return State.objects.filter(service_id__exact=service.id, filed_at__lte=make_aware(datetime.utcnow())).order_by(
            '-filed_at')[:limit]


class StateComment(models.Model):
    """comments for updates about a given state"""
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_created=True)
    edited_at = models.DateTimeField(auto_now=True)
    edited = models.BooleanField(default=False)
    content = models.CharField("user comments", max_length=2048)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.id is not None:
            origin = StateComment.objects.get(self.id)
            if origin is not None:
                self.edited = True
        else:
            self.created_at = make_aware(datetime.utcnow())
            self.edited_at = make_aware(datetime.utcnow())
        user = get_request().user
        self.user = user
        return super(StateComment, self).save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    @staticmethod
    def get_comments(state: State) -> List['StateComment']:
        return StateComment.objects.filter(state=state).order_by('-created_at')


class StateChange(models.Model):
    """tracks changes to states"""
    class ChangeTypes(models.TextChoices):
        SERVICE_CHANGE = 'service_change', text('Changed Service')
        VALUE_CHANGE = 'value_change', text('Changed State')
        FILED_AT = 'filed_at', text('Filed Time')
        FORECAST = 'forecast', text('Update Forecast Changed')
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    change_type = models.CharField(choices=ChangeTypes.choices, max_length=128)
    old_value = models.CharField("the original value of the state property", max_length=2048)
    new_value = models.CharField("the current value of the state property", max_length=2048)
