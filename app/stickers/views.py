from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .filters import StickerFilter
from .forms import StickerForm
from .models import Sticker


def sticker_filter_view(request):
    f = StickerFilter(request.GET, queryset=Sticker.objects.all())
    return render(request, "assets/sticker_filter.html", {"filter": f})


class StickerClerkListView(ListView):
    model = Sticker

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["clerk_stickers"] = Sticker.objects.filter(
            created_by=self.request.user.profile
        )
        context["form"] = StickerForm()
        return context

    def get_queryset(self):
        query = self.request.GET.get("stickers")

        if query:
            return Sticker.objects.filter(
                Q(name__icontains=query)
                | Q(no_plate__icontains=query)
                | Q(sticker__icontains=query)
            ).distinct()
        return Sticker.objects.all()


class StickerDetailView(DetailView):
    model = Sticker


class StickerCreateView(CreateView):
    model = Sticker
    form_class = StickerForm
    success_url = reverse_lazy("sticker-clerk-list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user.profile
        form.instance.updated_by = self.request.user.profile
        return super().form_valid(form)


class StickerUpdateView(UpdateView):
    model = Sticker
    form_class = StickerForm

    def form_valid(self, form):
        form.instance.updated_by = self.request.user.profile
        return super().form_valid(form)
