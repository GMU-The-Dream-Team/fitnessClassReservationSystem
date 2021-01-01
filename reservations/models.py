from django.db import models
from fitnessClass.models import FitnessClass
from accounts.models import Customer

# Create your models here.
class Reservation(models.Model):
    classReserved = models.ForeignKey(FitnessClass, default=None, on_delete=models.CASCADE)
    customerReserving = models.ForeignKey(Customer, default=None, on_delete=models.CASCADE)
    classDate = models.DateField(default=None)
    reservationStatus = models.CharField(max_length=20, default=None)
    reservationDate = models.DateField(auto_now=True)
    reservationTime = models.TimeField(auto_now=True)

    def __str__(self):
        return f'{self.classReserved} reserved by {self.customerReserving}'