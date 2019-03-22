import json

from django.conf import settings

from medexCms.models import MedexRequest
from medexCms.test import mocks


def get_coroner_statuses_list():
    return [{'status': 'blocked'}]


def post_examination_team(examination_id, medical_examiner, medical_examiners_officer, auth_token):
    if settings.LOCAL:
        if medical_examiner.user_id == 1:
            return mocks.UNSUCCESSFUL_POST_EXAMINATION_TEAM
        else:
            return mocks.SUCCESSFUL_POST_EXAMINATION_TEAM
    else:
        payload = {
            'medical_examiner': medical_examiner.user_id,
            'medical_examiner_officer': medical_examiners_officer.user_id,
        }
        return MedexRequest.post(auth_token,
                                 url='%s/examinations/%s/examination-team' % (settings.API_URL, examination_id),
                                 data=payload)


def post_new_examination(examination_object, auth_token):
    return MedexRequest.post(auth_token, '%s/cases/create' % settings.API_URL, json.dumps(examination_object))


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
