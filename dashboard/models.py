from django.db import models


# Create your models here.


class Service(models.Model):
    """a technical service that makes up a capability"""
    name = models.CharField("friendly name of a service", max_length=256)
    is_capability = models.BooleanField("if true makes the service a capability which is a business deliverable",
                                        default=False)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Relation(models.Model):
    """Maps a relationship between two entities"""
    DEPENDS_ON = 'depends_on'
    DEPENDENT = 'dependent'
    RELATION_CHOICES = [
        (DEPENDS_ON, 'Depends On'),
        (DEPENDENT, 'Dependent'),
    ]
    origin = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='origin_service')
    destination = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='destination_service')
    relation_type = models.CharField(choices=RELATION_CHOICES, default=DEPENDS_ON, max_length=128)

    def __str__(self):
        direction: str
        if self.relation_type == self.DEPENDENT:
            direction = "<-<"
        elif self.relation_type == self.DEPENDS_ON:
            direction = ">->"
        else:
            direction = "<->"
        return f"{self.origin.name} {direction} {self.destination.name}"


class State(models.Model):
    """a state is a way a service could be, like 'DOWN' or 'UP'"""
    UP = 'up'
    DOWN = 'down'
    MAINTENANCE_PLANNED = 'planned_maintenance'
    MAINTENANCE_UNPLANNED = 'unplanned_maintenance'
    DEGRADED_WARNING = 'degraded_warning'
    DEGRADED_CRITICAL = 'degraded_critical'
    VALUE_CHOICES = [
        (UP, 'Up'),
        (DOWN, 'Down'),
        (MAINTENANCE_PLANNED, 'Planned Maintenance'),
        (MAINTENANCE_UNPLANNED, 'Unplanned Maintenance'),
        (DEGRADED_WARNING, 'Degraded - Warning'),
        (DEGRADED_CRITICAL, 'Degraded - Critical'),
    ]
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    value = models.CharField(choices=VALUE_CHOICES, default=UP, max_length=128)
    filed_at = models.DateTimeField(auto_created=True)

    def __str__(self):
        return self.value
