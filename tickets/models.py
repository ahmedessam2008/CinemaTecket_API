from django.db import models

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
  