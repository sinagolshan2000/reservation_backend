from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from .serializers import *


class ProvinceView(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer


class CityView(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = City.objects.all().order_by("name")
    serializer_class = CitySerializer


class JobView(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = Job.objects.all()
    serializer_class = JobSerializer


class JobCategoryView(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = JobCategory.objects.all()
    serializer_class = JobCategorySerializer
