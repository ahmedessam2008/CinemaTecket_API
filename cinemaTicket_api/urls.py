
from django.contrib import admin
from django.db import router
from django.urls import path, include
from tickets import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register('users', views.viewsets_users)
router.register('movies', views.viewsets_movies)
router.register('reservations', views.viewsets_reservations)


urlpatterns = [
    path('admin/', admin.site.urls),
    # 1
    path("django/jsonresponsenomodel/", views.without_rest_andno_models),
    
    # 2
    path("django/jsonresponsewithmodel/", views.withmodel_no_rest),
    
    # 3-1 GET and POST form rest framework function based view @api_view
    path("rest/functionbasedviewlist/", views.function_based_view_list),
    
    
    # 3-2 GET and PUT and DELETE form rest framework function based view @api_view
    path("rest/functionbasedviewlist/<int:pk>", views.function_based_view_list_pk),
    
    # 4-1 GET and POST form rest framework Class based view APIView
    path("rest/classbasedviewlist/", views.Class_Based_View.as_view()),
    
    # 4-2 GET and PUT and DELETE form rest framework Class based view APIView
    path("rest/classbasedviewlist/<int:pk>", views.Class_Based_View_pk.as_view()),
    
    # 5-1 GET and POST form rest framework Class based view mixins
    path("rest/mixins/", views.mixins_list_create.as_view()),
    
    # 5-2 GET and PUT and DELETE form rest framework Class based view mixins
    path("rest/mixins/<int:pk>", views.mixins_pk.as_view()),
    
    # 6-1 GET and POST form rest framework Class based view generics
    path("rest/generics/", views.generics_ist_create.as_view()),
    
    # 6-2 GET and PUT and DELETE form rest framework Class based view generics
    path("rest/generics/<int:pk>", views.generics_pk.as_view()),
    
    # 7 ViewSets rest framework
    path("rest/viewsets/", include(router.urls)),
    
    # 8 Find Movie By function based view
    path("rest/findmovie/", views.find_movie),
    
    # 9 new reservation function based view
    path("rest/newreservation/", views.new_reservation),
    
    # 10 rest auth url ====> To make logout button in the page
    path("api-auth", include('rest_framework.urls')),
    
    # Token Authentication url
    path("api-token-auth", obtain_auth_token),
    
    
]
