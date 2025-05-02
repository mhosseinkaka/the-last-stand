from rest_framework.generics import ListAPIView, CreateAPIView
from ticket.models import Ticket, TicketReply
from ticket.serializers import TicketSerializer, TicketReplySerializer
from rest_framework.permissions import IsAuthenticated
from user.permissions import IsSupportUser

# Create your views here.

class CreateTicketView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

#normal user
class MyTicketsView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TicketSerializer

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user)

#support
class AllTicketsView(ListAPIView):
    permission_classes = [IsAuthenticated, IsSupportUser]
    queryset = Ticket.objects.all().order_by('-created_at')
    serializer_class = TicketSerializer
    

#support
class ReplyTicketView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsSupportUser]
    queryset = Ticket.objects.all()
    serializer_class = TicketReplySerializer
    
    def perform_create(self, serializer):
        ticket_id = self.kwargs['ticket_id']
        ticket = Ticket.objects.get(id=ticket_id)
        ticket.status = 'answered'
        ticket.save()
        serializer.save(ticket=ticket, user=self.request.user)