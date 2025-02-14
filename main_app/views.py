import requests
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from main_app.models import Digimon

# Create your views here.

class Home(LoginView):
  template_name = 'home.html'

def about(request):
    response = requests.get('https://digimon-api.vercel.app/api/digimon')
    digimon_list = response.json()
    return render(request, 'about.html', {'digimon_list': digimon_list})
