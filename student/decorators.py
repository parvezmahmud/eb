from django.shortcuts import redirect
from functools import wraps

def redirect_if_logged_in(view_func):
    """
    A decorator that redirects logged-in users to the home page.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')  # Replace 'home' with the name of your home page URL pattern
        return view_func(request, *args, **kwargs)
    return wrapper
