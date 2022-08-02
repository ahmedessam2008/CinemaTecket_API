from dataclasses import field
from .models import Movie, Reservation, UserData
from rest_framework import serializers

class MovieSerializer(serializers.ModelSerializer):
  class Meta:
    model= Movie
    fields= "__all__"

class ReservationSerializer(serializers.ModelSerializer):
  class Meta:
    model= Reservation
    fields= "__all__"

class UserDataSerializer(serializers.ModelSerializer):
  class Meta:
    model= UserData
    fields= ["pk", 'reservation', "name", "mobile"]