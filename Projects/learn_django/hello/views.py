from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import UserEntryForm
from .models import UserEntry

def user_form(request):
    if request.method == "POST":
        form = UserEntryForm(request.POST)