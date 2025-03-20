from django.shortcuts import redirect, get_object_or_404

from marketplace.models import Picture

def login_required(url='/login/'):

    def decorator(func):

        def inner_func(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect(url)

            return func(request, *args, **kwargs)

        return inner_func

    return decorator


def is_owner(func):
    def inner_func(request, *args, **kwargs):
        user = request.user
        picture = get_object_or_404(Picture, id=kwargs.get('id'))

        if picture.user != user:
            return redirect('/marketplace/')

        return func(request, *args, **kwargs)

    return inner_func