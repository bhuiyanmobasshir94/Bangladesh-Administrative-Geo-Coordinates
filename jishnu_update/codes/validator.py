import json
from marshmallow import Schema, fields, pprint, ValidationError, validate, EXCLUDE, validates_schema
from base.fields import CustomString
from base.data_dictionaries import country_dict, district_dict, symptoms_dict, realtion_dict, gender_dict, diseases_dict, assistance_requested_list, introducer_type_list
from datetime import datetime

blank_error_massage = 'Field cannot be blank'
contact_number_error_massage = 'Field should have at least 11 digits'


class BaseSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True


class Relation(BaseSchema):
    code = CustomString(validate=validate.OneOf(choices=realtion_dict.keys(), labels=realtion_dict.values()),
                        required=True)
    description = CustomString()


class Address(BaseSchema):

    address_line = CustomString(required=True, validate=validate.Length(min=1, error=blank_error_massage))
    town = CustomString(required=True)
    police_station = CustomString(required=True)
    sub_district = CustomString(required=True)
    district = CustomString(validate=validate.OneOf(district_dict.keys(), labels=district_dict.values()), required=True)


class IntroducerDetails(BaseSchema):
    name = CustomString(required=True, validate=validate.Length(min=1, error=blank_error_massage))
    contact_number = CustomString(required=True, validate=validate.Length(min=1, error=blank_error_massage))
    introducer_type = CustomString(required=True, validate=validate.OneOf(choices=introducer_type_list))
    name_of_organization = CustomString()

    @validates_schema
    def validate_field(self, data, **kwargs):
        if data['introducer_type'] in ['Hospital/Clinic', 'Govt. Agency/Local Govt', 'NGO']:
            if 'name_of_organization' not in data:
                raise ValidationError("name_of_organization is required")
            elif data['name_of_organization'] == "":
                raise ValidationError("name_of_organization can not be emtpy")


class Country(BaseSchema):
    code = CustomString(validate=validate.OneOf(choices=country_dict.keys(), labels=country_dict.values()), required=True)
    description = CustomString()


class PersonalDetails(BaseSchema):
    name = CustomString(required=True, validate=validate.Length(min=1, error=blank_error_massage))
    passport_number = CustomString()
    nid_number = CustomString()
    gender = CustomString(
        validate=validate.OneOf(choices=gender_dict.keys(), labels=gender_dict.values()),
        required=True
    )
    age = fields.Float(validate=validate.Range(min=0), required=True)
    father_name = CustomString(required=True, validate=validate.Length(min=1, error=blank_error_massage))
    contact_number = CustomString(required=True, validate=validate.Length(min=1, error=blank_error_massage))
    email = CustomString()
    address = fields.Nested(Address, required=True)
    facbook_profile_url = CustomString()
    foreign_mobile_no = CustomString()

    country_of_origin = fields.Nested(Country, required=True)
    country_of_residence = fields.Nested(Country, required=True)

    @validates_schema
    def validate_field(self, data, **kwargs):

        if 'passport_number' in data and 'nid_number' in data:
            if data['passport_number'] == "" and data['nid_number'] == "":
                raise ValidationError("At least one field is required between passport_number and nid_number")
        elif 'passport_number' in data:
            if data['passport_number'] == "":
                raise ValidationError("passport_number can not be empty")
        elif 'nid_number' in data:
            if data['nid_number'] == "":
                raise ValidationError("nid_number can not be emtpy")
        else:
            raise ValidationError("At least one field is required between passport_number and nid_number")

class EmergencyContact(BaseSchema):
    name = CustomString(required=True, validate=validate.Length(min=1, error=blank_error_massage))
    relation = fields.Nested(Relation, required=True)
    contact_number = CustomString(required=True, validate=validate.Length(min=1, error=blank_error_massage))
    email = CustomString()


class Covid19Exposure(BaseSchema):
    been_exposed = fields.Boolean(required=True)
    date = fields.DateTime(format='%d/%m/%Y')

    @validates_schema
    def validate_fields(self, data, **kwargs):

        if data["been_exposed"] is True:
            if 'date' not in data:
                raise ValidationError("date field is required")
            elif data['date'] > datetime.today():
                raise ValidationError("date must not be future")


class IncomerExposure(BaseSchema):
    been_exposed = fields.Boolean(required=True)
    date = fields.DateTime(format='%d/%m/%Y')
    country = fields.Nested(Country)

    @validates_schema
    def validate_fields(self, data, **kwargs):

        if data["been_exposed"] is True:
            if 'date' not in data:
                raise ValidationError("date field is required")
            elif data['date'] > datetime.today():
                raise ValidationError("date must not be future")
            if 'country' not in data:
                raise ValidationError("country field is required")


class SymptomsInAbroadAffairs(BaseSchema):
    pre_arrival_symptom_presence = fields.Boolean(required=True)
    pre_arrival_symptom_date = fields.DateTime(format='%d/%m/%Y')
    been_treated = fields.Boolean(required=True)
    treatment_date = fields.DateTime(format='%d/%m/%Y')
    post_arrival_symptom_presence = fields.Boolean(required=True)
    post_arrival_symptom_date = fields.DateTime(format='%d/%m/%Y')

    @validates_schema
    def validate_field(self, data, **kwargs):
        if data['pre_arrival_symptom_presence'] is True:
            if 'pre_arrival_symptom_date' not in data:
                raise ValidationError('pre_arrival_symptom_date field is required')
            elif data['pre_arrival_symptom_date'] > datetime.today():
                raise ValidationError("date must not be future")

        if data['been_treated'] is True:
            if 'treatment_date' not in data:
                raise ValidationError('treatment_date field is required')
            elif data['treatment_date'] > datetime.today():
                raise ValidationError("date must not be future")

        if data['post_arrival_symptom_presence'] is True:
            if 'post_arrival_symptom_date' not in data:
                raise ValidationError('post_arrival_symptom_date field is required')
            elif data['post_arrival_symptom_date'] > datetime.today():
                raise ValidationError("date must not be future")


class Transits(BaseSchema):
    country = fields.Nested(Country, required=True)
    period_in_hours = fields.Float(validate=validate.Range(min=0), required=True)


class TravelCompanions(BaseSchema):
    name = CustomString(required=True, validate=validate.Length(min=1, error=blank_error_massage))
    age = fields.Float(validate=validate.Range(min=0), required=True)
    passport_number = CustomString(required=True, validate=validate.Length(min=1, error=blank_error_massage))
    relation = fields.Nested(Relation, required=True)


class ArrivalDetails(BaseSchema):
    travel_date = fields.DateTime(format='%d/%m/%Y', required=True)
    travel_origin_country = fields.Nested(Country, required=True)
    flight_number = CustomString(validate=validate.Length(min=1, error=blank_error_massage))
    travel_companion_count = fields.Int(required=True, validate=validate.Range(min=0))
    has_arrived_healthy = fields.Boolean(required=True)
    transits = fields.List(fields.Nested(Transits))

    @validates_schema
    def validate_field(self, data, **kwargs):
        if data['travel_date'] > datetime.today():
            raise ValidationError("date must not be future")


class AbroadAffairs(BaseSchema):
    been_abroad = fields.Boolean(required=True)
    been_abroad_recently = fields.Boolean()
    covid_19_exposure = fields.Nested(Covid19Exposure)
    symptoms = fields.Nested(SymptomsInAbroadAffairs)
    arrival_details = fields.Nested(ArrivalDetails)


class ForeignTravels(BaseSchema):
    country = fields.Nested(Country, required=True)
    date = fields.DateTime(format='%d/%m/%Y', required=True)
    length_of_visit = fields.Int(required=True, validate=validate.Range(min=0))
    health_deterioration = fields.Boolean(required=True)

    @validates_schema
    def validate_field(self, data, **kwargs):
        if data['date'] > datetime.today():
            raise ValidationError("date must not be future")


class LocalTravels(BaseSchema):
    address_line = CustomString(required=True,validate=validate.Length(min=1, error=blank_error_massage))
    date = fields.DateTime(format='%d/%m/%Y', required=True)
    close_encounter_count = fields.Int(validate=validate.Range(min=0))

    @validates_schema
    def validate_field(self, data, **kwargs):
        if data['date'] > datetime.today():
            raise ValidationError("date must not be future")


class SymptomsForList(BaseSchema):
    code = CustomString(validate=validate.OneOf(choices=symptoms_dict.keys(),
                                                labels=symptoms_dict.values()), required=True)
    description = CustomString()


class Symptoms(BaseSchema):
    is_present = fields.Boolean(required=True)
    symptoms = fields.List(fields.Nested(SymptomsForList))
    date = fields.DateTime(format='%d/%m/%Y')
    is_under_treatment = fields.Boolean()

    @validates_schema
    def validate_field(self,data,**kwargs):
        if data['is_present'] is True:
            if 'symptoms' not in data:
                raise ValidationError("symptoms field is required")

            if 'date' not in data:
                raise ValidationError("date field is required")
            elif data['date'] > datetime.today():
                    raise ValidationError("date must not be future")

            if 'is_under_treatment' not in data:
                raise ValidationError("is_under_treatment field is required")


class Condition(BaseSchema):
    code = CustomString(validate=validate.OneOf(diseases_dict.keys(), labels=diseases_dict.values()), required=True)
    description = CustomString()


class PreExistingConditions(BaseSchema):
    is_present = fields.Boolean()
    conditions = fields.List(fields.Nested(Condition))


class PersonSchema(BaseSchema):
    introducer_details = fields.Nested(IntroducerDetails)
    personal_details = fields.Nested(PersonalDetails, required=True)
    emergency_contact = fields.Nested(EmergencyContact, required=True)
    covid_19_exposure = fields.Nested(Covid19Exposure, required=True)
    incomer_exposure = fields.Nested(IncomerExposure, required=True)
    abroad_affairs = fields.Nested(AbroadAffairs, required=True)
    foreign_travels = fields.List(fields.Nested(ForeignTravels))
    local_travels = fields.List(fields.Nested(LocalTravels))
    symptoms = fields.Nested(Symptoms, required=True)
    pre_existing_conditions = fields.Nested(PreExistingConditions)
    know_people_with_covid_19_symptoms = fields.Boolean(required=True)
    assistance_requested = CustomString(validate=validate.OneOf(choices=assistance_requested_list))



if __name__ == '__main__':

    # file_path = "E:\\covid api testing\\good\\3.json"
    file_path = "E:\\marshmallow_validation\\base\\sample_json.json"

    with open(file_path, "r") as file:
        data = json.load(file)
        # pprint(data)
        data = data['person']
        # pprint(data)
        print()

        try:
            result = PersonSchema().load(data)
            pprint(dict(result))
            print("ok")
        except ValidationError as ex:
            print("error")
            # pprint(ex.valid_data)
            pprint(ex.messages)

