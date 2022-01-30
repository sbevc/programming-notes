from django.contrib.auth.models import AnonymousUser as DjangoAnonymousUser

from .models import AnonymousUser


def default_anonymous_user(get_response):
    def middleware(request):
        if isinstance(request.user, DjangoAnonymousUser):
            request.user = AnonymousUser()
        response = get_response(request)

        return response
    return middleware
