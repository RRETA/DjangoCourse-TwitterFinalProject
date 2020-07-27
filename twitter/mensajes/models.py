from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Mensaje(models.Model):
    user = models.ForeignKey(User,related_name='mensajes',on_delete=models.CASCADE)
    title = models.CharField(max_length=140)
    mensaje = models.TextField(blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.title} by  {self.user.first_name}'
