from django.contrib import admin
from ticket.models import Ticket, TicketReply

# Register your models here.
admin.site.register(Ticket)
admin.site.register(TicketReply)