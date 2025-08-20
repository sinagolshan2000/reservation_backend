from django_filters import FilterSet, CharFilter

from reservation.models import BusinessOwner


class BusinessOwnerFilter(FilterSet):

    class Meta:
        model = BusinessOwner
        fields = ['city', 'job']
