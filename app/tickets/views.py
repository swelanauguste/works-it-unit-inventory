from clients.models import Client
from django.contrib import messages
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from users.models import User

from .forms import (
    CommentCreateForm,
    TicketAssignTechnicianForm,
    TicketCreateForm,
    TicketUpdateForm,
)
from .models import Comment, Ticket, TicketStatus


class TicketUpdateView(UpdateView):
    model = Ticket
    form_class = TicketUpdateForm

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


def closed_ticket_view(request, slug):
    ticket = get_object_or_404(Ticket, slug=slug)
    ticket.is_closed = True
    ticket.ticket_status = TicketStatus.objects.get(name="closed")
    ticket.updated_by = request.user
    ticket.save()
    messages.success(request, f"Your ticket {ticket} has been closed")
    return redirect("ticket-open-list")


def assign_technician_view(request, slug):
    ticket = get_object_or_404(Ticket, slug=slug)

    if request.method == "POST":
        form = TicketAssignTechnicianForm(request.POST)
        if form.is_valid():
            technician_id = form.cleaned_data["technician_id"]
            technician = get_object_or_404(User, id=technician_id.id)
            ticket.assigned_to = technician
            ticket.save()
            return redirect("ticket-detail", slug=ticket.slug)
    else:
        form = AssignTechnicianForm()

    return render(
        request, "tickets/assign_technician.html", {"form": form, "ticket": ticket}
    )


def create_ticket_view(request):
    if request.method == "POST":
        form = TicketCreateForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data["email"]
            summary = form.cleaned_data["summary"]
            description = form.cleaned_data["description"]
            file = form.cleaned_data["file"]
            print(file, "file")

            try:
                client = Client.objects.get(email=email)
            except ObjectDoesNotExist:
                # Add a custom error to the form for the email field
                form.add_error(
                    "email", "Email address not found, please contact support"
                )
                return render(request, "tickets/create_ticket.html", {"form": form})

            ticket = Ticket.objects.create(
                user=client, summary=summary, file=file, description=description
            )
            ticket.save()
            send_ticket_creation_email(ticket, email)
            messages.success(request, "Ticket was created successfully")
            return redirect("ticket-detail", slug=ticket.slug)
    else:
        form = TicketCreateForm()

    context = {"form": form}
    return render(request, "tickets/create_ticket.html", context)


def send_ticket_creation_email(ticket, recipient_email):
    current_site = Site.objects.get_current()
    domain = current_site.domain

    subject = f"New Ticket {ticket.ticket_id}"
    ticket_url = reverse("ticket-detail", kwargs={"slug": ticket.slug})
    full_url = f"http://{domain}{ticket_url}"

    html_message = render_to_string(
        "tickets/email_template.html", {"ticket": ticket, "full_url": full_url}
    )
    plain_message = strip_tags(html_message)

    send_mail(
        subject,
        plain_message,
        "it.works@mail.local",
        [recipient_email],
        html_message=html_message,
    )


class TicketOpenListView(ListView):
    model = Ticket
    paginate_by = 25

    def get_queryset(self):
        return (
            Ticket.objects.filter(is_closed=False)
            if Ticket.objects.filter(is_closed=False).exists()
            else Ticket.objects.none()
        )


class TicketClosedListView(ListView):
    model = Ticket
    paginate_by = 25

    def get_queryset(self):
        return (
            Ticket.objects.filter(is_closed=True)
            if Ticket.objects.filter(is_closed=True).exists()
            else Ticket.objects.none()
        )


class ClientTicketListView(ListView):
    model = Ticket
    template_name = "tickets/customer_ticket_list.html"

    def get_queryset(self):
        query = self.request.GET.get("ticket")

        if query:
            return Ticket.objects.filter(Q(ticket_id__iexact=query)).distinct()
        return Ticket.objects.none()


class TicketDetailView(DetailView):
    model = Ticket

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = CommentCreateForm()
        context["assign_technician_form"] = TicketAssignTechnicianForm()
        return context


def add_comment_view(request, slug):
    ticket = get_object_or_404(Ticket, slug=slug)

    if request.method == "POST":
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.ticket = ticket
            comment.save()
            return redirect("ticket-detail", slug=slug)

    # If the form is not valid or the request method is not POST
    return render(
        request, "ticket_detail.html", {"ticket": ticket, "comment_form": form}
    )
