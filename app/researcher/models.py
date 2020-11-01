from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
from django.contrib.auth.models import User
from datetime import datetime, date

# Create your models here.
class UserInfo(models.Model):
    class TestResult(models.TextChoices):
        POSITIVE=True
        NEGATIVE=False
        UNKNOWN=None
    class genders(models.TextChoices):
        MALE='M'
        FEMALE='F'
        UNKNOWN='NA'
    # relate          = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name            = models.CharField(max_length=64)
    phone           = models.CharField(max_length=12)
    age             = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(120)])
    gender          = models.CharField(max_length=2, choices=genders.choices, default=genders.UNKNOWN)
    location        = models.CharField(max_length=6, validators=[MinLengthValidator(6)])
    address         = models.CharField(max_length=16)
    test_result     = models.CharField(max_length=5, choices=TestResult.choices, default=TestResult.UNKNOWN)
    encryption_keys = models.TextField(blank=True, null=True)
    cluster_id      = models.IntegerField(default=0)
    def __str__(self):
        return str(self.id) + self.name

class K_User(models.Model):
    class TestResult(models.TextChoices):
        POSITIVE = True
        NEGATIVE = False
        UNKNOWN = None

    class genders(models.TextChoices):
        MALE='M'
        FEMALE='F'
        UNKNOWN='NA'
    cluster_id = models.CharField(max_length=128)
    age = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(120)])
    age_min = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(120)])
    age_max = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(120)])
    gender = models.CharField(max_length=1)
    location = models.CharField(max_length=32)
    test_result = models.CharField(max_length=5, choices=TestResult.choices)

class StayHomeRecord(models.Model):
    name = models.CharField(max_length=64)
    phone = models.CharField(max_length=12)
    address = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=32)
    images = models.CharField(max_length=32)  # TOBE updated
    videos = models.CharField(max_length=32)  # TOBE updated
    documents = models.CharField(max_length=32)  # TOBE updated


class Admin(models.Model):
    name = models.CharField(max_length=64)
    phone = models.CharField(max_length=12)
    encryption_keys = models.TextField(blank=True, null=True)


class Location(models.Model):
    postcode = models.CharField(max_length=6)
    name = models.CharField(max_length=64)


class Researcher(models.Model):
    name = models.CharField(max_length=64)
    phone = models.CharField(max_length=12)
    encryption_keys = models.TextField(blank=True, null=True)


class Tracer(models.Model):
    name = models.CharField(max_length=64)
    phone = models.CharField(max_length=12)
    encryption_keys = models.TextField(blank=True, null=True)


class Contact(models.Model):
    location = models.CharField(max_length=32)
    person1_id = models.CharField(max_length=128)
    person2_id = models.CharField(max_length=128)