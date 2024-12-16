from django_filters import FilterSet, ModelChoiceFilter
from .models import Response


class ResponseFilter(FilterSet):
    class Meta:
        model = Response
        fields = {
            'ads': ['exact'],
        }
