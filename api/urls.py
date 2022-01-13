from django.urls import path

from . import views

urlpatterns = [
    path('', views.PokeTrainersApi.as_view(), name = 'poketrainersapi'),

]
