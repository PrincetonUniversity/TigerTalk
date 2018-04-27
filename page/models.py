from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Leader(models.Model):
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    email = models.EmailField(max_length=100)
    club = models.ForeignKey('Club', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.name

class AutoDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        return datetime.datetime.now()

class Review(models.Model):
    text = models.TextField()
    fun = models.IntegerField(validators=[MaxValueValidator(1), MinValueValidator(0)])
    meaningful = models.IntegerField(validators=[MaxValueValidator(1), MinValueValidator(0)])
    stars = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    CBI = models.CharField(max_length=200)
    rating = models.IntegerField(default='0')
    created_at = models.DateTimeField(default=timezone.now)
    student = models.ForeignKey('Student', on_delete=models.PROTECT, null=True)
    club = models.ForeignKey('Club', on_delete=models.PROTECT, null=True)

class Club(models.Model):
    name = models.CharField(max_length=200)
    desc = models.TextField()
    category = models.ManyToManyField(Category)
    email = models.EmailField(max_length=200)
    website = models.TextField()
    fun_count = models.IntegerField(default = 0)
    meaning_count = models.IntegerField(default = 0)
    total_stars = models.FloatField(default = 0)


    def __str__(self):
        return self.name

    def display_cat(self):
        return ', '.join([ category.name for category in self.category.all()[:3] ])
    display_cat.short_description = 'Category'

    def display_leaders(self):
        return ', '.join([ leader.name for leader in self.leader_set.all()[:3] ])
    display_leaders.short_description = 'Leaders'

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student")
    netid = models.CharField(max_length=50)
    clubs_reviewed = models.ManyToManyField(Club, related_name="submissions")
    club_interviews_reviewed = models.ManyToManyField(Club, related_name="interviews")
    review_votes = models.ManyToManyField(Review, related_name="votes")
    is_club = models.BooleanField(default=False)
    clubs_liked = models.ManyToManyField(Club, related_name="likes")

    def __str__(self):
        return self.netid