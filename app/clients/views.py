from django.db.models import Q
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .models import Client, Department


class ClientListView(ListView):
    model = Client
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["client_count"] = Client.objects.all().count()
        return context

    def get_queryset(self):
        query = self.request.GET.get("q", "")
        queryset = Client.objects.all()

        if query:
            return Client.objects.filter(
                Q(name__icontains=query)
                | Q(department__name__icontains=query.replace("-", ""))
                | Q(job_title__icontains=query)
                | Q(email__icontains=query)
                | Q(ext__icontains=query)
            ).distinct()
        return queryset


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
