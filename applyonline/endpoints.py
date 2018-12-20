from drf_auto_endpoint.router import register, router
from drf_auto_endpoint.endpoints import Endpoint

from rest_framework import viewsets, serializers

import rest_framework_filters as filters

from drf_writable_nested import WritableNestedModelSerializer, UniqueFieldsMixin

import applyonline.models as models


class FamilyFilter(filters.FilterSet):
    class Meta:
        model = models.Family
        fields = {"id": ["exact"], "students": ["in"]}


class FamilySerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    name = serializers.CharField()

    class Meta:
        model = models.Family
        fields = ("id", "name")


class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Parent
        fields = "__all__"


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Address
        fields = "__all__"


class SchoolYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SchoolYear
        fields = ("pk", "label")


class FamilyNestedSerializer(WritableNestedModelSerializer):
    parents = ParentSerializer(many=True)
    address = AddressSerializer(allow_null=True)

    class Meta:
        model = models.Family
        fields = "__all__"
        extra_fields = ["parents"]

    def get_field_names(self, declared_fields, info):
        expanded_fields = super().get_field_names(declared_fields, info)

        if getattr(self.Meta, "extra_fields", None):
            if type(expanded_fields) is tuple:
                return expanded_fields + tuple(self.Meta.extra_fields)
            else:
                return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields


class StudentNestedSerializer(WritableNestedModelSerializer):
    families = FamilySerializer(many=True)

    class Meta:
        model = models.Student
        fields = (
            "first_name",
            "last_name",
            "preferred_name",
            "middle_name",
            "dob",
            "gender",
            "families",
        )


class StudentNestedSerializerFullFamilies(StudentNestedSerializer):
    families = FamilyNestedSerializer(many=True)


class ApplicationSerializer(WritableNestedModelSerializer):
    student = StudentNestedSerializerFullFamilies()
    school_year = SchoolYearSerializer()

    class Meta:
        model = models.Application
        fields = "__all__"


class StudentViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        user = self.request.user
        parent = user.profile
        families = parent.families.all()
        students = models.Student.objects.filter(families__in=families)
        return students


class FamilyViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        user = self.request.user
        parent = user.profile
        families = parent.families.all()
        return families


@register
class StudentFilterEndpoint(Endpoint):
    model = models.Student
    base_viewset = StudentViewSet
    base_serializer = StudentNestedSerializer


@register
class FamilyFilterEndpoint(Endpoint):
    model = models.Family
    base_viewset = FamilyViewSet
    base_serializer = FamilyNestedSerializer


@register
class ParentFilterEndpoint(Endpoint):
    model = models.Parent
    filter_fields = ("families",)


@register(url="appflow")
class ApplicationFlowEndpoint(Endpoint):
    model = models.Application
    base_serializer = ApplicationSerializer


router.register(models.Student, url="students")
router.register(models.Application, url="applications")
router.register(models.Family, url="families")
router.register(models.Evaluation)
router.register(models.OtherSchool)
router.register(models.Parent, url="parents")
router.register(models.SchoolYear)
router.register(models.Sibling)
router.register(models.Address)
