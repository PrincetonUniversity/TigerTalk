from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=200)

    def display_cat(self):
        return ', '.join([ category.name for category in self.category.all()[:3] ])
    
    display_cat.short_description = 'Category'

class Leader(models.Model):
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    email = models.EmailField(max_length=100)

    def display_leaders(self):
        return ', '.join([ leader.name for leader in self.leaders.all()[:3] ])
    
    display_leaders.short_description = 'Leaders'

class Club(models.Model):
    name = models.CharField(max_length=200)
    desc = models.TextField()
    category = models.ManyToManyField(Category)
    email = models.EmailField(max_length=200)
    leaders = models.ManyToManyField(Leader)
    website = models.TextField()




#class Post(models.Model):
#    title = models.CharField(max_length=200)
#    genre = models.CharField(max_length=200)
#    president = models.CharField(max_length=50)
#    text = models.TextField()
#    created_date = models.DateTimeField(
#            default=timezone.now)
#    published_date = models.DateTimeField(
#            blank=True, null=True)
#
#    def publish(self):
#        self.published_date = timezone.now()
#        self.save()
#
#    def __str__(self):
#        return self.title

