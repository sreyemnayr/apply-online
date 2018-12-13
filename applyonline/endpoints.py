from drf_auto_endpoint.router import register, router
from drf_auto_endpoint.endpoints import Endpoint

from rest_framework import viewsets, serializers

import rest_framework_filters as filters

from drf_writable_nested import WritableNestedModelSerializer

import applyonline.models as models
from address.models import Address


class FamilyFilter(filters.FilterSet):
    class Meta:
        model = models.Family
        fields = {'id': ['exact'],
                  'students': ['in']
                  }


class StudentFilter(filters.FilterSet):
    # families = filters.RelatedFilter(FamilyFilter, name="families")

    class Meta:
        model = models.Student
        fields = {'id': ['exact', 'in', 'startswith']}

class FamilySerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    name = serializers.CharField()

    class Meta:
        model = models.Family
        fields = ('id', 'name')


class StudentNestedSerializer(WritableNestedModelSerializer):
    families = FamilySerializer(many=True)

    class Meta:
        model = models.Student
        fields = ('first_name', 'last_name', 'preferred_name', 'middle_name', 'dob', 'gender', 'families')



class StudentViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        user = self.request.user
        parent = user.profile
        families = parent.family_set.all()
        students = models.Student.objects.filter(families__in=families)
        return students


class FamilyViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        user=self.request.user
        parent = user.profile
        families = parent.family_set.all()
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


router.register(models.Student, url='students')
router.register(models.Application, url='applications')
router.register(models.Family, url='families')
router.register(models.Evaluation)
router.register(models.OtherSchool)
router.register(models.Parent)
router.register(models.SchoolYear)
router.register(models.Sibling)
router.register(Address)



