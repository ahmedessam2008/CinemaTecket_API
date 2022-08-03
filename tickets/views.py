from email.policy import HTTP
from django.shortcuts import render
from django.http.response import JsonResponse
from .models import UserData, Movie, Reservation
from .serializers import UserDataSerializer, ReservationSerializer, MovieSerializer
from rest_framework.response import Response
from rest_framework import status, filters
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import mixins, generics, viewsets
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny, IsAuthenticatedOrReadOnly

from tickets import serializers
# Create your views here.
# 1- Without Rest Framework and No Models
def without_rest_andno_models(requrest):

  guests = [
    {
      'id': 1,
      "name": "Ahmed",
      "mobile": "201027372008"
    },
    {
      'id': 2,
      "name": "Mazen",
      "mobile": "201020690100"
    },
    {
      'id': 3,
      "name": "Yazan",
      "mobile": "201000713650"
    },
    
  ]
  return JsonResponse(guests, safe=False)
############################################
# 2- with Model and without Rest framework
def withmodel_no_rest(request):
  data = UserData.objects.all()
  response = {
    'userdata': list(data.values('name', 'mobile'))
  }
  return JsonResponse(response)
############################################

# list == GET
# Create == POST 

# pk query == GET
# update == PUT
# delete or destroy == DELETE


# 3- Function Based View (FBV)
# 3.1 GET and POST

@api_view(['GET', 'POST'])
def function_based_view_list(request):
  
  # GET
  if request.method == "GET":
    usersdata = UserData.objects.all()
    serializer = UserDataSerializer(usersdata, many=True)
    return Response(serializer.data)
  
  # POST 
  if request.method == "POST":
    serializer = UserDataSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
      return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

# 3.2 GET and PUT and DELETE
@api_view(['GET', 'PUT', 'DELETE'])
def function_based_view_list_pk(request, pk):
  try:
    userdata = UserData.objects.get(pk=pk)
  except UserData.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)
  
  # GET
  if request.method == "GET":
    serializer = UserDataSerializer(userdata)
    return Response(serializer.data)
  
  # PUT
  if request.method == "PUT":
    serializer = UserDataSerializer(userdata, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
  # DELETE
  if request.method == "DELETE":
    userdata.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
  
####################################################################################

# 4- Class based views (CBV)
# 4-1 List and Create == GET , POST
class Class_Based_View(APIView):
  
  # GET
  def get(self, request):
    usersdata = UserData.objects.all()
    serializer = UserDataSerializer(usersdata, many=True)
    return Response(serializer.data)
  
  # POST
  def post(self, request):
    serializer = UserDataSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
      return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    
# 4-2 List and Update and Delete == GET , PUT , DELETE
class Class_Based_View_pk(APIView):
  # Get the pk 
  def get_object(self, pk):
    try:
      return UserData.objects.get(pk=pk)
    except UserData.DoesNotExist:
      raise Http404
    
  # GET 
  def get(self, request, pk):
    userdata = self.get_object(pk)
    serializer = UserDataSerializer(userdata)
    return Response(serializer.data)
  
  # PUT
  def put(self, request, pk):
    userdata = self.get_object(pk=pk)
    serializer = UserDataSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
  # DELETE
  def delete(self, request, pk):
    userdata = self.get_object(pk=pk)
    userdata.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

###########################################################################

# 5 Maxins 
# 5-1 maxins list and create
class mixins_list_create(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
  queryset = UserData.objects.all()
  serializer_class = UserDataSerializer
  
  # Get
  def get(self, request):
    return self.list(request)
  
  # Post
  def post(self, request):
    return self.create(request)
  
# 5-1 maxins lsit and update and delete

class mixins_pk(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
  queryset = UserData.objects.all()
  serializer_class = UserDataSerializer
  
  # Get
  def get(self, request, pk):
    return self.retrieve(request)
  
  # Update
  def put(self, request, pk):
    return self.update(request)
  
  # Delete
  def delete(self, request, pk):
    return self.destroy(request)
  
###########################################################################################  
  
# 6 Generics
# 6-1 List and Create
class generics_ist_create(generics.ListCreateAPIView):
  queryset = UserData.objects.all()
  serializer_class = UserDataSerializer
  # authentication_classes = [BasicAuthentication]
  authentication_classes = [TokenAuthentication]
  # permission_classes = [IsAuthenticated]
  
# 6-2 Retrive and Update and Destroy 
class generics_pk(generics.RetrieveUpdateDestroyAPIView):
  queryset = UserData.objects.all()
  serializer_class = UserDataSerializer
  # authentication_classes = [BasicAuthentication]
  authentication_classes = [TokenAuthentication]
  # permission_classes = [IsAuthenticated]
  
#####################################################################################

# 7 ViewSets

class viewsets_users(viewsets.ModelViewSet):
  queryset = UserData.objects.all()
  serializer_class = UserDataSerializer

class viewsets_movies(viewsets.ModelViewSet):
  queryset = Movie.objects.all()
  serializer_class = MovieSerializer
  
  # this is some addition
  filter_backends = [filters.SearchFilter]
  search_fields = ['movie']

class viewsets_reservations(viewsets.ModelViewSet):
  queryset = Reservation.objects.all()
  serializer_class = ReservationSerializer
  
# 8 Find The movie
@api_view(['GET'])
def find_movie(request):
  movie = Movie.objects.filter(
    movie=request.data['movie'], 
    hall=request.data['hall'],)
  serializer = MovieSerializer(movie, many=True)
  return Response(serializer.data)

# 9 Create a new reservations
@api_view(['POST'])
def new_reservation(request):
  movie = Movie.objects.get(movie=request.data['movie'], hall=request.data['hall'])
  
  userdata = UserData()
  userdata.name = request.data['name']
  userdata.mobile = request.data['mobile']
  userdata.date_added = request.data['date_added']
  userdata.save()
  
  reservation = Reservation()
  reservation.movie = movie
  reservation.userdata = userdata
  reservation.save()
  return Response(status=status.HTTP_201_CREATED)
  
  