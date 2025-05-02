from django.urls import path
from ticket.views import CreateTicketView, MyTicketsView, AllTicketsView, ReplyTicketView

urlpatterns = [
    path('create-ticket/', CreateTicketView.as_view(), name='ticket-create'),
    path('my-tickets/', MyTicketsView.as_view(), name='my-tickets'),
    path('all-tickets/', AllTicketsView.as_view(), name='all-tickets'),
    path('<int:ticket_id>/reply/', ReplyTicketView.as_view(), name='ticket-reply'),
]