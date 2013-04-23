from django.conf.urls import patterns, include, url
from django.views.generic import ListView, DetailView

from .models import Cliente
from .views import listagem_pizzas

urlpatterns = patterns('',
    url(r'clientes', ListView.as_view(model=Cliente), name='home'),
    url(r'cliente/(?P<pk>\d+)', DetailView.as_view(model=Cliente), name='cliente'),
    url(r'pizzas', listagem_pizzas, name='listagem_pizzas'),
)
