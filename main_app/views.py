import requests
from django.contrib.auth.views import LoginView
from django.core.cache import cache 
import json
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

def get_cached_digimon(url, cache_key):
    cached_data = cache.get(cache_key)
    if cached_data:
        return json.loads(cached_data)
    
    try:
        response = requests.get(url)
        digimon_data = response.json()
        cache.set(cache_key, json.dumps(digimon_data), 86400)
        return digimon_data
    except:
        return None

def about(request):
    response = requests.get('https://digimon-api.vercel.app/api/digimon')
    digimon_list = response.json()
    return render(request, 'about.html', {'digimon_list': digimon_list})

def digimon_index(request):
    digimon = Digimon.objects.all()
    return render(request, 'digimon/index.html', {'digimon': digimon})

class DigimonCreate(CreateView):
    model = Digimon
    fields = ['name', 'img', 'level', 'happiness']
    success_url = '/digimon/'
