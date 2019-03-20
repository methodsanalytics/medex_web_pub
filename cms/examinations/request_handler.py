import json

from django.conf import settings

from medexCms.models import MedexRequest
from medexCms.test import mocks


def get_coroner_statuses_list():
    return [{'status': 'blocked'}]


def post_new_examination(examination_object, auth_token):
    return MedexRequest.post(auth_token, '%s/examinations' % settings.API_URL, json.dumps(examination_object))


def load_by_id(examination_id, auth_token):
    if settings.LOCAL:
        return mocks.SUCCESSFUL_CASE_LOAD
    else:
        return MedexRequest.get(auth_token, '%s/examinations/%s' % (settings.API_URL, examination_id))


def load_examinations_index(params, auth_token):
    if settings.LOCAL:
        return mocks.SUCCESSFUL_CASE_INDEX
    else:
        return MedexRequest.post(auth_token, '%s/examinations' % settings.API_URL, params)


def load_patient_details_by_id(examination_id, auth_token):
    if settings.LOCAL:
        return mocks.SUCCESSFUL_CASE_LOAD
    else:
        return MedexRequest.get(auth_token, '%s/examinations/%s/patientdetails' % (settings.API_URL, examination_id))


def update_patient_details(examination_id, submission, auth_token):
    return MedexRequest.put(auth_token, '%s/examinations/%s/patientdetails' % (settings.API_URL, examination_id),
                            submission)
