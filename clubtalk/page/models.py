from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator


class Category(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Leader(models.Model):
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    email = models.EmailField(max_length=100)

    def __str__(self):
        return self.name

class Review(models.Model):
    text = models.TextField()
    fun = models.IntegerField(validators=[MaxValueValidator(1), MinValueValidator(0)])
    meaningful = models.IntegerField(validators=[MaxValueValidator(1), MinValueValidator(0)])
    stars = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    CBI = models.CharField(max_length=200)
    rating = models.IntegerField(default='0')

class Club(models.Model):
    name = models.CharField(max_length=200)
    desc = models.TextField()
    category = models.ManyToManyField(Category)
    email = models.EmailField(max_length=200)
    leaders = models.ManyToManyField(Leader)
    website = models.TextField()
    reviews = models.ManyToManyField(Review)

    def __str__(self):
        return self.name

    def display_cat(self):
        return ', '.join([ category.name for category in self.category.all()[:3] ])
    display_cat.short_description = 'Category'

    def display_leaders(self):
        return ', '.join([ leader.name for leader in self.leaders.all()[:3] ])
    display_leaders.short_description = 'Leaders'

