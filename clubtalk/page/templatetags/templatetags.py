from django import template

register = template.Library()

@register.filter(name='mail')
def mail(mail):
    return "mailto:" + mail