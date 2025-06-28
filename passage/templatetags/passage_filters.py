from datetime import datetime
from django import template
register = template.Library()

@register.filter(name='make_it_short')
def make_it_short(text, arg):
    return ' '.join(text.split(' ')[:arg]) + '....'