from django.contrib import admin
from .models import Movie, Reservation, UserData


class MovieAdmin(admin.ModelAdmin):
  list_display = ['movie', 'hall', 'date']
  list_display_links = ['movie', 'date']
  list_editable = ['hall']
  search_fields = ['movie']
  list_filter = ['movie', 'date']
  
admin.site.register(Movie, MovieAdmin)

admin.site.site_header = "Cinema Ticket"
admin.site.site_title = "Cinema | Admin"

admin.site.register(UserData)
admin.site.register(Reservation)
