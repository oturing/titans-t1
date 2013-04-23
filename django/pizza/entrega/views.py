# coding: utf-8

from django.shortcuts import render_to_response

from .models import Pizza

def listagem_pizzas(request):
    pizzas = Pizza.objects.all()
    qt_pizzas = len(pizzas)
    contexto = {'pizzas':pizzas, 'qt_pizzas':qt_pizzas}
    return render_to_response('entrega/listagem_pizzas.html', contexto)

