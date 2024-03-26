from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.db.models import Q

from .filter import CardFilter
from .forms import CardForm
from .models import Card


def card_filter_view(request):
    f = CardFilter(request.GET, queryset=Card.objects.all())
    return render(request, "card/card_filter.html", {"filter": f})


class CardListView(LoginRequiredMixin, ListView):
    model = Card

    def get_queryset(self):
        queryset = Card.objects.all()
        query = self.request.GET.get("cards")

        if query:
            return Card.objects.filter(
                Q(name__icontains=query)
                | Q(licence__name__icontains=query.replace("-", ""))
                | Q(licence_no__icontains=query)
                | Q(category__name__icontains=query)
            ).distinct()
        return queryset


class CardDetailView(LoginRequiredMixin, DetailView):
    model = Card


class CardCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Card
    form_class = CardForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class CardUpdateView(LoginRequiredMixin, UpdateView):
    model = Card
    form_class = CardForm

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)
