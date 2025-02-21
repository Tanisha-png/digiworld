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
from main_app.models import Digimon, Toy, UserDigifarm, DigimonToy
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
    paginator = Paginator(digimon_list, 24)  # Show 25 digimon per page
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
        userdigifarm = UserDigifarm.objects.create(user=user, digimon=digimon)
        return redirect('digimon-index')
    except ValidationError as e:
        # Handle the validation error
        return redirect('digimon-index')

@login_required
def remove_digimon(request, user_id, digimon_id):
    user = request.user
    digimon = Digimon.objects.get(id=digimon_id)
    Digimon.objects.get(id=digimon_id).user.remove(user)
    userdigifarm = UserDigifarm.objects.get(user=user, digimon=digimon)
    userdigifarm.delete()
    return redirect('digifarm', user_id=user_id)

@login_required
def digifarm(request, user_id ):
    user = User.objects.get(id=user_id)
    digifarm = user.digimon.all()
    toys = Toy.objects.all()
    for digimon in digifarm:
        user_digifarm = UserDigifarm.objects.filter(user=user, digimon=digimon).first()
        if user_digifarm:
            digimon_toys = DigimonToy.objects.filter(user_digifarm=user_digifarm)
            digimon.given_toys = [dt.toy for dt in digimon_toys]
        else:
            digimon.given_toys = []
    return render(request, 'digimon/digifarm.html', {
        'digifarm': digifarm,
        'user': user,
        'toys': toys
    })



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
    success_url = '/powerups/'

@login_required
def associate_toy(request, digimon_id, toy_id):
    if request.method == 'POST':
        digimon = Digimon.objects.get(id=digimon_id)
        toy = Toy.objects.get(id=toy_id)
        digifarm = UserDigifarm.objects.get(user=request.user, digimon=digimon)
        DigimonToy.objects.create(user_digifarm_id=digifarm.id, toy=toy)
        return redirect('digifarm', user_id=request.user.id)

@login_required
def remove_toy(request, digimon_id, toy_id):
    if request.method == 'POST':
        digimon = Digimon.objects.get(id=digimon_id)
        toy = Toy.objects.get(id=toy_id)
        digifarm = UserDigifarm.objects.get(user=request.user, digimon=digimon)
        digimontoy = DigimonToy.objects.get(user_digifarm_id=digifarm.id, toy=toy)
        digimontoy.delete()
        return redirect('digifarm', user_id=request.user.id)

def show_all_users(request):
    users = User.objects.all()
    return render(request, 'community.html', {'users': users})
    # return render(request, 'digimon/index.html', {'digimon': digimon})
