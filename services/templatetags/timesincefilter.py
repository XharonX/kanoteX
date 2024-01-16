from django import template
from datetime import datetime, timedelta, timezone
from dateutil import relativedelta
from django.utils.timesince import timesince

register = template.Library()

@register.filter
def fivedaysago(date):
    today = datetime.now().astimezone(date.tzinfo)
    delta = today - date
    if timedelta(days=0) < delta < timedelta(days=2):
        return 'yesterday'
    elif delta < timedelta(days=1):
        return 'today'
    elif timedelta(days=2) < delta < timedelta(days=5):
        return str(delta.days) + 'days ago'
    else:
        return ' '
@register.filter
def months_since(value):
    try:
        today = datetime.now()
        today = today.astimezone(value.tzinfo)
        delta = relativedelta.relativedelta(dt1=today, dt2=value)
        time_slip = delta.years * 12 + delta.months
        return time_slip
    except ValueError:
        return 'infinity timeline'
