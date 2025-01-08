# custom_permissions.py
from django import template

register = template.Library()

@register.filter
def has_role_permission(user, permission_codename):
    """
    Custom filter to check if the user has a specific role-based permission.
    """
    if user.is_authenticated and hasattr(user, 'has_permission'):
        return user.has_permission(permission_codename)
    return False
