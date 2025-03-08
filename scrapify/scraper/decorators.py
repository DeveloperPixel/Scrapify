from django.shortcuts import redirect
from functools import wraps


def firebase_login_required(view_func):
    """
    Custom decorator to check if the user is logged in using Firebase.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if 'uid' not in request.session:
            next_url = request.path
            request.session['next_url'] = next_url
            # If user is not logged in, redirect to login page with next URL
            return redirect(f'/accounts/dual/?next={next_url}')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
