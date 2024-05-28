from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from .filters import ComputerFilter, PrinterFilter
from .forms import ComputerForm  # GetComputerNameForm,
from .forms import (
    CommentCreateForm,
    ComputerModelForm,
    MicrosoftOfficeUpdateForm,
    MonitorForm,
    MonitorModelForm,
    PrinterForm,
    PrinterModelForm,
)
from .models import ComputerModel  # ComputerName,
from .models import (
    Computer,
    ComputerComment,
    ComputerType,
    Maker,
    MicrosoftOffice,
    Monitor,
    MonitorModel,
    Printer,
    PrinterModel,
    Status,
)

def computer_list_view(request):
    query = request.GET.get('q', '')
    
    if query:
        computer_filter = ComputerFilter(request.GET, queryset=Computer.objects.filter(
            Q(computer_name__icontains=query) |
            Q(serial_number__icontains=query) |
            Q(user__icontains=query) |
            Q(notes__icontains=query))
        )
    else:
        computer_filter = ComputerFilter(request.GET, queryset=Computer.objects.all())

        
    all_computers = Computer.objects.all().count()
    computer_count = computer_filter.qs.count()
    return render(
        request,
        "assets/computer/computer_filter_list.html",
        {"filter": computer_filter, "computer_count": computer_count, "all_computers": all_computers},
    )


# def computer_filter_view(request):
#     f = ComputerFilter(request.GET, queryset=Computer.objects.all())
#     return render(request, "assets/computer_filter.html", {"filter": f})


def printer_filter_view(request):
    f = PrinterFilter(request.GET, queryset=Printer.objects.all())
    return render(request, "assets/printer_filter.html", {"filter": f})


class MicrosoftOfficeListView(LoginRequiredMixin, ListView):
    model = MicrosoftOffice

    def get_queryset(self):
        queryset = MicrosoftOffice.objects.filter(is_installed=False, has_failed=False)
        query = self.request.GET.get("microsoft_office_search")

        if query:
            return MicrosoftOffice.objects.filter(
                Q(version__name__icontains=query)
                | Q(product_key__icontains=query.replace("-", ""))
                | Q(computer__computer_name__icontains=query)
                | Q(computer__serial_number__icontains=query)
            ).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["microsoft_office_count"] = MicrosoftOffice.objects.all().count()
        context["microsoft_office_installed_count"] = MicrosoftOffice.objects.filter(
            is_installed=True
        ).count()
        context["microsoft_office_installed"] = MicrosoftOffice.objects.filter(
            is_installed=True
        )
        context["microsoft_office_has_failed"] = MicrosoftOffice.objects.filter(
            has_failed=True
        )
        context["microsoft_office_update_form"] = MicrosoftOfficeUpdateForm()
        return context


class MicrosoftOfficeDetailView(LoginRequiredMixin, DetailView):
    model = MicrosoftOffice

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["microsoft_office_update_form"] = MicrosoftOfficeUpdateForm()
        return context


class MicrosoftOfficeUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = MicrosoftOffice
    form_class = MicrosoftOfficeUpdateForm
    success_message = "Assigned to  %(computer)s"

    def form_valid(self, form):
        if form.instance.has_failed:
            form.instance.is_installed = False
            form.instance.has_failed = True
        elif form.instance.date_installed and not form.instance.computer:
            form.add_error("computer", "Please select a computer for installation.")

        return super().form_valid(form)


class MicrosoftOfficeAssignView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = MicrosoftOffice
    form_class = MicrosoftOfficeUpdateForm
    success_message = "Assigned to  %(computer)s"

    def form_valid(self, form):
        if form.instance.has_failed:
            form.instance.is_installed = False
            form.instance.has_failed = True
            form.instance.updated_by = self.request.user
        elif form.instance.date_installed and not form.instance.computer:
            form.add_error("computer", "Please select a computer for installation.")
        else:
            form.instance.is_installed = True
            form.instance.updated_by = self.request.user

        return super().form_valid(form)


def add_computer_comment_view(request, pk):
    computer = get_object_or_404(Computer, pk=pk)

    if request.method == "POST":
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.computer = computer
            comment.save()
            return redirect("computer-detail", pk=pk)

    # If the form is not valid or the request method is not POST
    return render(
        request, "assets/computer_detail.html", {"ticket": ticket, "comment_form": form}
    )


class ComputerListView(ListView):
    model = Computer
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["computer_count"] = Computer.objects.all().count()
        return context

    def get_queryset(self):
        query = self.request.GET.get("computers")

        if query:
            return Computer.objects.filter(
                Q(serial_number__icontains=query)
                | Q(computer_name__icontains=query)
                | Q(os__name__icontains=query)
                | Q(model__name__icontains=query)
                | Q(model__computer_type__name__icontains=query)
                | Q(model__maker__name__icontains=query)
                | Q(model__processor__icontains=query)
                | Q(model__ram__icontains=query)
                | Q(model__hdd__icontains=query)
                | Q(user__icontains=query)
                | Q(status__name__icontains=query)
                | Q(warranty_info__icontains=query)
                | Q(location__name__icontains=query)
                | Q(department__name__icontains=query)
                | Q(project__name__icontains=query)
                | Q(notes__icontains=query)
            ).distinct()
        return Computer.objects.all()


class ComputerModelListView(ListView):
    model = ComputerModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["computer_model_count"] = ComputerModel.objects.all().count()
        return context

    def get_queryset(self):
        query = self.request.GET.get("computer-models")

        if query:
            return ComputerModel.objects.filter(
                Q(name__icontains=query)
                | Q(computer_type__name__icontains=query)
                | Q(maker__name__icontains=query)
                | Q(processor__icontains=query)
                | Q(ram__icontains=query)
                | Q(hdd__icontains=query)
            ).distinct()
        return ComputerModel.objects.all()


class PrinterListView(ListView):
    model = Printer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["printer_count"] = Printer.objects.all().count()
        return context

    def get_queryset(self):
        query = self.request.GET.get("printers")

        if query:
            return Printer.objects.filter(
                Q(serial_number__icontains=query)
                | Q(printer_name__icontains=query)
                | Q(model__name__icontains=query)
                | Q(model__maker__name__icontains=query)
                | Q(status__name__icontains=query)
                | Q(location__name__icontains=query)
                | Q(ip_addr__icontains=query)
                | Q(department__name__icontains=query)
            ).distinct()
        return Printer.objects.all()


class PrinterModelListView(ListView):
    model = PrinterModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["printer_model_count"] = PrinterModel.objects.all().count()
        return context

    def get_queryset(self):
        query = self.request.GET.get("printer-models")

        if query:
            return PrinterModel.objects.filter(
                Q(name__icontains=query) | Q(maker__name__icontains=query)
            ).distinct()
        return PrinterModel.objects.all()


# class ComputerCreateView(CreateView):
#     model = Computer
#     form_class = ComputerForm

#     def form_valid(self, form):
#         form.instance.created_by = self.request.user
#         form.instance.updated_by = self.request.user
#         return super().form_valid(form)


class ComputerCreateView(CreateView, SuccessMessageMixin):
    model = Computer
    form_class = ComputerForm
    success_message = "Computer was created successfully."
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['last_computer_name'] = Computer.get_last_computer_name(self)
        return context

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        if "save_and_add_another" in self.request.POST:
            return reverse_lazy("computer-create")
        return reverse_lazy("computer-list")


class ComputerDeleteView(DeleteView):
    model = Computer
    success_url = reverse_lazy("computer-list")


class ComputerUpdateView(UpdateView):
    model = Computer
    form_class = ComputerForm

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class ComputerModelCreateView(CreateView):
    model = ComputerModel
    form_class = ComputerModelForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class ComputerModelUpdateView(UpdateView):
    model = ComputerModel
    form_class = ComputerModelForm


class ComputerDetailView(DetailView):
    model = Computer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = CommentCreateForm()
        return context


class ComputerModelDetailView(DetailView):
    model = ComputerModel


class PrinterCreateView(CreateView):
    model = Printer
    form_class = PrinterForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class PrinterUpdateView(UpdateView):
    model = Printer
    form_class = PrinterForm

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class PrinterModelCreateView(CreateView):
    model = PrinterModel
    form_class = PrinterModelForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class PrinterModelUpdateView(UpdateView):
    model = PrinterModel
    form_class = PrinterModelForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class PrinterDetailView(DetailView):
    model = Printer


class PrinterModelDetailView(DetailView):
    model = PrinterModel


class MonitorListView(ListView):
    model = Monitor

    def get_queryset(self):
        query = self.request.GET.get("monitors")

        if query:
            return Monitor.objects.filter(
                Q(serial_number__icontains=query)
                | Q(model__name__icontains=query)
                | Q(model__maker__name__icontains=query)
            ).distinct()
        return Monitor.objects.all()


class MonitorModelListView(ListView):
    model = MonitorModel

    def get_queryset(self):
        query = self.request.GET.get("monitor-models")

        if query:
            return MonitorModel.objects.filter(
                Q(name__icontains=query) | Q(maker__name__icontains=query)
            ).distinct()
        return MonitorModel.objects.all()


class MonitorCreateView(CreateView):
    model = Monitor
    form_class = MonitorForm


class MonitorUpdateView(UpdateView):
    model = Monitor
    form_class = MonitorForm


class MonitorModelCreateView(CreateView):
    model = MonitorModel
    form_class = MonitorModelForm


class MonitorModelUpdateView(UpdateView):
    model = MonitorModel
    form_class = MonitorModelForm


class MonitorDetailView(DetailView):
    model = Monitor


class MonitorModelDetailView(DetailView):
    model = MonitorModel
