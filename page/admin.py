from django.contrib import admin

from .models import Club
from .models import Category
from .models import Leader
from .models import Review

admin.site.register(Category)

from django.contrib import admin

# Define the admin class
class LeaderAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'email')
admin.site.register(Leader, LeaderAdmin)

class ClubAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'desc', 'display_cat', 'display_leaders')
admin.site.register(Club, ClubAdmin)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('text',)
admin.site.register(Review, ReviewAdmin)