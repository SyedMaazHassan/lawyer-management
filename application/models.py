from django.db import models
from datetime import datetime
from django.contrib.auth.models import User, auth
# Create your models here.

# python manage.py makemigrations
# python manage.py migrate
# python manage.py runserver

class lawyer_plan(models.Model):
    price = models.FloatField()
    sublowers_allowed = models.IntegerField()

    def __str__(self):
        return f'${self.price} - {self.sublowers_allowed} people'


class lawyer(models.Model):
    """

    Model for lawyer registration

    """
    first_name =  models.CharField(max_length=255)
    last_name =  models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone_number =  models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    lisence_number = models.CharField(max_length=90) #ask for limit
    bar_number = models.CharField(max_length=90)
    selected_plan = models.ForeignKey(lawyer_plan, on_delete = models.CASCADE)
    is_approved = models.BooleanField(default = False) #True #False
    is_rejected = models.BooleanField(default = False) #False #True
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class client(models.Model):
    first_name =  models.CharField(max_length=255)
    last_name =  models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone_number =  models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null = True)