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
from main_app.models import Digimon, Toy
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.models import User

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
    return render(request, 'about.html')

def digimon_index(request):
    digimon_list = Digimon.objects.all()
    paginator = Paginator(digimon_list, 25)  # Show 25 digimon per page
    page_number = request.GET.get('page')
    digimon = paginator.get_page(page_number)
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

def remove_digimon(request, user_id, digimon_id):
    user = request.user
    Digimon.objects.get(id=digimon_id).user.remove(user)
    return redirect('digifarm', user_id=user_id)

def digifarm(request, user_id ):
    user = User.objects.get(id=user_id)
    digifarm = user.digimon.all()
    return render(request, 'digimon/digifarm.html', {
        'digifarm': digifarm,
        'user': user
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

class ToyCreate(LoginRequiredMixin, CreateView):
    model = Toy
    fields = '__all__'

class ToyList(LoginRequiredMixin, ListView):
    model = Toy

class ToyDetail(LoginRequiredMixin, DetailView):
    model = Toy

class ToyUpdate(LoginRequiredMixin, UpdateView):
    model = Toy
    fields = ['name', 'color']

class ToyDelete(LoginRequiredMixin, DeleteView):
    model = Toy
    success_url = '/toys/'

def associate_toy(request,digimon_id, toy_id):
    Digimon.objects.get(id=digimon_id).toys.add(toy_id)
    return redirect('digifarm', digimon_id=digimon_id, toy_id=toy_id)

def remove_toy(request, digimon_id, toy_id):
    Digimon.objects.get(id=digimon_id).toys.remove(toy_id)
    return redirect('digifarm', digimon_id=digimon_id)
