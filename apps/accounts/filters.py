import django_filters.rest_framework as filters
from django.db.models import Q

from apps.accounts.models import User


class UserFilter(filters.FilterSet):
    search = filters.CharFilter(method='filter_search')

    class Meta:
        model = User
        fields = ['search']

    def filter_search(self, queryset, _, value):
        return queryset.filter(
            Q(username__icontains=value) | Q(first_name__icontains=value)
        )
