from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.conf import settings

def role_permission_required(permission_codename):
    """
    Custom decorator to check permissions based on RoleModel.
    permission_codename: e.g., 'app.add_tablemodel'
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Check if the user is authenticated
            if not request.user.is_authenticated:
                messages.error(request, "You must be logged in to access this page.")
                # Redirect to the previous page or home if referer is not available
                return redirect(request.META.get('HTTP_REFERER', settings.LOGIN_URL))

            # Check if the user has the required permission via the RoleModel
            if request.user.has_permission(permission_codename.split('.')[-1]):
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, "You do not have permission to access this page.")
                # Redirect to the previous page or home if referer is not available
                return redirect(request.META.get('HTTP_REFERER', settings.LOGIN_URL))

        return _wrapped_view
    return decorator
