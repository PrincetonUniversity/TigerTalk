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

# Create your views here.
def post_list(request):
    clubs = Club.objects.all()
    return render(request, 'page/index.html', {'clubs': clubs})

def post_detail(request, pk):
    club = get_object_or_404(Club, pk=pk)
    review_count = club.reviews.count()
    fun_count = 0;
    mean_count = 0;
    star_count = 0;
    for r in club.reviews.all():
        fun_count += r.fun;
        mean_count += r.meaningful;
        star_count += r.stars;

    if (review_count != 0):
        star_count = star_count / review_count;
    return render(request, 'page/post_detail.html', {'club': club, 'review_count': review_count, 'fun_count': fun_count, 'mean_count': mean_count, 'star_count': star_count})

def post_list_full(request):
	clubs = Club.objects.all()
	return render(request, 'page/post_list_full.html', {'clubs': clubs})

def post_new(request, pk):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.save()
            club = get_object_or_404(Club, pk=pk)
            club.reviews.add(review)
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
    error = False
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            error = True
        else:
            clubs = Club.objects.filter(name__icontains=q) | Club.objects.filter(desc__icontains=q)
            return render(request, 'page/search_results.html', {'clubs': clubs, 'query': q})
    return render(request, 'page/search_form.html', {'error': error})

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