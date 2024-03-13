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
from .forms import (
    CommentCreateForm,
    ComputerForm,
    # GetComputerNameForm,
    MicrosoftOfficeUpdateForm,
    MonitorForm,
    PrinterForm,
)
from .models import (
    Computer,
    ComputerComment,
    ComputerModel,
    # ComputerName,
    ComputerType,
    Maker,
    MicrosoftOffice,
    Monitor,
    MonitorModel,
    Printer,
    PrinterModel,
    Status,
)


# def get_next_computer_name_view(request):
#     form = GetComputerNameForm()
#     computer_name_prefix = "MCWT"
#     last_computer_name = ComputerName.objects.order_by("-last_used_number").first()

#     if request.method == "POST":
#         form = GetComputerNameForm(request.POST)
#         if form.is_valid():
#             if last_computer_name:
#                 # Increment the last used number to get the next sequence
#                 next_number = last_computer_name.last_used_number + 1
#             else:
#                 # If no computers exist yet, start from 1
#                 next_number = 1

#             # Combine prefix with next number to get the full computer name
#             next_computer_name = f"{computer_name_prefix}{next_number}"

#             # Save the new computer name with the incremented number
#             ComputerName.objects.create(
#                 computer_name=next_computer_name, last_used_number=next_number
#             )

#             # Redirect or update context as necessary
#             return redirect(
#                 "computer-create"
#             )  # Replace 'your_success_url' with your actual URL name

#     else:
#         # If GET request or the form is not valid, show the form again with the next predicted name
#         if last_computer_name:
#             next_number = last_computer_name.last_used_number + 1
#         else:
#             next_number = 1
#         next_computer_name = f"{computer_name_prefix}{next_number}"
#         context = {
#             "form": form,
#             "next_computer_name": next_computer_name,  # Provide the predicted next computer name in context
#         }
#         return render(request, "assets/get_computer_name.html", context)


def computer_filter_view(request):
    f = ComputerFilter(request.GET, queryset=Computer.objects.all())
    return render(request, "assets/computer_filter.html", {"filter": f})


def printer_filter_view(request):
    f = PrinterFilter(request.GET, queryset=Printer.objects.none())
    return render(request, "assets/printer_filter.html", {"filter": f})


class MicrosoftOfficeListView(LoginRequiredMixin, ListView):
    model = MicrosoftOffice

    def get_queryset(self):
        queryset = MicrosoftOffice.objects.filter(is_installed=False)
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
        if form.instance.date_installed and not form.cleaned_data.get(
            "has_failed", False
        ):
            form.instance.is_installed = True
            form.instance.has_failed = (
                False  # Explicitly setting this in case of re-activation attempts
            )
        else:
            form.instance.is_installed = False
            form.instance.has_failed = True
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
    paginate_by = 25

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


class ComputerCreateView(CreateView):
    model = Computer
    form_class = ComputerForm

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # context["last_computer_name"] = ComputerName.objects.order_by(
    #     #     "-computer_name"
    #     # ).first()
    #     # context["get_computer_name_form"] = GetComputerNameForm
    #     return context


# class ComputerCreateView(CreateView):
#     model = Computer
#     form_class = ComputerForm
#     success_url = reverse_lazy("computer-list")  # Adjust with your actual success URL
    
#     def get_initial(self):
#         initial = super().get_initial()
        
#         # Compute the next computer name
#         last_computer_name_instance = ComputerName.objects.order_by("-last_used_number").first()
#         if last_computer_name_instance:
#             next_number = last_computer_name_instance.last_used_number + 1
#         else:
#             next_number = 1
#         next_computer_name = f"MCWT{next_number}"
        
#         # Set the initial value for the computer_name field
#         initial['computer_name'] = next_computer_name
#         return initial

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     last_computer_name_instance = ComputerName.objects.order_by(
    #         "-last_used_number"
    #     ).first()
    #     if last_computer_name_instance:
    #         # Increment the last used number for the next computer name
    #         next_computer_name = (
    #             f"MCWT{last_computer_name_instance.last_used_number + 1}"
    #         )
    #     else:
    #         next_computer_name = "MCWT1"
    #     context["next_computer_name"] = next_computer_name
    #     return context

    # def form_valid(self, form):
    #     # This is where you handle what happens after the form is submitted and valid
    #     # It's also where you'd typically save your model instance

    #     # First, let's save the Computer instance
    #     self.object = form.save(commit=False)
    #     self.object.computer_name = form.cleaned_data.get('computer_name', '')
    #     self.object.save()

    #     # Now update the ComputerName instance
    #     last_used_number = int(self.object.computer_name.replace("MCWT", ""))  # Extract the number part
    #     ComputerName.objects.create(
    #         computer_name=self.object.computer_name,
    #         last_used_number=last_used_number
    #     )

    #     return super().form_valid(form)


class ComputerUpdateView(UpdateView):
    model = Computer
    form_class = ComputerForm


class ComputerModelCreateView(CreateView):
    model = ComputerModel
    fields = "__all__"


class ComputerModelUpdateView(UpdateView):
    model = ComputerModel
    fields = "__all__"


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


class PrinterUpdateView(UpdateView):
    model = Printer
    form_class = PrinterForm


class PrinterModelCreateView(CreateView):
    model = PrinterModel
    fields = "__all__"


class PrinterModelUpdateView(UpdateView):
    model = PrinterModel
    fields = "__all__"


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
    fields = "__all__"


class MonitorModelUpdateView(UpdateView):
    model = MonitorModel
    fields = "__all__"


class MonitorDetailView(DetailView):
    model = Monitor


class MonitorModelDetailView(DetailView):
    model = MonitorModel