from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from ...views import procedure_views 


urlpatterns = [
    path('', procedure_views.get_list_procedures, name='list_procedures'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
