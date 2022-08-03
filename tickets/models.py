from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

class Movie(models.Model):
  hall = models.CharField(max_length=100)
  movie = models.CharField(max_length=100)
  date = models.DateTimeField()
  
  class Meta:
    ordering= ['-date']
    
  def __str__(self):
    return self.movie
  
  
class UserData(models.Model):
  name = models.CharField(max_length=100)
  mobile = models.CharField(max_length=100)
  date_added = models.DateTimeField(auto_created=True, null=True, blank=True)
  
  class Meta:
    ordering= ['-date_added']
    
  def __str__(self):
    return self.name
  
  
class Reservation(models.Model):
  userdata = models.ForeignKey(UserData, on_delete=models.CASCADE, related_name="reservation")
  movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reservation")
  
# To create token key every time create user
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def TokenCreate(sender, instance, created, **kwargs):
  if created:
    Token.objects.create(user=instance)