from django.urls import path

from .views import (
    ClientTicketListView,
    TicketDetailView,
    TicketListView,
    TicketUpdateView,
    add_comment_view,
    assign_technician_view,
    create_ticket_view,
)

urlpatterns = [
    path("", create_ticket_view, name="ticket-create"),
    path("client/tickets/", ClientTicketListView.as_view(), name="client-ticket-list"),
    path("tickets/", TicketListView.as_view(), name="ticket-list"),
    path(
        "tickets/detail/<slug:slug>/", TicketDetailView.as_view(), name="ticket-detail"
    ),
    path(
        "tickets/update/<slug:slug>/", TicketUpdateView.as_view(), name="ticket-update"
    ),
    path(
        "assign-technician/<slug:slug>/",
        assign_technician_view,
        name="assign-technician",
    ),
    path("ticket/add-comment/<slug:slug>/", add_comment_view, name="add-comment"),
]
