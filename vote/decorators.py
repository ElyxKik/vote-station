from functools import wraps
from django.http import HttpResponseForbidden

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user

        if user.is_authenticated and user.is_admin:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("Accès refusé. Vous n'êtes pas administrateur.")

    return _wrapped_view
