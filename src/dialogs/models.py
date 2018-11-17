from django.db import models

# API urls для:
#   - создания Thread'a(создавать может только Admin, максимум 1 Admin в Thread'е)
#   - создания Message для Participant'ов Thread'a
#   - получения списка Thread'ов юзера
#   - получения сообщений из Thread'a
#   - добавления/удаления Driver'а из Thread'a(удалять может только Admin, если в Thread'e не остается никого кроме Admin'a - удалять сам Thread)

class BasicModel(models.Model):
    created = models.DateField(auto_now=True)
    updated = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True


class Thread(BasicModel):

    participants = models.ManyToManyField('accounts.CustomUser', related_name='threads')


class Message(BasicModel):

    text = models.CharField(max_length=512)
    sender = models.ForeignKey('accounts.CustomUser', related_name='messages',
                               on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, related_name='messages', on_delete=models.CASCADE)

