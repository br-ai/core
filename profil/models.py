from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from django_countries.fields import CountryField

# Create your models here.

class User(AbstractUser):

    genre = (
        ('Homme','Homme'),
        ('Femme','Femme'),
        )

    typ = (
        ('Prestataire','Prestataire'),
        ('Client','Client'),
        )


    profile_pic = models.ImageField(upload_to='profile_pic/', default='user_profile.jpeg', null = True)
    bio = models.TextField(max_length=160, blank=True, null=True)
    cover = models.ImageField(upload_to='covers/', blank=True)
    gender = models.CharField(default='Homme', choices=genre, max_length=10, null = True)
    cover =  models.ImageField(upload_to='user_cover/', default='cover.jpg', null = True)
    # countrie = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True)
    # citie = models.ForeignKey(City, on_delete=models.CASCADE, blank=True, null=True)
    phone_number = models.BigIntegerField(null = True, blank = True, unique = True)
    typ_user =  models.CharField(max_length=30, choices=typ, default='Client', blank=True, null=True)
    certifie = models.BooleanField(default = False)
    country = CountryField(null = True, blank_label='(select country)') 
    phone = models.CharField(max_length=20, null = True)
    devoile = models.CharField(max_length=50, null = True)

    def __str__(self):
        return self.username

    def serialize(self):
        return {
            'id': self.id,
            "username": self.username,
            "profile_pic": self.profile_pic.url,
            "first_name": self.first_name,
            "last_name": self.last_name
        }

class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    followers = models.ManyToManyField(User, blank=True, related_name='following')

    def __str__(self):
        return f"User: {self.user}"
        