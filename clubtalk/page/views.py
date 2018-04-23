from django.shortcuts import render
from django.utils import timezone
from .models import Club
from .models import Category
from .models import Leader
from .models import Review
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect
from django.db import models
from django.http import HttpResponse
from django.db.models import Count
from . import CASClient

time = 1

# Create your views here.
def post_list(request):
    clubs = Club.objects.all()
    return render(request, 'page/index.html', {'clubs': clubs})

def post_detail(request, pk):
    global time
    club = get_object_or_404(Club, pk=pk)
    review_count = club.reviews.count()
    star_result = 0
    if (review_count != 0):
        star_result = club.total_stars / review_count
    total_happy = 0
    happy_result = 0
    for review in club.reviews.all():
        total_happy += review.fun
    if (review_count):
        if ((total_happy / review_count) >= .5):
            happy_result = 1
        elif ((total_happy / review_count) < .5):
            happy_result = 0
    else:
        happy_result = 0

    reviews = club.reviews.all()
    reviews.time = reviews.order_by('-created_at')
    reviews.rating = reviews.order_by('-rating')

    if 'sort' in request.GET:
        sort = request.GET['sort']
        if sort == "1":
            time = 1
            return render(request, 'page/post_detail2.html', {'club': club, 'review_count': review_count, 'fun_count': club.fun_count, 'mean_count': club.meaning_count, 'happy_result': happy_result, 'star_count': star_result, 'reviews' : reviews.time, 'time' : time})

        elif sort == "2":
            time = 2
            return render(request, 'page/post_detail2.html', {'club': club, 'review_count': review_count, 'fun_count': club.fun_count, 'mean_count': club.meaning_count, 'happy_result': happy_result, 'star_count': star_result, 'reviews' : reviews.rating, 'time' : time})

    else:
        return render(request, 'page/post_detail2.html', {'club': club, 'review_count': review_count, 'fun_count': club.fun_count, 'mean_count': club.meaning_count, 'happy_result': happy_result, 'star_count': star_result, 'reviews' : reviews.time, 'time' : time})


def post_list_full(request):
	clubs = Club.objects.all()
	return render(request, 'page/post_list_full.html', {'clubs': clubs})

def review_increment(request, pk_Club, pk_Review):
    review = get_object_or_404(Review, pk=pk_Review)
    review.rating += 1;
    review.save()
    return post_detail(request, pk_Club)

def review_decrement(request, pk_Club, pk_Review):
    review = get_object_or_404(Review, pk=pk_Review)
    review.rating -= 1;
    review.save()
    return post_detail(request, pk_Club)

def post_new(request, pk):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.save()
            club = get_object_or_404(Club, pk=pk)
            club.reviews.add(review)
            club.fun_count += review.fun
            club.meaning_count += review.meaningful
            club.total_stars += review.stars
            club.save()
            return redirect('post_detail', pk=pk)
    else:
        form = PostForm()
    return render(request, 'page/post_edit.html', {'form': form})   

def search_form(request):
    return render(request, 'page/search_form.html')

def review_detail(request, pk):
    review = get_object_or_404(Review, pk=pk)
    return render(request, 'page/review_detail.html', {'review': review})

def search(request):
    if 'q' in request.GET:
        q = request.GET['q']
        type = request.GET['type']

        if type == "%":
            if not q:
                clubs = Club.objects.all()
                return render(request, 'page/search_results.html', {'clubs': clubs})
            else:
                q2 = q.split(' ')
                clubs = Club.objects.filter(name__icontains=q2[0]) | Club.objects.filter(desc__icontains=q2[0])
                for i in range(1, len(q2)):
                    clubs = clubs.filter(name__icontains=q2[i]) | clubs.filter(desc__icontains=q2[i])
                return render(request, 'page/search_results.html', {'clubs': clubs, 'query': q})
        else:
            clubs = Club.objects.filter(category__id=type)
            if not q:
                return render(request, 'page/search_results.html', {'clubs': clubs})
            else:
                q2 = q.split(' ')
                clubs = clubs.filter(name__icontains=q2[0]) | clubs.filter(desc__icontains=q2[0])
                for i in range(1, len(q2)):
                    clubs = clubs.filter(name__icontains=q2[i]) | clubs.filter(desc__icontains=q2[i])
                return render(request, 'page/search_results.html', {'clubs': clubs, 'query': q}) 

def login(request):
    C = CASClient.CASClient(request)
    auth_attempt = C.Authenticate()
    if "netid" in auth_attempt:
        request.session["netid"] = auth_attempt["netid"]
        return redirect('/clublist')  
    elif "location" in auth_attempt:
        return redirect(auth_attempt["location"])
    else:
        abort(500)