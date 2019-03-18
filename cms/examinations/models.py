from rest_framework import status
from datetime import datetime

from medexCms.utils import parse_datetime

from . import request_handler


class Examination():

    def __init__(self, obj_dict=None):
        if obj_dict:
            self.id = obj_dict.get("id")
            self.time_of_death = obj_dict.get("timeOfDeath")
            self.given_names = obj_dict.get("givenNames")
            self.surname = obj_dict.get("surname")
            self.nhs_number = obj_dict.get("nhsNumber")
            self.gender = obj_dict.get("gender")
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
            self.jewellery_collected = obj_dict.get("jewelleryCollected")
            self.jewellery_details = obj_dict.get("jewelleryDetails")
            self.date_of_birth = obj_dict.get("dateOfBirth")
            self.date_of_death = obj_dict.get("dateOfDeath")
            self.faith_priority = obj_dict.get("faithPriority")
            self.child_priority = obj_dict.get("childPriority")
            self.coroner_priority = obj_dict.get("coronerPriority")
            self.other_priority = obj_dict.get("otherPriority")
            self.priority_details = obj_dict.get("priorityDetails")
            self.completed = obj_dict.get("completed")
            self.coroner_status = obj_dict.get("coronerStatus")

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
        self.id = obj_dict.get("id")
        self.time_of_death = obj_dict.get("timeOfDeath")
        self.date_of_birth = parse_datetime(obj_dict.get("dateOfBirth"))
        self.date_of_death = parse_datetime(obj_dict.get("dateOfDeath"))
        self.appointment_date = obj_dict.get("appointmentDate")
        self.appointment_time = obj_dict.get("appointmentTime")
        self.last_admission = obj_dict.get("lastAdmission")
        self.case_created_date = obj_dict.get("caseCreatedDate")

    def display_dod(self):
        return self.date_of_death.strftime(self.date_format)

    def display_dob(self):
        return self.date_of_birth.strftime(self.date_format)
