from django import template
import json

register = template.Library()

@register.filter
def display_json_keys_values(json_field):
    try:
        data = json.loads(json_field)
        output = ''
        for key, value in data.items():
            output += f'{key}: {value}<br>'
        return output
    except (ValueError, TypeError):
        return json_field or ''