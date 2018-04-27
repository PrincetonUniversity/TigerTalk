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


class AutoDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        return datetime.datetime.now()

class Review(models.Model):
    FUN_CHOICES = (
        (1, 'Yes'),
        (0, 'No'),
    )
    text = models.TextField()
    fun = models.IntegerField(choices=FUN_CHOICES)
    meaningful = models.IntegerField(validators=[MaxValueValidator(1), MinValueValidator(0)])
    stars = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    CBI = models.CharField(max_length=200)
    rating = models.IntegerField(default='0')
    created_at = models.DateTimeField(default=timezone.now)

class Club(models.Model):
    name = models.CharField(max_length=200)
    desc = models.TextField()
    category = models.ManyToManyField(Category)
    email = models.EmailField(max_length=200)
    leaders = models.ManyToManyField(Leader)
    website = models.TextField()
    reviews = models.ManyToManyField(Review)
    fun_count = models.IntegerField(default = 0)
    meaning_count = models.IntegerField(default = 0)
    total_stars = models.FloatField(default = 0)

    def __str__(self):
        return self.name

    def display_cat(self):
        return ', '.join([ category.name for category in self.category.all()[:3] ])
    display_cat.short_description = 'Category'

    def display_leaders(self):
        return ', '.join([ leader.name for leader in self.leaders.all()[:3] ])
    display_leaders.short_description = 'Leaders'

