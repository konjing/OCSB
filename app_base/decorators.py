""" Custom Decorator """
from django.http import HttpResponse

def allowed_users(allowed_roles=[]):
    """ Authorize depend on user group """
    def decorator(view_func):
        def warpper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view')
        return warpper_func
    return decorator
