from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Max

UserModel = get_user_model()



class ChatMessage(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='user')
    sender = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='from_user')
    recipient = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='to_user')

    body = models.CharField(
        max_length=255,
        null=True,
    )

    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(
        default=False
    )

    @staticmethod
    def send_message(from_user, to_user, body):
        sender_message = ChatMessage(
            user=from_user,
            sender=from_user,
            recipient=to_user,
            body=body,
            is_read=True
        )
        sender_message.save()

        recipient_message = ChatMessage(
            user=to_user,
            sender=from_user,
            body=body,
            recipient=from_user
        )
        recipient_message.save()

        return sender_message

    @staticmethod
    def get_messages(user):
        users = []
        messages = ChatMessage.objects.filter(user=user).\
            values('recipient').annotate(last=Max('date')).\
            order_by('-last')

        for message in messages:
            users.append({
                'user': UserModel.objects.get(pk=message['recipient']),
                'last': message['last'],
                'unread': ChatMessage.objects.filter(
                    user=user, recipient__pk=message['recipient'],
                    is_read=False).count()
            })

        return users



    #
    # author = models.ForeignKey(UserModel, on_delete=models.RESTRICT,)
    #
    # chat = models.ForeignKey(Chat, on_delete=models.RESTRICT)
    #
