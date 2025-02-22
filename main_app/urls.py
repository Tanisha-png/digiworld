from django.urls import path
from . import views

urlpatterns = [
  path('', views.Home.as_view(), name='home'),
  path('about/', views.about, name='about'),
  path('digimon/', views.digimon_index, name='digimon-index'),
  # Digifarm
  path('digimon/create/', views.DigimonCreate.as_view(), name='digimon-create'),
  path('user/<int:user_id>/digifarm/', views.digifarm, name='digifarm'),  
  path('user/<int:user_id>/digifarm/<int:digimon_id>/associate-digimon/', views.associate_digimon, name='associate-digimon'),
  path('user/<int:user_id>/digifarm/<int:digimon_id>/remove-digimon/', views.remove_digimon, name='remove-digimon'),
  path('users/', views.show_all_users, name='show-all-users'),
  # Toys
  path('powerups/', views.ToyList.as_view(), name='toy-index'),
  path('powerups/create/', views.ToyCreate.as_view(), name='toy-create'),
  path('powerups/<int:pk>/', views.ToyDetail.as_view(), name='toy-detail'),
  path('powerups/<int:pk>/update/', views.ToyUpdate.as_view(), name = 'toy-update'),
  path('powerups/<int:pk>/delete/', views.ToyDelete.as_view(), name = 'toy-delete'),
  path('digimon/<int:digimon_id>/powerups/<int:toy_id>/associate-toy/', views.associate_toy, name='associate-toy'),
  path('digimon/<int:digimon_id>/remove-toy/<int:toy_id>/', views.remove_toy, name='remove-toy'),
  # Sign up
  path('accounts/signup/', views.signup, name='signup'),
]
