from datetime import date, timedelta

from django import template

register = template.Library()


@register.filter
def fecha_amigable(value):
    hoy = date.today()
    if value.date() == hoy:
        return "Hoy"
    elif value.date() == hoy - timedelta(days=1):
        return "Ayer"
    else:
        return value.strftime("%d/%m/%Y")
