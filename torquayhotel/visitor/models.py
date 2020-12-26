from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.URLField(max_length=200)
    nickname = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user}"    
    

class Room(models.Model):
    ROOM_CATEGORIES=(
        ('ST', 'STANDARD'),
        ('DEL', 'DELUXE'),
        ('SUI', 'SUITE'),
    )
    number = models.IntegerField(null=True)
    category = models.CharField(max_length=3, choices=ROOM_CATEGORIES)
    beds = models.IntegerField()
    capacity = models.IntegerField()
    seeview = models.BooleanField(default=True)
    balcony = models.BooleanField(default=True)
    roomservice = models.BooleanField(default=True)
    breakfast = models.BooleanField(default=True)
    lunch = models.BooleanField(default=True)
    dinner = models.BooleanField(default=True)
    
    def __str__(self):
        return f"N°{self.number}, {self.category} with {self.beds} bed(s) for {self.capacity} people(s)"    
    

class Reservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
    check_in = models.DateField()
    check_out = models.DateField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    # profile = models.ForeignKey('Profile', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} has booked {self.room} from {self.check_in} to {self.check_out}"    
    


class Avaibility(models.Model):
    room = models.ManyToManyField(Room) 


class Request(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=150)
    message = models.CharField(max_length=500)
