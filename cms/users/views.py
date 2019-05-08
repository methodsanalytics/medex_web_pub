from django.shortcuts import render, redirect

from rest_framework import status

from errors.utils import log_unexpected_method, log_api_error
from errors.views import __handle_method_not_allowed_error, __handle_not_permitted_error
from home.utils import redirect_to_login, render_404
from medexCms.utils import get_code_versions
from permissions.forms import PermissionBuilderForm

from .forms import CreateUserForm
from .models import User


def create_user(request):
    user = User.initialise_with_token(request)
    if not user.check_logged_in():
        return redirect_to_login()

    if not user.permitted_actions.can_invite_user:
        template, context, status_code = __handle_not_permitted_error(user)

    elif request.method == 'GET':
        template, context, status_code = __get_create_user(user)

    elif request.method == 'POST':
        template, context, status_code, redirect_response = __post_create_user(user, request.POST)

        if redirect_response:
            return redirect_response

    else:
        log_unexpected_method(request.method, 'create user')
        template, context, status_code = __handle_method_not_allowed_error(user)

    return render(request, template, context, status=status_code)


def __get_create_user(user):
    template = 'users/new.html'
    status_code = status.HTTP_200_OK
    context = __set_create_user_context(user, CreateUserForm(), False)
    return template, context, status_code


def __post_create_user(user, post_body):
    template = 'users/new.html'

    form = CreateUserForm(post_body)

    if form.validate():
        response = User.create(form.response_to_dict(), user.auth_token)

        if response.ok:
            return None, None, None, redirect('/users/%s/add_permission' % response.json()['userId'])
        else:
            log_api_error('user creation', response.text)
            status_code = response.status_code
    else:
        status_code = status.HTTP_400_BAD_REQUEST

    context = __set_create_user_context(user, form, True)
    return template, context, status_code, None


def __set_create_user_context(user, form, invalid):
    return {
        'session_user': user,
        'page_heading': 'Add a user',
        'form': form,
        'invalid': invalid,
        'version': get_code_versions(),
    }


def add_permission(request, user_id):
    user = User.initialise_with_token(request)
    if not user.check_logged_in():
        return redirect_to_login()

    managed_user = User.load_by_id(user_id, user.auth_token)
    if managed_user is None:
        return render_404(request, user, 'user')

    if not user.permitted_actions.can_create_user_permission:
        template, context, status_code = __handle_not_permitted_error(user)

    elif request.method == 'GET':
        template, context, status_code = __get_add_permission(user, managed_user)

    elif request.method == 'POST':
        template, context, status_code, redirect_response = __post_add_permission(user, managed_user, request.POST)

        if redirect_response:
            return redirect_response

    else:
        log_unexpected_method(request.method, 'add permission')
        template, context, status_code = __handle_method_not_allowed_error(user)

    return render(request, template, context, status=status_code)


def __get_add_permission(user, managed_user):
    template = 'users/permission_builder.html'
    status_code = status.HTTP_200_OK

    context = __set_add_permission_context(user, PermissionBuilderForm(), False, managed_user)
    return template, context, status_code


def __post_add_permission(user, managed_user, post_body):
    template = 'users/permission_builder.html'

    form = PermissionBuilderForm(post_body)
    add_another = True if post_body.get('add_another') == "true" else False

    if form.is_valid():
        response = managed_user.add_permission(form, user.auth_token)

        if response.ok:
            if add_another:
                return None, None, None, redirect('add_permission', user_id=managed_user.user_id)
            else:
                return None, None, None, redirect('/settings')
        else:
            log_api_error('permission creation', response.text)
            status_code = response.status_code

    else:
        status_code = status.HTTP_400_BAD_REQUEST

    context = __set_add_permission_context(user, form, True, managed_user)

    return template, context, status_code, None


def __set_add_permission_context(user, form, invalid, managed_user):
    trusts = user.get_permitted_trusts()
    regions = user.get_permitted_regions()

    return {
        'session_user': user,
        'sub_heading': 'Add role and permission level',
        'form': form,
        'submit_path': 'add_permission',
        'invalid': invalid,
        'trusts': trusts,
        'regions': regions,
        'managed_user': managed_user,
        'version': get_code_versions(),
    }
