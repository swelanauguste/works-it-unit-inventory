from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .models import Client, Department


class ClientListView(ListView):
    model = Client


class ClientCreateView(CreateView):
    model = Client
    fields = "__all__"


class ClientUpdateView(UpdateView):
    model = Client
    fields = "__all__"


class ClientDetailView(DetailView):
    model = Client


class DepartmentListView(ListView):
    model = Department