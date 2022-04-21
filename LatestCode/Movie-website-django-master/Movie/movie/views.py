
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponsePermanentRedirect
import django.views.decorators.csrf
import json
from movie.models import *
from django.http import HttpResponse
import math


def detail(request, model, id):
    items = []
    try:
        if model.get_name() == 'movie' and id != 'None':
            label = 'actor'
            object = model.objects.get(movieid=id)
            records = Act.objects.filter(movieid_id=id)
            for query in records:
                for actor in Actor.objects.filter(actorid=query.actorid_id):
                    items.append(actor)
        if model.get_name() == 'actor':
            label = 'movie'
            # Get the Actor
            object = model.objects.get(actorid=id)
            # Get Movie Id's in which Actor is Present
            records = Act.objects.filter(actorid_id=id)
            for query in records:
                for movie in Movie.objects.filter(movieid=query.movieid_id):
                    items.append(movie)
    except:
        return render(request, '404.html')
    return render(request, '{}_list.html'.format(label), {'items': items, 'number': len(items), 'object': object})


def whole_list(request, page):
    actors = Actor.objects.all()
    pages = int(math.ceil(len(actors) / 20))
    page = int(page)
    # find the last index of actor to be displayed on a page
    lastIndex = 0
    if page < pages:
        lastIndex = page * 20
    else:
        lastIndex = len(actors)

    # finding the list of pages to be displayed at bottom at a time
    distance = pages - page
    start_page_num = 1

    if distance >= 5:# if these are initial pages
        start_page_num = page - 5
    elif distance < 5: # if its thelast pages
        start_page_num = page - 10 + distance

    end_page_num = 10
    if page > 5:
        end_page_num = page + 5

    displayPages = []
    for i in range(start_page_num, end_page_num + 1):
        if 1 <= i <= pages:
            displayPages.append(i)

    data = {'items': actors[20 * (page - 1):lastIndex], 'current_page': page, 'page_number': pages, 'pages': displayPages}
    return render(request, 'Allactors.html', data)

def add_seen(request, movie_id):
    if not request.is_secure():
        history = Seen.objects.filter(movieid_id=movie_id, username=request.user.get_username())
        if len(history) == 0:
            weight=0
            try:
                movie = Popularity.objects.get(movieid_id=movie_id)
                weight = movie.weight
                movie.delete()
            except:
                movie=None

            new_record = Popularity(movieid_id=movie_id, weight=weight + 3)
            new_record.save()
            new_record = Seen(movieid_id=movie_id, username=request.user.get_username())
            new_record.save()
            return HttpResponse('1')
        else:
            history.delete()
            return HttpResponse('0')


@django.views.decorators.csrf.csrf_protect
def seen(request):
    records = Seen.objects.filter(username=request.user.get_username())
    movies = []
    for record in records:
        movie_id = str(record).split('|')[1]
        movies.append(Movie.objects.get(movieid=movie_id))
    return render(request, 'seen.html', {'items': movies, 'number': len(movies)})

#Order
def add_order(request, movie_id):
    if not request.is_secure():
        history = Order.objects.filter(movieid_id=movie_id, username=request.user.get_username())
        if len(history) == 0:
            weight = 0
            try:
                movie = Popularity.objects.get(movieid_id=movie_id)
                weight = movie.weight
                movie.delete()
            except:
                movie=None
            new_record = Popularity(movieid_id=movie_id, weight=weight + 3)
            new_record.save()
            new_record = Order(movieid_id=movie_id, username=request.user.get_username())
            new_record.save()
            return HttpResponse('1')
        else:
            history.delete()
            return HttpResponse('0')


@django.views.decorators.csrf.csrf_protect
def order(request):
    records = Order.objects.filter(username=request.user.get_username())
    price=0

    movies = []
    for record in records:
        movie_id = str(record).split('|')[1]
        rc= Movie.objects.get(movieid=movie_id)
        price= rc.price+price
        movies.append(Movie.objects.get(movieid=movie_id))
    return render(request, 'order.html', {'items': movies, 'number': len(movies), 'totalamount': price})

@django.views.decorators.csrf.csrf_protect
def delete_order(request, movie_id):

    Order.objects.filter(movieid_id=movie_id, username=request.user.get_username()).delete()
    # Order.objects.filter(movieid_id=movie_id, username=request.user.get_username())
    return HttpResponsePermanentRedirect(reverse('order'))

def searchbar(request):
    if request.method != "POST":
        return render(request, '404.html')
    else:
        searched = request.POST['searched']
        print(searched)
        all_movies = Movie.objects.filter(title__contains=searched)
        print(all_movies)
        if len(all_movies) > 0:
            return render(request, 'searchbar.html', {'data': all_movies})
        else:
            return render(request, '404.html')


