from django import template

register = template.Library()

@register.filter
def default_profile_pic(profile_pic):
    return profile_pic if profile_pic else 'default_profile.jpg'

