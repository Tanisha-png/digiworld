from django.urls import path
from . import views

# as_view() is only used for Class-based Views, it converts it to a
#   function as you can't provide a class

urlpatterns = [
  path('', views.Home.as_view(), name='home'),
  path('about/', views.about, name='about'),
  path('digimon/', views.digimon_index, name='digimon-index'),
  path('user/<int:user_id>/digifarm/', views.digifarm, name='digifarm'),  
  path('user/<int:user_id>/digifarm/<int:digimon_id>/associate-digimon/', views.associate_digimon, name='associate-digimon'),
  path('digimon/create/', views.DigimonCreate.as_view(), name='digimon-create'),
  path('user/<int:user_id>/digifarm/<int:digimon_id>/remove-digimon/', views.remove_digimon, name='remove-digimon'),
  path('toys/create/', views.ToyCreate.as_view(), name='toy-create'),
  path('toys/', views.ToyList.as_view(), name='toy-index'),
  path('toys/<int:pk>/', views.ToyDetail.as_view(), name='toy-detail'),
  path('toys/<int:pk>/update/', views.ToyUpdate.as_view(), name = 'toy-update'),
  path('toys/<int:pk>/delete/', views.ToyDelete.as_view(), name = 'toy-delete'),
  path('digimon/<int:digimon_id>/associate_toy/<int:toy_id>/', views.associate_toy, name='associate_toy'),
  path('digimon/<int:digimon_id>/remove-toy/<int:toy_id>/', views.remove_toy, name='remove-toy'),
  path('accounts/signup/', views.signup, name='signup'),
]
