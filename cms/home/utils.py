from django.shortcuts import redirect, render
from rest_framework import status

from errors.models import NotFoundError


def redirect_to_landing():
    return redirect('/')


def redirect_to_examination(examination_id):
    return redirect('/cases/%s/patient-details' % examination_id)


def redirect_to_login():
    return redirect('/login')


def redirect_to_landing_with_filters(location, person, status):
    url = '/?'
    if location:
        url = "%slocation=%s&" % (url, location)

    if person:
        url = "%sperson=%s&" % (url, person)

    if status:
        url = "%sstatus=%s&" % (url, status)

    return redirect(url[:-1])


def render_error(request, user, error):
    context = {
        'session_user': user,
        'error': error,
    }
    return render(request, 'errors/base_error.html', context, status=error.status_code)


def render_404(request, user, entity_name=''):
    context = {
        'session_user': user,
        'error': NotFoundError(entity_name),
    }
    return render(request, 'errors/base_error.html', context, status=status.HTTP_404_NOT_FOUND)
