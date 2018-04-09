from django.shortcuts import render
from django.utils import timezone
from .models import Club
from .models import Category
from .models import Leader
from django.shortcuts import render, get_object_or_404

# Create your views here.
def post_list(request):
	clubs = Club.objects.all()
	return render(request, 'page/post_list.html', {'clubs': clubs})

def post_detail(request, pk):
	club = get_object_or_404(Club, pk=pk)
	return render(request, 'page/post_detail.html', {'club': club})

def post_list_full(request):
	clubs = Club.objects.all()
	return render(request, 'page/post_list_full.html', {'clubs': clubs})	
