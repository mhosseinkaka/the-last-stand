from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, get_object_or_404
from ticket.models import Ticket, TicketReply, TicketMessage
from ticket.serializers import TicketSerializer, TicketReplySerializer, TicketMessageSerializer
from rest_framework.permissions import IsAuthenticated
from user.permissions import IsSupportUser, IsSuperUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from bootcamp.models import Bootcamp
from sms_ir import *
from kavenegar import *
import http.client
import json

# Create your views here.

class CreateTicketView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        subject = request.data.get('subject')
        message = request.data.get('message')
        bootcamp_id = request.data.get('bootcamp')
        image = request.FILES.get('ticket_image')
        file = request.FILES.get('ticket_file')

        bootcamp = Bootcamp.objects.filter(id=bootcamp_id).first() if bootcamp_id else None
        ticket = Ticket.objects.create(user=request.user, subject=subject, bootcamp=bootcamp)
        TicketMessage.objects.create(ticket=ticket, message=message, ticket_image=image, ticket_file=file)

        serializer = TicketSerializer(ticket)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

#normal user
class MyTicketsView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TicketSerializer

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user)

#support
class AllTicketsView(ListAPIView):
    permission_classes = [IsSupportUser | IsSuperUser]
    queryset = Ticket.objects.all().order_by('-created_at')
    serializer_class = TicketSerializer
    

#support
class ReplyTicketView(CreateAPIView):
    serializer_class = TicketReplySerializer
    permission_classes = [IsSupportUser | IsSuperUser]

    def perform_create(self, serializer):
        ticket_id = self.kwargs['ticket_id']
        ticket = get_object_or_404(Ticket, id=ticket_id)
        ticket.status = 'answered'
        ticket.save()
        serializer.save(ticket=ticket, user=self.request.user)
        try:
            conn = http.client.HTTPSConnection("api.sms.ir")
            payload = json.dumps({
                                "lineNumber": 30002108001178,
                                "messageText": f"پاسخ تیکت شما داده شد.",
                                "mobiles": [ticket.user.phone],      
                                })
            headers = {
                'X-API-KEY': '...',
                'Content-Type': 'application/json'}
            conn.request("POST", "/v1/send/bulk", payload, headers)
            res = conn.getresponse()
            data = res.read()
            print(data.decode("utf-8"))
            # api = KavenegarAPI('...')
            # params = { 'sender' : '2000660110', 'receptor': ticket.user.phone, 'message' :f"پاسخ تیکت شما داده شد." }
            # api.sms_send(params)
        except (APIException, HTTPException) as e:
            print("sms.ir error:", e)
            return Response({"detail": "ارسال پیامک با مشکل مواجه شد."}, status=400)


class CloseTicketView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        ticket = get_object_or_404(Ticket, id=pk)

        if ticket.user != request.user and not request.user.groups.filter(name='Supports').exists():
            return Response({"detail": "اجازه ندارید این تیکت را ببندید."}, status=403)

        if ticket.status == 'closed':
            return Response({"detail": "تیکت قبلاً بسته شده."}, status=400)

        ticket.status = 'closed'
        ticket.save()
        return Response({"detail": "تیکت بسته شد."}, status=200)
    

class AddMessageToTicketView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, ticket_id):
        ticket = get_object_or_404(Ticket, id=ticket_id)

            
        if ticket.status == 'closed':
            return Response({"detail": "این تیکت بسته شده و امکان ارسال پیام جدید وجود ندارد."},
                            status=status.HTTP_400_BAD_REQUEST)

            
        if ticket.user != request.user and not request.user.groups.filter(name='Supports').exists():
            return Response({"detail": "شما مجاز به ارسال پیام در این تیکت نیستید."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = TicketMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ticket=ticket)
            if ticket.status == 'new':
                ticket.status = 'in_progress'
                ticket.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)