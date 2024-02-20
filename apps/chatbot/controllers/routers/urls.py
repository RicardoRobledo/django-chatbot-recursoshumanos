from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from ...views import openai_views


urlpatterns = [
    path('', openai_views.post_message, name='post_message'),
    path('cleaner_manager/', openai_views.post_clean, name='post_clean'),
    path('thread/', openai_views.post_create_thread, name='post_create_thread'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
