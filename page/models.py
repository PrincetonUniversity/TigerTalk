from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Leader(models.Model):
    name = models.CharField(max_length=40)
    title = models.CharField(max_length=40)
    email = models.EmailField(max_length=40)
    club = models.ForeignKey('Club', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.name

class AutoDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        return datetime.datetime.now()

class Review(models.Model):
    text = models.TextField(max_length=2000)
    fun = models.IntegerField(validators=[MaxValueValidator(1), MinValueValidator(0)])
    meaningful = models.IntegerField(validators=[MaxValueValidator(1), MinValueValidator(0)])
    stars = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    CBI = models.CharField(max_length=200)
    rating = models.IntegerField(default='0')
    created_at = models.DateTimeField(default=timezone.now)
    student = models.ForeignKey('Student', on_delete=models.PROTECT, null=True)
    club = models.ForeignKey('Club', on_delete=models.PROTECT, null=True)

class Interview(models.Model):
    text = models.TextField(max_length=2000)
    positive = models.IntegerField(validators=[MaxValueValidator(1), MinValueValidator(0)])
    hard = models.IntegerField(validators=[MaxValueValidator(1), MinValueValidator(0)])
    rating = models.IntegerField(default='0')
    created_at = models.DateTimeField(default=timezone.now)
    student = models.ForeignKey('Student', on_delete=models.PROTECT, null=True)
    club = models.ForeignKey('Club', on_delete=models.PROTECT, null=True)

class Club(models.Model):
    name = models.CharField(max_length=80)
    desc = models.TextField(max_length=1600, null=True, blank=True)
    category = models.ManyToManyField(Category, blank=True)
    email = models.EmailField(max_length=30)
    website = models.CharField(max_length=400, null=True, blank=True)
    fun_count = models.IntegerField(default = 0)
    meaning_count = models.IntegerField(default = 0)
    positive_count = models.IntegerField(default = 0)
    hard_count = models.IntegerField(default = 0)
    total_stars = models.FloatField(default = 0)
    photo1 = models.ImageField(upload_to='gallery', null=True, blank=True)
    photo2 = models.ImageField(upload_to='gallery', null=True, blank=True)
    photo3 = models.ImageField(upload_to='gallery', null=True, blank=True)


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
    clubs_reviewed = models.ManyToManyField(Club, related_name="submissions", blank=True)
    club_interviews_reviewed = models.ManyToManyField(Club, related_name="interviews", blank=True)
    review_upvotes = models.ManyToManyField(Review, related_name="upvotes", blank=True)
    review_downvotes = models.ManyToManyField(Review, related_name="downvotes", blank=True)
    clubs_liked = models.ManyToManyField(Club, related_name="likes", blank=True)
    clubs_interested = models.ManyToManyField(Club, related_name="interested", blank=True)

    def __str__(self):
        return self.netid