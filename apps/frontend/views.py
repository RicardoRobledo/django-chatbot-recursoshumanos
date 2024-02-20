from django.views import View
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.decorators.cache import never_cache


__author__ = 'Ricardo'
__version__ = '0.1'


@method_decorator(login_required(login_url='/'), name='dispatch')
@method_decorator(never_cache, name='dispatch')
class IndexView(View):

    def get(self, request, *args, **kwargs):
        """
        This method return our chatbot view
        """

        response = render(request, 'frontend/index.html')
        
        return response
