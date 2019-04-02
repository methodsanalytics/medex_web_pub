from rest_framework import status
from datetime import datetime, timedelta

from medexCms.utils import parse_datetime, is_empty_date
from people.models import BereavedRepresentative
from users.utils import get_user_presenter

from . import request_handler


class Examination:

    def __init__(self, obj_dict=None):
        if obj_dict:
            self.id = obj_dict.get("id")
            self.time_of_death = obj_dict.get("timeOfDeath")
            self.given_names = obj_dict.get("givenNames")
            self.surname = obj_dict.get("surname")
            self.nhs_number = obj_dict.get("nhsNumber")
            self.hospital_number_1 = obj_dict.get("hospitalNumber_1")
            self.hospital_number_2 = obj_dict.get("hospitalNumber_2")
            self.hospital_number_3 = obj_dict.get("hospitalNumber_3")
            self.gender = obj_dict.get("gender")
            self.gender_details = obj_dict.get("genderDetails")
            self.house_name_number = obj_dict.get("houseNameNumber")
            self.street = obj_dict.get("street")
            self.town = obj_dict.get("town")
            self.county = obj_dict.get("county")
            self.postcode = obj_dict.get("postcode")
            self.country = obj_dict.get("country")
            self.last_occupation = obj_dict.get("lastOccupation")
            self.organisation_care_before_death_locationId = obj_dict.get("organisationCareBeforeDeathLocationId")
            self.death_occurred_location_id = obj_dict.get("deathOccuredLocationId")
            self.mode_of_disposal = obj_dict.get("modeOfDisposal")
            self.funeral_directors = obj_dict.get("funeralDirectors")
            self.personal_affects_collected = obj_dict.get("personalAffectsCollected")
            self.personal_affects_details = obj_dict.get("personalAffectsDetails")
            self.date_of_birth = obj_dict.get("dateOfBirth")
            self.date_of_death = obj_dict.get("dateOfDeath")
            self.faith_priority = obj_dict.get("faithPriority")
            self.child_priority = obj_dict.get("childPriority")
            self.coroner_priority = obj_dict.get("coronerPriority")
            self.cultural_priority = obj_dict.get("culturalPriority")
            self.other_priority = obj_dict.get("otherPriority")
            self.priority_details = obj_dict.get("priorityDetails")
            self.completed = obj_dict.get("completed")
            self.coroner_status = obj_dict.get("coronerStatus")
            self.representatives = obj_dict.get("representatives")
            self.out_of_hours = obj_dict.get('outOfHours')

    @classmethod
    def load_by_id(cls, examination_id, auth_token):
        response = request_handler.load_by_id(examination_id, auth_token)

        authenticated = response.status_code == status.HTTP_200_OK

        if authenticated:
            return Examination(response.json())
        else:
            return None


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

    def display_dod(self):
        return self.date_of_death.strftime(self.date_format) if self.date_of_death else 'D.O.D unknown'

    def display_dob(self):
        return self.date_of_birth.strftime(self.date_format) if self.date_of_birth else 'D.O.B unknown'

    def display_appointment_date(self):
        return self.appointment_date.strftime(self.date_format) if self.appointment_date else None

    def calc_age(self):
        if self.date_of_birth and self.date_of_death:
            return self.date_of_death.year - self.date_of_birth.year - (
                    (self.date_of_death.month, self.date_of_death.day) < (
                self.date_of_birth.month, self.date_of_birth.day))
        else:
            return 0

    def calc_last_admission_days_ago(self):
        if self.last_admission:
            delta = datetime.now() - self.last_admission
            return delta.days
        else:
            return 0

    def calc_created_days_ago(self):
        if self.case_created_date:
            delta = datetime.now() - self.case_created_date
            return delta.days
        else:
            return 0

    def urgent(self):
        return True if self.urgency_score and self.urgency_score > 0 else False


class PatientDetails:

    def __init__(self, obj_dict, modes_of_disposal={}):
        self.modes_of_disposal = modes_of_disposal

        self.id = obj_dict.get("id")

        self.completed = obj_dict.get("completed")
        self.coroner_status = obj_dict.get("coronerStatus")

        self.given_names = obj_dict.get("givenNames")
        self.surname = obj_dict.get("surname")
        self.gender = obj_dict.get("gender").lower()
        self.gender_details = obj_dict.get("genderDetails")
        self.nhs_number = obj_dict.get("nhsNumber")
        self.hospital_number_1 = obj_dict.get("hospitalNumber_1")
        self.hospital_number_2 = obj_dict.get("hospitalNumber_2")
        self.hospital_number_3 = obj_dict.get("hospitalNumber_3")
        self.time_of_death = obj_dict.get("timeOfDeath")
        self.death_occurred_location_id = obj_dict.get("placeDeathOccured")
        self.medical_examiner_office_responsible = obj_dict.get("medicalExaminerOfficeResponsible")
        self.out_of_hours = obj_dict.get("outOfHours")

        self.house_name_number = obj_dict.get("houseNameNumber")
        self.street = obj_dict.get("street")
        self.town = obj_dict.get("town")
        self.county = obj_dict.get("county")
        self.country = obj_dict.get("country")
        self.postcode = obj_dict.get("postCode")
        self.last_occupation = obj_dict.get("lastOccupation")
        self.organisation_care_before_death_location_id = obj_dict.get("organisationCareBeforeDeathLocationId")
        self.any_implants = 'true' if obj_dict.get("anyImplants") else 'false'
        self.implant_details = obj_dict.get("implantDetails")
        self.funeral_directors = obj_dict.get("funeralDirectors")
        self.any_personal_effects = 'true' if obj_dict.get("anyPersonalEffects") else 'false'
        self.personal_affects_details = obj_dict.get("personalEffectDetails")

        self.cultural_priority = 'true' if obj_dict.get("culturalPriority") else 'false'
        self.faith_priority = 'true' if obj_dict.get("faithPriority") else 'false'
        self.child_priority = 'true' if obj_dict.get("childPriority") else 'false'
        self.coroner_priority = 'true' if obj_dict.get("coronerPriority") else 'false'
        self.other_priority = 'true' if obj_dict.get("otherPriority") else 'false'
        self.priority_details = obj_dict.get("priorityDetails")

        if not is_empty_date(obj_dict.get("dateOfBirth")):
            self.date_of_birth = parse_datetime(obj_dict.get("dateOfBirth"))
            self.day_of_birth = self.date_of_birth.day
            self.month_of_birth = self.date_of_birth.month
            self.year_of_birth = self.date_of_birth.year
        else:
            self.date_of_birth = None
            self.day_of_birth = None
            self.month_of_birth = None
            self.year_of_birth = None

        if not is_empty_date(obj_dict.get("dateOfDeath")):
            self.date_of_death = parse_datetime(obj_dict.get("dateOfDeath"))
            self.day_of_death = self.date_of_death.day
            self.month_of_death = self.date_of_death.month
            self.year_of_death = self.date_of_death.year
        else:
            self.date_of_death = None
            self.day_of_death = None
            self.month_of_death = None
            self.year_of_death = None

        self.mode_of_disposal = ''
        for key, value in self.modes_of_disposal.items():
            if value == obj_dict.get("modeOfDisposal"):
                self.mode_of_disposal = key

        self.representatives = []
        for representative in obj_dict.get("representatives"):
            self.representatives.append(BereavedRepresentative(representative))

    @classmethod
    def load_by_id(cls, examination_id, auth_token):
        response = request_handler.load_patient_details_by_id(examination_id, auth_token)

        authenticated = response.status_code == status.HTTP_200_OK

        if authenticated:
            modes_of_disposal = request_handler.load_modes_of_disposal(auth_token)
            return PatientDetails(response.json(), modes_of_disposal)
        else:
            return None


class CaseBreakdown:

    def __init__(self, obj_dict, medical_team):

        self.timeline_items = obj_dict.get('events')
        self.patient_name = obj_dict.get("patientName")
        self.nhs_number = obj_dict.get("nhsNumber")
        self.date_of_death = obj_dict.get("dateOfDeath")
        self.time_of_death = obj_dict.get("timeOfDeath")
        self.events = []

        self.medical_team = medical_team
        self.qap_discussion = CaseBreakdownQAPDiscussion.from_data(medical_team, self.get_latest_cause_of_death(),
                                                                   self.get_qap_discussion_draft())
        self.latest_admission = CaseBreakdownLatestAdmission.from_data(self.get_latest_admission_draft())

        for item in self.timeline_items:
            self.events.append(CaseEvent(len(self.events) + 1, item.get('latest')))

    @classmethod
    def load_by_id(cls, auth_token, examination_id):
        response = request_handler.load_case_breakdown_by_id(examination_id, auth_token)
        medical_team = MedicalTeam.load_by_id(examination_id, auth_token)

        if response.status_code == status.HTTP_200_OK:
            return CaseBreakdown(response.json(), medical_team)
        else:
            return None

    def get_latest_cause_of_death(self):
        return None

    def get_qap_discussion_draft(self):
        return None

    def get_latest_admission_draft(self):
        return None


class CaseBreakdownLatestAdmission:
    def __init__(self):
        self.day_of_last_admission = ''
        self.month_of_last_admission = ''
        self.year_of_last_admission = ''
        self.date_of_last_admission_unknown = False

        self.time_of_last_admission = ''
        self.time_of_last_admission_unknown = False

        self.latest_admission_notes = ''
        self.suspect_referral = ''

    @classmethod
    def from_data(cls, draft=None):
        latest_admission = CaseBreakdownLatestAdmission()
        if draft is not None:
            try:
                latest_admission.day_of_last_admission = draft['day_of_last_admission']
                latest_admission.month_of_last_admission = draft['month_of_last_admission']
                latest_admission.year_of_last_admission = draft['year_of_last_admission']
                latest_admission.date_of_last_admission_unknown = draft['date_of_last_admission_unknown']
                latest_admission.time_of_last_admission = draft['time_of_last_admission']
                latest_admission.time_of_last_admission_unknown = draft['time_of_last_admission_unknown']
                latest_admission.latest_admission_notes = draft['latest_admission_notes']
                latest_admission.suspect_referral = draft['suspect_referral']

            except KeyError:
                print('Could not parse latest admission object')

        return latest_admission

    def to_object(self):
        return {
            'day_of_last_admission': self.day_of_last_admission,
            'month_of_last_admission': self.month_of_last_admission,
            'year_of_last_admission': self.year_of_last_admission,
            'date_of_last_admission_unknown': self.date_of_last_admission_unknown,
            'time_of_last_admission': self.time_of_last_admission,
            'time_of_last_admission_unknown': self.time_of_last_admission_unknown,
            'latest_admission_notes': self.latest_admission_notes,
            'suspect_referral': self.suspect_referral,
        }


class CaseBreakdownQAPDiscussion:

    def __init__(self):
        self.default_qap = None
        self.use_default_qap = False

        self.alternate_qap = MedicalTeamMember()
        self.cause_of_death = None

        self.day_of_conversation = ''
        self.month_of_conversation = ''
        self.year_of_conversation = ''
        self.time_of_conversation = ''

        self.details = ''
        self.outcome = ''

    @classmethod
    def from_data(cls, medical_team=None, cause_of_death=None, qap_draft=None):
        qap_discussion = CaseBreakdownQAPDiscussion()

        cls.__set_default_qap(medical_team, qap_discussion, qap_draft)

        qap_discussion.cause_of_death = cause_of_death

        cls.__load_qap_draft(qap_discussion, qap_draft)

        return qap_discussion

    @classmethod
    def __load_qap_draft(cls, qap_discussion, qap_draft):
        if qap_draft is not None:
            try:
                qap_discussion.use_default_qap = qap_draft['use_default_qap']
                qap_discussion.alternate_qap = MedicalTeamMember.from_dict(qap_draft['alternate_qap'])
                qap_discussion.day_of_conversation = qap_draft['day_of_conversation']
                qap_discussion.month_of_conversation = qap_draft['month_of_conversation']
                qap_discussion.year_of_conversation = qap_draft['year_of_conversation']
                qap_discussion.time_of_conversation = qap_draft['time_of_conversation']
                qap_discussion.details = qap_draft['details']
                qap_discussion.outcome = qap_draft['outcome']

            except KeyError:
                print('Could not parse qap draft object')

    @classmethod
    def __set_default_qap(cls, medical_team, qap_discussion, qap_draft):
        if medical_team is not None and medical_team.qap is not None and medical_team.qap.name != '':
            qap_discussion.default_qap = medical_team.qap

            if qap_draft is None:
                qap_discussion.use_default_qap = True

    def to_object(self):
        return {
            'default_qap': self.default_qap.to_object(),
            'alternate_qap': self.alternate_qap.to_object(),
            'cause_of_death': self.cause_of_death.to_object(),
            'day_of_conversation': self.day_of_conversation,
            'month_of_conversation': self.month_of_conversation,
            'year_of_conversation': self.year_of_conversation,
            'time_of_conversation': self.time_of_conversation,
            'details': self.details,
            'outcome': self.outcome
        }


class CauseOfDeathProposal:

    def __init__(self):
        from users.models import User

        self.medical_examiner = User()
        self.creation_date = ''
        self.section_1a = ''
        self.section_1b = ''
        self.section_1c = ''
        self.section_2 = ''

    def to_object(self):
        return {
            'medical_examiner': get_user_presenter(self.medical_examiner),
            'creation_date': self.creation_date,
            'section_1a': self.section_1a,
            'section_1b': self.section_1b,
            'section_1c': self.section_1c,
            'section_2': self.section_2
        }


class CaseEvent:
    date_format = '%d.%m.%Y'
    time_format = "%H:%M"

    def __init__(self, number, obj_dict):
        self.number = number
        self.type = obj_dict.get('type')
        self.user_name = obj_dict.get('user').get('name')
        self.user_role = obj_dict.get('user').get('role')
        self.created_date = obj_dict.get('createdDate')
        self.body = obj_dict.get('body')

    def display_date(self):
        date = parse_datetime(self.created_date)
        if date.date() == datetime.today().date():
            return 'Today at %s' % date.strftime(self.time_format)
        elif date.date() == datetime.today().date() - timedelta(days=1):
            return 'Yesterday at %s' % date.strftime(self.time_format)
        else:
            time = date.strftime(self.time_format)
            date = date.strftime(self.date_format)
            return "%s at %s" % (date, time)


class MedicalTeam:

    def __init__(self, obj_dict):
        from users.models import User

        self.consultant_responsible = MedicalTeamMember.from_dict(
            obj_dict['consultantResponsible']) if 'consultantResponsible' in obj_dict else None
        self.qap = MedicalTeamMember.from_dict(obj_dict['qap']) if 'qap' in obj_dict else None
        self.general_practitioner = MedicalTeamMember.from_dict(
            obj_dict['generalPractitioner']) if 'generalPractitioner' in obj_dict else None

        if "consultantsOther" in obj_dict:
            self.consultants_other = [MedicalTeamMember.from_dict(consultant) for consultant in
                                      obj_dict['consultantsOther']]
        else:
            self.consultants_other = []

        self.nursing_team_information = obj_dict[
            'nursingTeamInformation'] if 'nursingTeamInformation' in obj_dict else ''

        self.medical_examiner = User(obj_dict['medicalExaminer']) if 'medicalExaminer' in obj_dict else None
        self.medical_examiners_officer = User(
            obj_dict['medicalExaminerOfficer']) if 'medicalExaminerOfficer' in obj_dict else None

    @classmethod
    def load_by_id(cls, examination_id, auth_token):
        response = request_handler.load_medical_team_by_id(examination_id, auth_token)

        authenticated = response.status_code == status.HTTP_200_OK

        if authenticated:
            return MedicalTeam(response.json())
        else:
            return None


class MedicalTeamMember:

    def __init__(self, name='', role='', organisation='', phone_number='', notes=''):
        self.name = name.strip() if name else ''
        self.role = role
        self.organisation = organisation
        self.phone_number = phone_number
        self.notes = notes

    @staticmethod
    def from_dict(obj_dict):
        name = obj_dict['name'] if 'name' in obj_dict else ''
        role = obj_dict['role'] if 'role' in obj_dict else ''
        organisation = obj_dict['organisation'] if 'organisation' in obj_dict else ''
        phone_number = obj_dict['phone'] if 'phone' in obj_dict else ''
        notes = obj_dict['notes'] if 'notes' in obj_dict else ''
        return MedicalTeamMember(name=name, role=role, organisation=organisation, phone_number=phone_number,
                                 notes=notes)

    def has_name(self):
        return self.name and len(self.name.strip()) > 0

    def has_valid_name(self):
        return len(self.name.strip()) < 250

    def has_name_if_needed(self):
        if text_field_is_not_null(self.role) or text_field_is_not_null(self.organisation) or text_field_is_not_null(
                self.phone_number):
            return text_field_is_not_null(self.name)
        else:
            return True

    def to_object(self):
        return {
            "name": self.name,
            "role": self.role,
            "organisation": self.organisation,
            "phone": self.phone_number,
            "notes": self.notes
        }


def text_field_is_not_null(field):
    return field and len(field.strip()) > 0
