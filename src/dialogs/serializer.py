from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Thread, Message


User = get_user_model()


class CreateThreadSerializer(serializers.Serializer):

    default_error_messages = {
        'not_found': 'user(s) does not exist or incorrect',
    }

    participants = serializers.ListSerializer(
        child=serializers.IntegerField(), required=True, write_only=True)

    class Meta:
        fields = (
            'participants',
        )

    def validate_participants(self, participants: list) -> User:
        qs = User.objects.filter(id__in=participants)\
                         .exclude(type=User.ADMIN)\
                         .values_list('id', flat=True)
        if qs.count() != len(participants):
            self.fail('not_found')

        creator_id = self.context['request'].user.pk
        return [*qs, creator_id]

    def create(self, validated_data: dict) -> dict:
        tr = Thread.objects.create()
        tr.participants.add(*validated_data['participants'])

        return {}



class ThreadSerializer(serializers.ModelSerializer):

    participant = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Thread
        fields = (
            'id',
            'participant',
        )


class CreateMessageSerializer(serializers.ModelSerializer):

    default_error_messages = {
        'invalid_user': 'user {user_id} not in thread participants',
    }

    sender = serializers.HiddenField(default=serializers.CreateOnlyDefault(serializers.CurrentUserDefault()))
    thread = serializers.PrimaryKeyRelatedField(queryset=Thread.objects.all(), write_only=True)

    class Meta:
        model = Message
        fields = (
            'text',
            'sender',
            'thread',
        )

    def validate(self, attrs):
        tr = attrs['thread']
        user_id = attrs['sender'].id
        if not tr.participants.filter(id=user_id).exists():
            self.fail('invalid_user', user_id=user_id)

        return attrs
