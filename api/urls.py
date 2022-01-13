from django.urls import path

from . import views

urlpatterns = [
    path('trainers/', views.Trainers.as_view(), name = 'trainers'),
    path('teams/', views.Teams.as_view(), name = 'teams'),
    path('members/', views.TeamMembers.as_view(), name = 'members'),

]
