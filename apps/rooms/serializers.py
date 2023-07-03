from rest_framework import serializers
from .models import Room, Message


class MessageSerializer(serializers.ModelSerializer):
    room = serializers.SlugRelatedField(slug_field='slug', read_only=True)
    sender = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Message
        fields = ['room', 'sender', 'content', 'created_at']


class BaseRoomSerializer(serializers.ModelSerializer):
    "serializer for annonymous users"

    class Meta:
        model = Room
        fields = [
            'name',
        ]


class RoomSerializer(serializers.ModelSerializer):
    "serializer for authenticated users"
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ['name', 'messages']
