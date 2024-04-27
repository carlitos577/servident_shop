from django import template

register = template.Library()

@register.filter(name='is_base64')
def is_base64(value):
    try:
        # Intenta decodificar el valor como base64
        _ = value.encode('utf-8')
        return True
    except:
        return False
