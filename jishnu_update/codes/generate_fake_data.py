from faker import Faker
# from faker.generator import random

from time import sleep
import json
from pprint import pprint
from base.data_dictionaries import country_dict, district_dict, symptoms_dict, realtion_dict, gender_dict, diseases_dict, assistance_requested_list, introducer_type_list, district_wise_sub_district
from validator import PersonSchema
import random
faker = Faker()

sub_district_list = dict()
for district in district_wise_sub_district:

    sub_district_list[district] = []
    for sub_district in district_wise_sub_district[district]:
        sub_district_list[district].append(sub_district['name'])


class Relation:

    def __init__(self):
        self.code = faker.word(ext_word_list=realtion_dict.keys())
        self.description = faker.sentence()


class Address:
    def __init__(self):
        self.address_line = faker.sentence()
        self.town = faker.word()
        self.police_station = faker.word()
        self.district = faker.word(ext_word_list=district_dict.keys())
        self.sub_district = faker.word(ext_word_list=sub_district_list[self.district])


class IntroducerDetails:

    def __init__(self):
        self.name = faker.name()
        self.contact_number = faker.phone_number()
        self.introducer_type = faker.word(ext_word_list=introducer_type_list)

        if self.introducer_type in ['Hospital/Clinic', 'Govt. Agency/Local Govt', 'NGO']:
            self.name_of_organization = faker.word()


class Country:

    def __init__(self):
        self.code = faker.word(ext_word_list=country_dict.keys())
        self.description = faker.sentence()


class PersonalDetails:

    def __init__(self):
        self.name = faker.name()
        self.passport_number = faker.sentence()
        self.nid_number = faker.sentence()
        self.gender = faker.word(ext_word_list=gender_dict.keys())
        self.age = random.randrange(1,200)

        self.father_name = faker.word()
        self.contact_number = faker.phone_number()
        self.email = faker.email()
        self.address = Address()
        self.facbook_profile_url = faker.sentence()
        self.foreign_mobile_no = faker.sentence()
        self.country_of_origin = Country()
        self.country_of_residence = Country()


class EmergencyContact:

    def __init__(self):
        self.name = faker.name()
        self.relation = Relation()
        self.contact_number = faker.phone_number()
        self.email = faker.email()


class Covid19Exposure:
    def __init__(self):
        self.been_exposed = random.randint(0, 1)
        if self.been_exposed:
            self.date = faker.date_between(start_date='-100d', end_date='today')



class IncomerExposure:

    def __init__(self):
        self.been_exposed = random.randint(0, 1)
        if self.been_exposed:
            self.date = faker.date_between(start_date='-100d', end_date='today')
            self.country = Country()

#
class SymptomsInAbroadAffairs:


    def __init__(self):
        self.pre_arrival_symptom_presence = random.randint(0, 1)
        if self.pre_arrival_symptom_presence:
            self.pre_arrival_symptom_date = faker.date_between(start_date='-100d', end_date='today')
        self.been_treated = random.randint(0, 1)
        if self.been_treated:
            self.treatment_date = faker.date_between(start_date='-100d', end_date='today')
        self.post_arrival_symptom_presence = random.randint(0, 1)
        if self.post_arrival_symptom_presence:
            self.post_arrival_symptom_date = faker.date_between(start_date='-100d', end_date='today')


class Transits:
    def __init__(self):
        self.country = Country()
        self.period_in_hours = random.randrange(24)


class ArrivalDetails:

    def __init__(self):
        self.travel_date = faker.date_between(start_date='-100d', end_date='today')
        self.travel_origin_country = Country()
        self.flight_number = faker.word()
        self.travel_companion_count = random.randrange(500)
        self.has_arrived_healthy = random.randint(0, 1)
        self.transits = []
        for i in range(random.randrange(0, 3)):
            self.transits.append(Transits())


class AbroadAffairs:

    def __init__(self):
        self.been_abroad = random.randint(0, 1)
        if self.been_abroad:
            self.been_abroad_recently = random.randint(0, 1)
            self.covid_19_exposure = Covid19Exposure()
            self.symptoms = SymptomsInAbroadAffairs()
            self.arrival_details = ArrivalDetails()


class ForeignTravels:

    def __init__(self):
        self.country = Country()
        self.date = faker.date_between(start_date='-100d', end_date='today')
        self.length_of_visit = random.randrange(300)
        self.health_deterioration = random.randint(0, 1)


class LocalTravels:

    def __init__(self):
        self.address_line = faker.sentence()
        self.date =faker.date_between(start_date='-100d', end_date='today')
        self.close_encounter_count = random.randrange(100)


class SymptomsForList:

    def __init__(self):
        self.code = faker.word(ext_word_list=symptoms_dict.keys())
        self.description = faker.sentence()


class Symptoms:

    def __init__(self):
        self.is_present = random.randint(0, 1)
        if self.is_present:
            self.symptoms = []
            self.date = faker.date_between(start_date='-100d', end_date='today')
            self.is_under_treatment = random.randint(0, 1)
            for i in range(random.randrange(1, 4)):
                self.symptoms.append(SymptomsForList())


class Condition:

    def __init__(self):
        self.code = faker.word(ext_word_list=diseases_dict.keys())
        self.description = faker.sentence()


class PreExistingConditions:

    def __init__(self):
        self.is_present = random.randint(0, 1)
        if self.is_present:
            self.conditions = []
            for i in range(random.randrange(1, 4)):
                self.conditions.append(Condition())


class Person:

    def __init__(self):
        self.introducer_details = IntroducerDetails()
        self.personal_details = PersonalDetails()
        self.emergency_contact = EmergencyContact()
        self.covid_19_exposure = Covid19Exposure()
        self.incomer_exposure = IncomerExposure()
        self.abroad_affairs = AbroadAffairs()
        self.foreign_travels = []
        self.local_travels = []
        self.symptoms = Symptoms()
        self.pre_existing_conditions = PreExistingConditions()
        self.know_people_with_covid_19_symptoms = random.randint(0, 1)
        if random.randint(0, 1):
            self.assistance_requested = faker.word(ext_word_list=assistance_requested_list)

        for i in range(random.randrange(0, 5)):
            self.foreign_travels.append(ForeignTravels())

        for i in range(random.randrange(0, 5)):
            self.local_travels.append(LocalTravels())



for i in range(300):
    with open("sample data\\sampale_data"+str(i)+".json", "w") as file:
        person = Person()

        p = PersonSchema().dump(person)
        p["version"] = "1.0"
        data = dict()

        data['person'] = p
        data["version"] = "1.0"
        json.dump(data, file, sort_keys=True, indent=4, separators=(',', ': '))




#
#
#
# print("introducer details:")
# print("\t", 'name: ', person.introducer_details.name)
# print("\t", 'contact_number: ', person.introducer_details.contact_number)
# print("\t", 'email: ', person.introducer_details.email)
# print("\t", 'nid_number :', person.introducer_details.nid_number)
# print("\t", "address:")
# print("\t\t", 'address_line: ',person.introducer_details.address.address_line)
# print("\t\t", 'town: ',person.introducer_details.address.town)
# print("\t\t", 'police_station: ',person.introducer_details.address.police_station)
# print("\t\t", 'sub_district: ',person.introducer_details.address.sub_district)
# print("\t\t", 'district: ',person.introducer_details.address.district)
# print("\t","relation:")
# print("\t\t", 'code: ',person.introducer_details.relation.code)
# print("\t\t", 'description: ',person.introducer_details.relation.description)
#
# print("personal details: ")
# print("\t", 'name: ', person.personal_details.name)
# print("\t", 'contact_number: ', person.personal_details.contact_number)
# print("\t", 'email: ', person.personal_details.email)
# print("\t", 'nid_number :', person.personal_details.nid_number)
# print("\t", 'gender :', person.personal_details.gender)
# print("\t", 'age :', person.personal_details.age)
# print("\t", 'father_name :', person.personal_details.father_name)
# print("\t", "address:")
# print("\t\t", 'address_line: ',person.personal_details.address.address_line)
# print("\t\t", 'town: ',person.personal_details.address.town)
# print("\t\t", 'police_station: ',person.personal_details.address.police_station)
# print("\t\t", 'sub_district: ',person.personal_details.address.sub_district)
# print("\t\t", 'district: ',person.personal_details.address.district)
# print("\t", 'facbook_profile_url :', person.personal_details.facbook_profile_url)
# print("\t", 'foreign_mobile_no :', person.personal_details.foreign_mobile_no)
# print("\tcountry_of_origin:")
# print("\t\t", 'code: ',person.personal_details.country_of_origin.code)
# print("\t\t", 'description: ',person.personal_details.country_of_origin.description)
# print("\tcountry_of_residence:")
# print("\t\t", 'code: ',person.personal_details.country_of_residence.code)
# print("\t\t", 'description: ',person.personal_details.country_of_residence.description)
# print("emergency contact:")
# print("\t","name: ", person.emergency_contact.name)
# print("\t","relation:")
# print("\t\t", 'code: ',person.emergency_contact.relation.code)
# print("\t\t", 'description: ',person.emergency_contact.relation.description)
# print("\t","contact_number: ", person.emergency_contact.contact_number)
# print("\t","email: ", person.emergency_contact.email)
# print('Covid19Exposure: ')
# print("\t",'been_exposed: ', person.covid_19_exposure.been_exposed)
# print("\t",'date: ', person.covid_19_exposure.date)
# print('IncomerExposure: ')
# print("\t", 'been_exposed: ', person.incomer_exposure.been_exposed)
# print("\t", 'date: ', person.incomer_exposure.date)
# print("\tcountry:")
# print("\t\t", 'code: ',person.incomer_exposure.country.code)
# print("\t\t", 'description: ',person.incomer_exposure.country.description)
# print("AbroadAffairs: ")
# print("\t","been_abroad: ", person.abroad_affairs.been_abroad)
# print("\t","been_abroad_recently: ", person.abroad_affairs.been_abroad_recently)
# print("\t","Covid19Exposure: ")
# print("\t\t",'been_exposed: ', person.abroad_affairs.covid_19_exposure.been_exposed)
# print("\t\t",'date: ', person.abroad_affairs.covid_19_exposure.date)
# print("\tSymptoms: ")
# print("\t\t",'pre_arrival_symptom_presence: ', person.abroad_affairs.symptoms.pre_arrival_symptom_presence)
# print("\t\t",'pre_arrival_symptom_date: ', person.abroad_affairs.symptoms.pre_arrival_symptom_date)
# print("\t\t",'been_treated: ', person.abroad_affairs.symptoms.been_treated)
# print("\t\t",'treatment_date: ', person.abroad_affairs.symptoms.treatment_date)
# print("\t\t",'post_arrival_symptom_presence: ', person.abroad_affairs.symptoms.post_arrival_symptom_presence)
# print("\t\t",'post_arrival_symptom_date: ', person.abroad_affairs.symptoms.post_arrival_symptom_date)
# print("\tarrival_details: ")
# print("\t\t","travel_date: ", person.abroad_affairs.arrival_details.travel_date)
# print("\t\ttravel_origin_country:")
# print("\t\t\t", 'code: ',person.abroad_affairs.arrival_details.travel_origin_country.code)
# print("\t\t\t", 'description: ',person.abroad_affairs.arrival_details.travel_origin_country.description)
# print("\t\t","flight_number: ", person.abroad_affairs.arrival_details.flight_number)
# print("\t\t","travel_companion_count: ", person.abroad_affairs.arrival_details.travel_companion_count)
# print("\t\t","has_arrived_healthy: ", person.abroad_affairs.arrival_details.has_arrived_healthy)
# print("\t\t","transits: ")
# for i in range(len(person.abroad_affairs.arrival_details.transits)):
#     print("\t\t\tcountry:")
#     print("\t\t\t\t", 'code: ', person.abroad_affairs.arrival_details.transits[i].country.code)
#     print("\t\t\t\t", 'description: ', person.abroad_affairs.arrival_details.transits[i].country.description)
#     print("\t\t\t\t","period_in_hours: ",person.abroad_affairs.arrival_details.transits[i].period_in_hours)
#
# if len(person.foreign_travels):
#     print("ForeignTravels: ")
# for i in range(len(person.foreign_travels)):
#
#     print("\tcountry")
#     print("\t\t", 'code: ',person.foreign_travels[i].country.code)
#     print("\t\t", 'description: ',person.foreign_travels[i].country.description)
#     print("\t","date: ", person.foreign_travels[i].date)
#     print("\t","length_of_visit: ", person.foreign_travels[i].length_of_visit)
#     print("\t","health_deterioration: ", person.foreign_travels[i].health_deterioration)
#     print()
#
# if len(person.local_travels):
#     print("Local Travels: ")
# for i in range(len(person.local_travels)):
#     print("\t", "address_line: ", person.local_travels[i].address_line)
#     print("\t", "date: ", person.local_travels[i].date)
#     print("\t", "close_encounter_count: ", person.local_travels[i].close_encounter_count)
#     print()
#
# print("symptoms: ")
# print("\t","is_present: ", person.symptoms.is_present)
#
# if len(person.symptoms.symptoms):
#     print("\t", "symptoms: ")
# for i in range(len(person.symptoms.symptoms)):
#     print("\t\t","code : ", person.symptoms.symptoms[i].code)
#     print("\t\t","description : ", person.symptoms.symptoms[i].description)
#
#
# print("\t","date: ", person.symptoms.date)
# print("\t","is_under_treatment: ", person.symptoms.is_under_treatment)
#
# print("PreExistingConditions")
# print("\t","is_present: ", person.pre_existing_conditions.is_present)
#
# if len(person.pre_existing_conditions.conditions):
#     print("\t", "conditions: ")
# for i in range(len(person.pre_existing_conditions.conditions)):
#     print("\t\t","code : ", person.pre_existing_conditions.conditions[i].code)
#     print("\t\t","description : ",person.pre_existing_conditions.conditions[i].description)
#     print()
#
#
# print("assistant requested:")
# print("\t", person.assistance_requested)
#
#