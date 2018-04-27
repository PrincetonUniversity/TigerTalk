from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Club, Category, Leader, Review, Student
from .forms import PostForm, LoginForm
from .decorators import CAS_login_required
from django.db import models
from django.db.models import Count
from django.http import HttpResponse
from . import CASClient
from django.contrib import auth
from django.contrib.auth.models import User

time = 1

def post_list(request):
    clubs = Club.objects.all()
    return render(request, 'page/index.html', {'clubs': clubs})

@CAS_login_required
def post_detail(request, pk):
    global time
    club = get_object_or_404(Club, pk=pk)
    reviews = club.review_set.all()
    review_count = reviews.count()
    star_result = 0
    if (review_count != 0):
        star_result = club.total_stars;

    if (review_count):
        if ((club.fun_count / review_count) >= .5):
            happy_result = 1
        elif ((club.fun_count / review_count) < .5):
            happy_result = 0
    else:
        happy_result = 0

    if (review_count):
        if ((club.meaning_count / review_count) >= .5):
            mean_result = 1
        elif ((club.meaning_count / review_count) < .5):
            mean_result = 0
    else:
        mean_result = 0

    reviews.time = reviews.order_by('-created_at')
    reviews.rating = reviews.order_by('-rating')

    if 'sort' in request.GET:
        sort = request.GET['sort']
        if sort == "1":
            time = 1
            return render(request, 'page/post_detail2.html', {'club': club, 'review_count': review_count, 'fun_count': club.fun_count, 'happy_result': happy_result, 'mean_result': mean_result, 'star_count': star_result, 'reviews' : reviews.time, 'time' : time})

        elif sort == "2":
            time = 2
            return render(request, 'page/post_detail2.html', {'club': club, 'review_count': review_count, 'fun_count': club.fun_count, 'mean_count': club.meaning_count, 'happy_result': happy_result, 'mean_result': mean_result, 'star_count': star_result, 'reviews' : reviews.rating, 'time' : time})

    else:
        return render(request, 'page/post_detail2.html', {'club': club, 'review_count': review_count, 'fun_count': club.fun_count, 'mean_count': club.meaning_count, 'happy_result': happy_result, 'mean_result': mean_result, 'star_count': star_result, 'reviews' : reviews.time, 'time' : time})

@CAS_login_required
def top20(request):
    clubs = Club.objects.all()
    clubs = clubs.order_by('-total_stars', 'name')[:20]
    return render(request, 'page/top20.html', {'clubs': clubs})

@CAS_login_required
def all_reviews(request, pk):
    global time;
    club = get_object_or_404(Club, pk=pk)

    reviews = club.review_set.all()
    review_count = reviews.count()

    if (review_count):
        if ((club.fun_count / review_count) >= .5):
            happy_result = 1
        elif ((club.fun_count / review_count) < .5):
            happy_result = 0
    else:
        happy_result = 0

    if (review_count):
        if ((club.meaning_count / review_count) >= .5):
            mean_result = 1
        elif ((club.meaning_count / review_count) < .5):
            mean_result = 0
    else:
        mean_result = 0

    reviews.time = reviews.order_by('-created_at')
    reviews.rating = reviews.order_by('-rating')

    if 'sort' in request.GET:
        sort = request.GET['sort']
        if sort == "1":
            time = 1
            return render(request, 'page/all_reviews.html', {'club': club, 'fun_count': club.fun_count, 
                'happy_result': happy_result, 'mean_result': mean_result, 
                'reviews' : reviews.time, 'time' : time})

        elif sort == "2":
            time = 2
            return render(request, 'page/all_reviews.html', {'club': club, 'review_count': review_count, 
                'fun_count': club.fun_count, 'mean_count': club.meaning_count, 'happy_result': happy_result, 
                'mean_result': mean_result, 'reviews' : reviews.rating, 
                'time' : time})

    else:
        return render(request, 'page/all_reviews.html', {'club': club, 'review_count': review_count, 'fun_count': club.fun_count, 'mean_count': club.meaning_count, 'happy_result': happy_result, 'mean_result': mean_result, 'reviews' : reviews.time, 'time' : time})
    return render(request, 'page/all_reviews.html', {'club': club, 'reviews': reviews})

@CAS_login_required
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

@CAS_login_required
def post_new(request, pk):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            club = get_object_or_404(Club, pk=pk)
            review = form.save(commit=False)
            review.student = request.user.student
            review.club = club
            club.fun_count += review.fun
            club.meaning_count += review.meaningful
            review_count = club.review_set.count()
            if review_count != 0:
                club.total_stars = club.total_stars * review_count
                club.total_stars += review.stars
                club.total_stars = club.total_stars / (review_count+1)
            else: 
                club.total_stars = review.stars
            review.save()
            club.save()
            return redirect('post_detail', pk=pk)
    else:
        form = PostForm()
    return render(request, 'page/post_edit.html', {'form': form, 'user': request.user})  

def search_form(request):
    return render(request, 'page/search_form.html')

@CAS_login_required
def review_detail(request, pk):
    review = get_object_or_404(Review, pk=pk)
    return render(request, 'page/review_detail.html', {'review': review})

@CAS_login_required
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

def logintemp(request):
    C = CASClient.CASClient(request)
    auth_attempt = C.Authenticate()
    if "netid" in auth_attempt:
        netid = auth_attempt["netid"]
        request.session["netid"] = netid
        username = netid
        password = netid
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            # User has already logged in before
            auth.login(request, user)
            return redirect('/') 
        else:
            # first time loggin in - create a user
            user = User.objects.create_user(username=username, password=password)
            email = netid + "@princeton.edu"
            is_club = False
            if Club.objects.filter(email=email):
                is_club = True
            student = Student(user=user, netid=netid, is_club=is_club)
            student.save()
            auth.login(request, user)
            return redirect('/')
    elif "location" in auth_attempt:
        return redirect(auth_attempt["location"])
    else:
        abort(500)

def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            netid = form.cleaned_data['username']
            username = netid
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                # User has already logged in before
                auth.login(request, user)
                return redirect('post_list_full') 
            else:
                # first time loggin in - create a user
                user = User.objects.create_user(username=username, password=password)
                email = netid + "@princeton.edu"
                is_club = False
                if Club.objects.filter(email=email):
                    is_club = True
                student = Student(user=user, netid=netid, is_club=is_club)
                student.save()
                auth.login(request, user)
                return redirect('post_list_full')
    else:
        form = LoginForm()
    return render(request, 'page/logintemp.html', {'form': form}) 