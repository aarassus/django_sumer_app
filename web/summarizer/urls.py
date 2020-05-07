from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path('accueil', views.accueil),
    path('resumeur', views.resumeur, name='resumeur')
]