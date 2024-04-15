from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .models import KnowledgeBase, KnowledgeBaseCategory, KnowledgeBaseComment


class KnowledgeBaseListView(ListView):
    model = KnowledgeBase

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["knowledgebase_count"] = KnowledgeBase.objects.all().count()
        return context

    def get_queryset(self):
        query = self.request.GET.get("knowledgebase")

        if query:
            return KnowledgeBase.objects.filter(
                Q(name__icontains=query)
                | Q(description__icontains=query)
                | Q(category__name__icontains=query)
            ).distinct()
        return KnowledgeBase.objects.all()


class KnowledgeBaseDetailView(DetailView):
    model = KnowledgeBase


class KnowledgeBaseCreateView(CreateView):
    model = KnowledgeBase
    fields = "__all__"


class KnowledgeBaseUpdateView(UpdateView):
    model = KnowledgeBase
    fields = "__all__"


class KnowledgeBaseCommentCreateView(CreateView):
    model = KnowledgeBaseComment
    fields = ["comments"]

    def form_valid(self, form):
        form.instance.knowledgebase_id = self.kwargs["pk"]
        return super().form_valid(form)
