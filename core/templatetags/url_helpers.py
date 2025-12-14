from django import template
from urllib.parse import urlencode

register = template.Library()


@register.simple_tag
def query_string(request, exclude_keys=None, **kwargs):
    if exclude_keys is None:
        exclude_keys = []
    elif isinstance(exclude_keys, str):
        exclude_keys = [k.strip() for k in exclude_keys.split(",")]

    params = {}

    for key, value in request.GET.items():
        if key not in exclude_keys:
            params[key] = value

    for key, value in kwargs.items():
        if value is not None:
            params[key] = value

    return urlencode(params)
