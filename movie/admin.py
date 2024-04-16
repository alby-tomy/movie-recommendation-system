from django.contrib import admin
from .models import Movie, Genre, MyList, Myrating

# Register your models here.
admin.site.register(Myrating)
admin.site.register(MyList)


class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)} 
admin.site.register(Genre, GenreAdmin)

class MovieAdmin(admin.ModelAdmin):
    list_display = ['id','title', 'genre', 'slug']
    prepopulated_fields = {'slug':('title',)}
    list_per_page = 10
    
admin.site.register(Movie, MovieAdmin)