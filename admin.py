from django.contrib import admin

# Register your models here.
from .models import Author, Genre, Book, BookInstance, Category, Leader, Club

#admin.site.register(Book)
#admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Category)
#admin.site.register(BookInstance)

# Define the admin class
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)

# Define the admin class
class LeaderAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'email')
    #fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

# Register the admin class with the associated model
admin.site.register(Leader, LeaderAdmin)


class BooksInstanceInline(admin.TabularInline):
    model = BookInstance


# Register the Admin classes for Book using the decorator

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]

@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'desc', 'display_cat', 'display_leaders')

# Register the Admin classes for BookInstance using the decorator

@admin.register(BookInstance) 
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back')
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )