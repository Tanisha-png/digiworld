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
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect


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
    try:
        digimon = Digimon.objects.get(id=digimon_id)
        user = request.user
        if user.digimon.count() >= 6:
            # You could add a message here using Django's messages framework
            return redirect('digifarm', user_id=user_id)
        digimon.user.add(user)
        return redirect('digifarm', user_id=user_id)
    except ValidationError as e:
        # Handle the validation error
        return redirect('digifarm', user_id=user_id)

def digifarm(request, user_id ):
    user = request.user
    digifarm = user.digimon.all()
    return render(request, 'digimon/digifarm.html', {
        'digifarm': digifarm,
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
