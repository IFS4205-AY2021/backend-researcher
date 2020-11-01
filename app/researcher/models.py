from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class User(models.Model):
    class TestResult(models.TextChoices):
        POSITIVE = True
        NEGATIVE = False
        UNKNOWN = None

    name = models.CharField(max_length=64)
    phone = models.CharField(max_length=12)
    age = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(120)])
    address = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=32)
    test_result = models.CharField(max_length=5, choices=TestResult.choices)
    encryption_keys = models.TextField(blank=True, null=True)


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