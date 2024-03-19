from django.urls import path

from .views import (
    ClientTicketListView,
    TicketDetailView,
    TicketOpenListView,
    TicketClosedListView,
    TicketUpdateView,
    add_comment_view,
    assign_technician_view,
    create_ticket_view,
    closed_ticket_view,
)

urlpatterns = [
    path("", create_ticket_view, name="ticket-create"),
    path("client/tickets/", ClientTicketListView.as_view(), name="client-ticket-list"),
    path("open-tickets/", TicketOpenListView.as_view(), name="ticket-open-list"),
    path("closed-tickets/", TicketClosedListView.as_view(), name="ticket-closed-list"),
    path(
        "tickets/detail/<slug:slug>/", TicketDetailView.as_view(), name="ticket-detail"
    ),
    path(
        "tickets/closed/<slug:slug>/", closed_ticket_view, name="ticket-closed"
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
