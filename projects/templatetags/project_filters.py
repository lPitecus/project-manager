from django import template

register = template.Library()


@register.filter
def status_to_bootstrap_class(status):
    status_classes = {
        "TODO": "secondary",
        "IN PROGRESS": "primary",
        "PAUSED": "warning",
        "DONE": "success",
        "CANCELED": "danger",
    }
    return status_classes.get(status, "secondary")
