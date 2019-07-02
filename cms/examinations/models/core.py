from datetime import datetime, timedelta, timezone

from errors.models import GenericError
from errors.utils import log_api_error
from medexCms.api import enums

from medexCms.utils import parse_datetime

from examinations import request_handler


class Examination:

    def __init__(self, form_data=None, examination_id=None):
        self.id = None
        self.time_of_death = None
        self.given_names = None
        self.surname = None
        self.nhs_number = None
        self.hospital_number_1 = None
        self.hospital_number_2 = None
        self.hospital_number_3 = None
        self.gender = None
        self.gender_details = None
        self.house_name_number = None
        self.street = None
        self.town = None
        self.county = None
        self.postcode = None
        self.country = None
        self.last_occupation = None
        self.organisation_care_before_death_locationId = None
        self.place_of_death = None
        self.me_office = None
        self.mode_of_disposal = None
        self.funeral_directors = None
        self.personal_affects_collected = None
        self.personal_affects_details = None
        self.date_of_birth = None
        self.date_of_death = None
        self.faith_priority = None
        self.child_priority = None
        self.coroner_priority = None
        self.cultural_priority = None
        self.other_priority = None
        self.priority_details = None
        self.completed = None
        self.coroner_status = None
        self.representatives = None
        self.out_of_hours = None

        if form_data:
            self.fill_from_form(form_data, examination_id)

    def fill_from_form(self, obj_dict, examination_id):
        self.id = examination_id if examination_id else obj_dict.get("id")
        self.given_names = obj_dict.get("givenNames")
        self.surname = obj_dict.get("surname")
        self.gender = obj_dict.get("gender")
        self.gender_details = obj_dict.get("genderDetails")
        self.place_of_death = obj_dict.get("placeDeathOccured")
        self.me_office = obj_dict.get("medicalExaminerOfficeResponsible")
        self.nhs_number = obj_dict.get("nhsNumber")
        self.hospital_number_1 = obj_dict.get("hospitalNumber_1")
        self.hospital_number_2 = obj_dict.get("hospitalNumber_2")
        self.hospital_number_3 = obj_dict.get("hospitalNumber_3")
        self.date_of_birth = obj_dict.get("dateOfBirth")
        self.date_of_death = obj_dict.get("dateOfDeath")
        self.time_of_death = obj_dict.get("timeOfDeath")

    @classmethod
    def create(cls, submission, auth_token):
        examination = None
        error = None
        response = request_handler.post_new_examination(submission, auth_token)

        if response.ok:
            examination = Examination(submission, response.json().get('examinationId'))
        else:
            log_api_error('case creation', response.text)
            error = GenericError(response, {"action": "create", "type": "case"})

        return examination, error


class ExaminationOverview:
    date_format = '%d.%m.%Y'

    def __init__(self, obj_dict):
        self.urgency_score = obj_dict.get("urgencyScore")
        self.given_names = obj_dict.get("givenNames")
        self.surname = obj_dict.get("surname")
        self.nhs_number = obj_dict.get("nhsNumber")
        self.id = obj_dict.get("examinationId")
        self.time_of_death = obj_dict.get("timeOfDeath")
        self.date_of_birth = parse_datetime(obj_dict.get("dateOfBirth"))
        self.date_of_death = parse_datetime(obj_dict.get("dateOfDeath"))
        self.appointment_date = parse_datetime(obj_dict.get("appointmentDate"))
        self.appointment_time = obj_dict.get("appointmentTime")
        self.last_admission = parse_datetime(obj_dict.get("lastAdmission"))
        self.case_created_date = parse_datetime(obj_dict.get("caseCreatedDate"))
        self.open = obj_dict.get('open')

    def calc_last_admission_days_ago(self):
        if self.last_admission:
            # TODO Remove this conditional when we date consistency
            if self.last_admission.tzinfo is None:
                delta = datetime.now() - self.last_admission
            else:
                delta = datetime.now(timezone.utc) - self.last_admission
            return delta.days
        else:
            return 0

    def calc_created_days_ago(self):
        if self.case_created_date:
            # TODO Remove this conditional when we date consistency
            if self.case_created_date.tzinfo is None:
                delta = datetime.now() - self.case_created_date
            else:
                delta = datetime.now(timezone.utc) - self.case_created_date
            return delta.days
        else:
            return 0

    def calc_age(self):
        if self.date_of_death and self.date_of_birth:
            return self.date_of_death.year - self.date_of_birth.year - (
                (self.date_of_death.month, self.date_of_death.day) < (self.date_of_birth.month, self.date_of_birth.day))
        else:
            return None

    def urgent(self):
        return True if self.urgency_score and self.urgency_score > 0 and self.open else False


class CauseOfDeathProposal:
    date_format = '%d.%m.%Y'
    time_format = "%H:%M"

    def __init__(self):
        from users.models import User

        self.medical_examiner = User()
        self.qap = None
        self.status = enums.cod_status.NOT_DISCUSSED
        self.creation_date = ''
        self.section_1a = ''
        self.section_1b = ''
        self.section_1c = ''
        self.section_2 = ''

    # TODO confirm this function is unneeded
    # def to_object(self):
    #     return {
    #         'medical_examiner': get_user_presenter(self.medical_examiner),
    #         'creation_date': self.creation_date,
    #         'qap': get_medical_team_member_presenter(self.qap),
    #         'status': self.status,
    #         'section_1a': self.section_1a,
    #         'section_1b': self.section_1b,
    #         'section_1c': self.section_1c,
    #         'section_2': self.section_2
    #     }

    def display_date(self):
        if self.creation_date:
            date = parse_datetime(self.creation_date)
            if date.date() == datetime.today().date():
                return 'Today at %s' % date.strftime(self.time_format)
            elif date.date() == datetime.today().date() - timedelta(days=1):
                return 'Yesterday at %s' % date.strftime(self.time_format)
            else:
                time = date.strftime(self.time_format)
                date = date.strftime(self.date_format)
                return "%s at %s" % (date, time)
        else:
            return None
