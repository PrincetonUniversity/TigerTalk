from django.http import HttpResponseRedirect
from django.urls import reverse

def CAS_login_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('login'))
    wrap.__doc__= function.__doc__
    wrap.__name__= function.__name__
    return wrap