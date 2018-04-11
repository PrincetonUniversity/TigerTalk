from django.contrib import admin

from .models import Club
from .models import Category
from .models import Leader


admin.site.register(Category)

from django.contrib import admin

# Define the admin class
class LeaderAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'email')
    #fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
admin.site.register(Leader, LeaderAdmin)

# Register the Admin classes for Book using the decorator

class ClubAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'desc', 'display_cat', 'display_leaders')

admin.site.register(Club, ClubAdmin)

  
