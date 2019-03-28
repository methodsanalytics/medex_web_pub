from django.conf import settings

from medexCms.models import MedexRequest
from medexCms.test import mocks


def load_trusts_list(auth_token):
    if settings.LOCAL:
        return mocks.SUCCESSFUL_TRUST_LOAD
    else:
        return MedexRequest.get(auth_token, "%s/locations" % settings.API_URL).json()['locations']


def load_region_list(auth_token):
    if settings.LOCAL:
        return mocks.SUCCESSFUL_REGION_LOAD
    else:
        return MedexRequest.get(auth_token, "%s/locations" % settings.API_URL).json()['locations']


def get_locations_list(auth_token):
    if settings.LOCAL:
        return mocks.SUCCESSFUL_TRUST_LOAD
    else:
        return MedexRequest.get(auth_token, "%s/locations" % settings.API_URL).json()['locations']


def get_me_offices_list(auth_token):
    if settings.LOCAL:
        return mocks.SUCCESSFUL_ME_OFFICES_LOAD
    else:
        return MedexRequest.get(auth_token, "%s/locations" % settings.API_URL).json()['locations']


def get_permitted_locations_list(auth_token):
    if settings.LOCAL:
        return mocks.SUCCESSFUL_TRUST_LOAD
    else:
        return MedexRequest.get(auth_token, "%s/locations" % settings.API_URL).json()['locations']


def get_permitted_users(auth_token, location_id):
    if settings.LOCAL:
        return mocks.SUCCESSFUL_MEDICAL_EXAMINERS
    else:
        # TODO update to the right end point once we have it
        return MedexRequest.get(auth_token, "%s/users/medical_examiners" % settings.API_URL).json()
