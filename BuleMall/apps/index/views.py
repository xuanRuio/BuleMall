from django.shortcuts import render

# Create your views here.
from django.views import View
from django import http

class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')
