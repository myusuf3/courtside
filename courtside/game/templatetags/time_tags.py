from django import template

from delorean import parse

register = template.Library()

def localize_datetime(timezone, string):
    gametime = parse(string)
    gametime.shift(timezone)
    return gametime.datetime.strftime("%Y-%m-%d %I:%M %p")

@register.simple_tag(takes_context=True)
def localize_time(context, string):
    string = str(string)
    timezone = context['timezone']
    return localize_datetime(timezone, string)