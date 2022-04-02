import operator
import random

from django.shortcuts import render
from movie.models import *


def index(request):
    data = {}
    movie_dict = {}
    for movie in Movie.objects.all():
        movie_dict[movie.movieid] = movie
    popular_movies = Popularity.objects.all().order_by('-weight')
    popular = []
    for movie in popular_movies[:6]:
        try:
            # if is_url_image(movie_dict[movie.movieid_id].poster):
            popular.append({'movieid': movie.movieid_id, 'poster': movie_dict[movie.movieid_id].poster})
        except:
            continue
    data['popular'] = popular
    popular_movie_list = []
    for movie in popular_movies[:6]:
        popular_movie_list.append(movie_dict[movie.movieid_id])
    data['recommendation'] = get_recommendation(request, popular_movie_list)
    return render(request, 'base.html', data)


def get_recommendation(request, popular_movie_list):
    result = []
    already_added =[]
    movie_dict = {}
    movie_ratings = {}
    for movie in Movie.objects.all():
        movie_dict[movie.movieid] = movie
        movie_ratings[movie.movieid] = movie.rate;
    # sorting the movies according to ratings ;
    sortedList=sorted(movie_ratings.items(), key=operator.itemgetter(1), reverse=True)
    #sorted list is a list of tuples
    #sorted fuction has returned the (movie_id, rating) in descending order
    for item in sortedList:
        movie = movie_dict[item[0]]
        if movie not in popular_movie_list:
            # if is_url_image(movie.poster):
            result.append({'movieid': movie.movieid, 'poster': movie.poster})
        if len(result) == 10:
            break
    final_result = random.sample(result, 6)
    return final_result;

# def is_url_image(image_url):
#     try:
#         page = requests.get(image_url)
#
#     except Exception as e:
#         print("error:", e)
#         return False
#
#         # check status code
#     if (page.status_code != 200):
#         return False
#
#     return True









