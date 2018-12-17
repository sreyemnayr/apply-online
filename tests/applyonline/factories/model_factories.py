import random

from factory.django import DjangoModelFactory
import factory

from django.utils import timezone

import applyonline.models


class ApplicationFactory(DjangoModelFactory):
    class Meta:
        model = applyonline.models.Application

    student = factory.SubFactory("tests.applyonline.factories.StudentFactory")
    school_year = factory.SubFactory("tests.applyonline.factories.SchoolYearFactory")


class StudentFactory(DjangoModelFactory):
    class Meta:
        model = applyonline.models.Student

    first_name = factory.Faker("first_name")
    middle_name = factory.Faker("first_name")
    preferred_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    dob = factory.Faker("date_this_decade")

    class Params:
        male = factory.Trait(
            first_name=factory.Faker("first_name_male"),
            middle_name=factory.Faker("first_name_male"),
            preferred_name=factory.Faker("first_name_male"),
            gender="M",
        )
        female = factory.Trait(
            first_name=factory.Faker("first_name_female"),
            middle_name=factory.Faker("first_name_female"),
            preferred_name=factory.Faker("first_name_female"),
            gender="F",
        )


class FamilyFactory(DjangoModelFactory):
    class Meta:
        model = applyonline.models.Family

    name = factory.Faker("last_name")


class ParentFactory(DjangoModelFactory):
    class Meta:
        model = applyonline.models.Parent

    first_name = factory.Faker("first_name")
    preferred_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    dob = factory.Faker("past_date")


class SchoolYearFactory(DjangoModelFactory):
    class Meta:
        model = applyonline.models.SchoolYear

    label = "2019-2020"
    start = factory.Faker("date_this_decade")
    end = factory.Faker("future_date")
    open = True


class EvaluationFactory(DjangoModelFactory):
    class Meta:
        model = applyonline.models.Evaluation


class SiblingFactory(DjangoModelFactory):
    class Meta:
        model = applyonline.models.Sibling


class OtherSchoolFactory(DjangoModelFactory):
    class Meta:
        model = applyonline.models.OtherSchool
