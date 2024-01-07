from django import template
from datetime import datetime, timedelta, timezone
from dateutil import relativedelta
from django.utils.timesince import timesince

register = template.Library()

@register.filter
def fivedaysago(date):
    today = datetime.today()

    delta = today - date
    if delta < timedelta(days=5):
        return timesince(date) + 'ago'
    return date.strftime('%d-%m-%Y')

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
