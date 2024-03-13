from django.contrib import admin

from .models import Comment, Ticket, TicketCategory, TicketStatus

admin.site.register(TicketCategory)
admin.site.register(TicketStatus)
admin.site.register(Ticket)
admin.site.register(Comment)
