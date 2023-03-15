from django.shortcuts import render
from djoser.views import TokenCreateView

# Create your views here.

class CustomTokenCreateView(TokenCreateView):
    authentication_classes = []