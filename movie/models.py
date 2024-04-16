from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'genre'
        verbose_name_plural = 'genres'
        
    def __str__(self):
        return self.name
    
    def get_url(self):
        return reverse('login',args=[self.slug])
    
class Movie(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, unique=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    movie_logo = models.ImageField(upload_to='movie-logo', blank=True)
    description = models.TextField(blank=True)
    year = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
        
    class Meta:
        ordering = ('title',)
        verbose_name = 'movie'
        verbose_name_plural = 'movies'
        
    def __str__(self):
        return self.title
    def get_url(self):
        return reverse('index', args=[self.genre.slug,self.slug])


class Myrating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    
    
class MyList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    watch = models.BooleanField(default=False)