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
    
def associate_digimon(request, user_id, digimon_id):
  # Note that you can pass a toy's id instead of the whole object
  Digimon.objects.get(id=digimon_id).user.add(user_id)
  return redirect('digifarm', digimon_id=digimon_id)

def digifarm(request, user_id, digimon_id):
    digimon = Digimon.objects.get(id=digimon_id)
    return render(request, 'digimon/digifarm.html', {
        'digimon': digimon,
        # 'user_id': user_id
    })

# def remove_toy(request, cat_id, toy_id):
#   Cat.objects.get(id=cat_id).toys.remove(toy_id)
#   return redirect('cat-detail', cat_id=cat_id)
  
def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('digimon-index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)
