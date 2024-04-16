from django.urls import path
from . import views



urlpatterns = [
    path('', views.index, name="index"),
    path('signup/', views.signUp, name='signup'),
    path('login/', views.Login, name='login'),
    path('logout/', views.Logout, name='logout'),
    path('contribution/', views.contribution, name='contribution'),
    path('<int:movie_id>/', views.detail, name='detail'),
    path('wishlist/', views.wishList, name='wishlist'),
    path('add-movies', views.add_movies, name='add-movies'),
    path('update/<int:movie_id>',views.updateMovie,name='updateMovie'),
    path('delete/<int:movieId>/', views.deleteMovie, name='deleteMovie'),
    path('genreview/', views.genreview, name='genreview'),
    path('search/', views.search, name='search'),
    

    
]