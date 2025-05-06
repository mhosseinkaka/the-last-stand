from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from ticket.models import Ticket, TicketReply
from ticket.serializers import TicketSerializer, TicketReplySerializer
from rest_framework.permissions import IsAuthenticated
from user.permissions import IsSupportUser
from rest_framework.response import Response
from rest_framework import status

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


class CloseTicketView(UpdateAPIView):
    queryset = Ticket.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def patch(self, request, *args, **kwargs):
        ticket = self.get_object()

        if ticket.user != request.user and not request.user.groups.filter(name='Supports').exists():
            return Response({"detail": "شما اجازه بستن این تیکت را ندارید."}, status=status.HTTP_403_FORBIDDEN)

        if ticket.status == 'closed':
            return Response({"detail": "این تیکت قبلاً بسته شده است."}, status=status.HTTP_400_BAD_REQUEST)

        ticket.status = 'closed'
        ticket.save()

        return Response({"detail": "تیکت با موفقیت بسته شد."}, status=status.HTTP_200_OK)