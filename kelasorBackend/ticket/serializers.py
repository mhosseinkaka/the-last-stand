from rest_framework.serializers import ModelSerializer, StringRelatedField
from ticket.models import Ticket, TicketReply, TicketMessage


class TicketReplySerializer(ModelSerializer):
    user = StringRelatedField(read_only=True)

    class Meta:
        model = TicketReply
        fields = ['id', 'user', 'message', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

class TicketMessageSerializer(ModelSerializer):
    class Meta:
        model = TicketMessage
        fields = ['id', 'message', 'ticket_image', 'ticket_file', 'created_at']
        read_only_fields = ['id', 'created_at']

class TicketSerializer(ModelSerializer):
    message = TicketMessageSerializer(many=True, read_only=True)
    replies = TicketReplySerializer(many=True, read_only=True)

    class Meta:
        model = Ticket
        fields = ['id', 'user', 'subject', 'bootcamp', 'status', 'created_at', 'message', 'replies']
        read_only_fields = ['id', 'user', 'status', 'created_at']