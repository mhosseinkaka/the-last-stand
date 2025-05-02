from rest_framework.serializers import ModelSerializer
from ticket.models import Ticket, TicketReply


class TicketReplySerializer(ModelSerializer):
    class Meta:
        model = TicketReply
        fields = ['id', 'user', 'message', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

class TicketSerializer(ModelSerializer):
    replies = TicketReplySerializer(many=True, read_only=True)

    class Meta:
        model = Ticket
        fields = ['id', 'user', 'subject', 'message', 'status', 'created_at', 'replies']
        read_only_fields = ['id', 'user', 'status', 'created_at']