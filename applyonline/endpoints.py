from drf_auto_endpoint.router import register, router
from drf_auto_endpoint.endpoints import Endpoint

from rest_framework import viewsets, serializers

import rest_framework_filters as filters

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


class StudentViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        user = self.request.user
        parent = user.profile
        families = parent.family_set.all()
        students = models.Student.objects.filter(family__in=families)
        return students


@register
class StudentFilterEndpoint(Endpoint):
    model = models.Student
    # filter_fields = ('families', )
    base_viewset = StudentViewSet

router.register(models.Student, url='students')
router.register(models.Application, url='applications')
router.register(models.Family)
router.register(models.Evaluation)
router.register(models.OtherSchool)
router.register(models.Parent)
router.register(models.SchoolYear)
router.register(models.Sibling)
router.register(Address)



