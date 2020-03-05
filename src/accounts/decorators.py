from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return view_func(request, *args, **kwargs)

    return wrapper

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
                print(group)
            if group not in allowed_roles:
                return HttpResponse("You are not authorized to view this page.")
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def admin_only(view_func):
    def wrapper(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == "customer":
            return redirect('user-page')

        if group == "admin":
            return view_func(request, *args, **kwargs)
            
    return wrapper
