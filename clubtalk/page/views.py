from django.shortcuts import render
from django.utils import timezone
from .models import Club
from .models import Category
from .models import Leader
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

# Create your views here.
def post_list(request):
	return render(request, 'page/post_list.html')

def post_detail(request, pk):
	club = get_object_or_404(Club, pk=pk)
	return render(request, 'page/post_detail.html', {'club': club})

def post_list_full(request):
	clubs = Club.objects.all()
	return render(request, 'page/post_list_full.html', {'clubs': clubs})	

def search_form(request):
    return render(request, 'page/search_form.html')

def search(request):
    error = False
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            error = True
        else:
            clubs = Club.objects.filter(name__icontains=q)
            return render(request, 'page/search_results.html', {'clubs': clubs, 'query': q})
    return render(request, 'page/search_form.html', {'error': error})