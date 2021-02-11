from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    email = models.EmailField(max_length=50)
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)
    street = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=20)
    zipcode = models.CharField(max_length=20)
    phoneNumber = models.CharField(max_length=20)
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    verificationChoices = [
        ('Annual', 'Annual Pass Holder'),
        ('Resident', 'Town of Leesburg Resident'),
        ('Neither', 'Neither'),
        ('UnVerified', 'UnVerified')
    ]
    verified = models.CharField(max_length=20, choices=verificationChoices)

    def __str__ (self):
        return f'{self.firstName} {self.lastName}'