from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect
from .forms import *  #user form importing forms.py
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
import pandas as pd
from django.db.models import Case, When



# # To get similar movies based on user rating
# def get_similar(movie_name,rating,corrMatrix):
#     similar_ratings = corrMatrix[movie_name]*(rating-2.5)
#     similar_ratings = similar_ratings.sort_values(ascending=False)
#     return similar_ratings


# def recommend(request):
#     if not request.user.is_authenticated:
#         return redirect("login")
#     if not request.user.is_active:
#         raise Http404


#     movie_rating=pd.DataFrame(list(Myrating.objects.all().values()))

#     new_user=movie_rating.user_id.unique().shape[0]
#     current_user_id= request.user.id
# 	# if new user not rated any movie
#     if current_user_id>new_user:
#         movie=Movie.objects.get(id=19)
#         q=Myrating(user=request.user,movie=movie,rating=0)
#         q.save()


#     userRatings = movie_rating.pivot_table(index=['user_id'],columns=['movie_id'],values='rating')
#     userRatings = userRatings.fillna(0,axis=1)
#     corrMatrix = userRatings.corr(method='pearson')

#     user = pd.DataFrame(list(Myrating.objects.filter(user=request.user).values())).drop(['user_id','id'],axis=1)
#     user_filtered = [tuple(x) for x in user.values]
#     movie_id_watched = [each[0] for each in user_filtered]

#     similar_movies = pd.DataFrame()
#     for movie,rating in user_filtered:
#         similar_movies = similar_movies.append(get_similar(movie,rating,corrMatrix),ignore_index = True)

#     movies_id = list(similar_movies.sum().sort_values(ascending=False).index)
#     movies_id_recommend = [each for each in movies_id if each not in movie_id_watched]
#     preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(movies_id_recommend)])
#     movie_list=list(Movie.objects.filter(id__in = movies_id_recommend).order_by(preserved)[:10])

#     context = {'movie_list': movie_list}
#     return render(request, 'recommend.html', context)


def search(request):
    query = request.GET.get('q')
    if query:
        movies = Movie.objects.filter(title__icontains=query)
    else:
        movies = Movie.objects.all()
    return render(request, 'search.html', {'movies': movies, 'query':query})


# Create your views here.
def index(request):
    movies = Movie.objects.all()
    query = request.GET.get('q')

    if query:
        movies = Movie.objects.filter(Q(title__icontains=query)).distinct()
        return render(request, 'list.html', {'movies': movies})

    return render(request, 'list.html', {'movies': movies})


def genreview(request):
    genres_with_movies = []
    genres = Genre.objects.all()
    for genre in genres:
        movies = Movie.objects.filter(genre=genre)
        genres_with_movies.append({'genre': genre, 'movies': movies})

    # Get the search query from the request
    query = request.GET.get('q')

    if query:
        # Filter movies by title if a search query is present
        movies = Movie.objects.filter(title__icontains=query).distinct()
        return render(request, 'genreview.html', {'movies': movies})

    return render(request, 'genreview.html', {'genres_with_movies': genres_with_movies})



# Show details of the movie
def detail(request, movie_id):  
    if not request.user.is_authenticated:
        return redirect("login")
    if not request.user.is_active:
        raise Http404
    movies = get_object_or_404(Movie, id=movie_id)
    movie = Movie.objects.get(id=movie_id)
    
    temp = list(MyList.objects.all().values().filter(movie_id=movie_id,user=request.user))
    if temp:
        update = temp[0]['watch']
    else:
        update = False
    if request.method == "POST":

        # For my list
        if 'watch' in request.POST:
            watch_flag = request.POST['watch']
            if watch_flag == 'on':
                update = True
            else:
                update = False
            if MyList.objects.all().values().filter(movie_id=movie_id,user=request.user):
                MyList.objects.all().values().filter(movie_id=movie_id,user=request.user).update(watch=update)
            else:
                q=MyList(user=request.user,movie=movie,watch=update)
                q.save()
            if update:
                messages.success(request, "Movie added to your list!")
            else:
                messages.success(request, "Movie removed from your list!")

            
        # For rating
        else:
            rate = request.POST['rating']
            if Myrating.objects.all().values().filter(movie_id=movie_id,user=request.user):
                Myrating.objects.all().values().filter(movie_id=movie_id,user=request.user).update(rating=rate)
            else:
                q=Myrating(user=request.user,movie=movie,rating=rate)
                q.save()

            messages.success(request, "Rating has been submitted!")

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    out = list(Myrating.objects.filter(user=request.user.id).values())

    # To display ratings in the movie detail page
    movie_rating = 0
    rate_flag = False
    for each in out:
        if each['movie_id'] == movie_id:
            movie_rating = each['rating']
            rate_flag = True
            break

    context = {'movies': movies,'movie_rating':movie_rating,'rate_flag':rate_flag,'update':update}
    return render(request, 'detail.html', context)



# MyList functionality
def wishList(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if not request.user.is_active:
        raise Http404

    movies = Movie.objects.filter(mylist__watch=True,mylist__user=request.user)
    query = request.GET.get('q')

    if query:
        movies = Movie.objects.filter(Q(title__icontains=query)).distinct()
        return render(request, 'wish-list.html', {'movies': movies})

    return render(request, 'wish-list.html', {'movies': movies})


# Register user
def signUp(request):
    form = UserForm(request.POST or None)

    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("index")

    context = {'form': form}

    return render(request, 'signUp.html', context)


# Login User
def Login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("index")
            else:
                return render(request, 'login.html', {'error_message': 'Your account disable'})
        else:
            return render(request, 'login.html', {'error_message': 'Invalid Login'})

    return render(request, 'login.html')


# Logout user
def Logout(request):
    logout(request)
    return redirect("login")


def add_movies(request):
    
    genres = Genre.objects.all()
    if request.method == 'POST':
        title = request.POST['title']
        genre_id = request.POST['genre']
        description = request.POST['description']
        movie_logo = request.FILES['movie-logo']
        year = request.POST['year']
        
        user = request.user
        
        slug = slugify(title)
        genre = get_object_or_404(Genre, id=genre_id)
        movie = Movie(title=title, slug=slug, genre = genre,year=year, description=description, movie_logo=movie_logo,user=user )
        movie.save()
        return redirect('contribution')

    return render(request, 'add_movies.html', {'genres':genres})


def contribution(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if not request.user.is_active:
        raise Http404
    
    movies = Movie.objects.filter(user=request.user)
    
    # Pass the contributions to the template
    return render(request, 'contribution.html', {'movies': movies})


def updateMovie(request, movie_id):
    # Retrieve the movie object or return 404 if not found
    movie = get_object_or_404(Movie, id=movie_id)

    if request.method == 'POST':
        # Fill the form with data from the request and the movie instance
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            # Save the updated data
            form.save()
            # Redirect to a success page or another view
            return redirect('contribution')  # Assuming 'contribution' is the name of the view
    else:
        # Create a form instance with the movie's current data
        form = MovieForm(instance=movie)

    # Render the update template with the form
    return render(request, 'update.html', {'form': form})


def deleteMovie(request, movieId):
    if request.method == 'POST':
         movieID = Movie.objects.get(id=movieId)
         movieID.delete()
         return redirect('contribution')
    return render(request,'delete.html')


@login_required
def rate_movie(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    if request.method == 'POST':
        form2 = RatingForm(request.POST)
        if form2.is_valid():
            rating = form2.save(commit=False)
            rating.user = request.user
            rating.movie = movie
            rating.save()
            return redirect('detail', movie_id=movie_id)
    else:
        form2 = RatingForm()
    return render(request, 'detail.html', {'form2': form2, 'movie': movie})
