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
  # path('digimon/<int:pk>/update/', views.DigimonUpdate.as_view(), name='digimon-update'),
  # path('digimon/<int:pk>/delete/', views.DigimonDelete.as_view(), name='digimon-delete'),
  path('accounts/signup/', views.signup, name='signup'),
]
