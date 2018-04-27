from django.contrib import admin

from .models import Club
from .models import Category
from .models import Leader
from .models import Review
from .models import Student

admin.site.register(Category)

class LeaderAdmin(admin.ModelAdmin):
    def club(self, obj):
        return obj.club.name
    list_display = ('name', 'title', 'email', 'club')
admin.site.register(Leader, LeaderAdmin)

class ClubAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'desc', 'display_cat', 'display_leaders')
admin.site.register(Club, ClubAdmin)

class ReviewAdmin(admin.ModelAdmin):
    def author(self, obj):
        return obj.student.netid
    def club(self, obj):
        return obj.club.name
    list_display = ('text', 'author', 'club')
admin.site.register(Review, ReviewAdmin)

class StudentAdmin(admin.ModelAdmin):
    list_display = ('netid', 'is_club')
admin.site.register(Student, StudentAdmin)