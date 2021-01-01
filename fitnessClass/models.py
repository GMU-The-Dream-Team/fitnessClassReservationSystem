from django.db import models
from accounts.models import Customer
from django.db.models.fields.related import ForeignKey

# Create your models here.
class FitnessClass(models.Model):
    className = models.CharField(max_length=100)
    instructorName = models.CharField(max_length=100)
    dayOfWeekChoices = [
        ('Sunday', 'Sunday'),
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday')
    ]
    timeOfDay = [
        ('5:00 am', '5:00 am'),
        ('5:15 am', '5:15 am'),
        ('5:30 am', '5:30 am'),
        ('5:45 am', '5:45 am'),
        ('6:00 am', '6:00 am'),
        ('6:15 am', '6:15 am'),
        ('6:30 am', '6:30 am'),
        ('6:45 am', '6:45 am'),
        ('7:00 am', '7:00 am'),
        ('7:15 am', '7:15 am'),
        ('7:30 am', '7:30 am'),
        ('7:45 am', '7:45 am'),
        ('8:00 am', '8:00 am'),
        ('8:15 am', '8:15 am'),
        ('8:30 am', '8:30 am'),
        ('8:45 am', '8:45 am'),
        ('9:00 am', '9:00 am'),
        ('9:15 am', '9:15 am'),
        ('9:30 am', '9:30 am'),
        ('9:45 am', '9:45 am'),
        ('10:00 am', '10:00 am'),
        ('10:15 am', '10:15 am'),
        ('10:30 am', '10:30 am'),
        ('10:45 am', '10:45 am'),
        ('11:00 am', '11:00 am'),
        ('11:15 am', '11:15 am'),
        ('11:30 am', '11:30 am'),
        ('11:45 am', '11:45 am'),
        ('12:00 pm', '12:00 pm'),
        ('12:15 pm', '12:15 pm'),
        ('12:30 pm', '12:30 pm'),
        ('12:45 pm', '12:45 pm'),
        ('1:00 pm', '1:00 pm'),
        ('1:15 pm', '1:15 pm'),
        ('1:30 pm', '1:30 pm'),
        ('1:45 pm', '1:45 pm'),
        ('2:00 pm', '2:00 pm'),
        ('2:15 pm', '2:15 pm'),
        ('2:30 pm', '2:30 pm'),
        ('2:45 pm', '2:45 pm'),
        ('3:00 pm', '3:00 pm'),
        ('3:15 pm', '3:15 pm'),
        ('3:30 pm', '3:30 pm'),
        ('3:45 pm', '3:45 pm'),
        ('4:00 pm', '4:00 pm'),
        ('4:15 pm', '4:15 pm'),
        ('4:30 pm', '4:30 pm'),
        ('4:45 pm', '4:45 pm'),
        ('5:00 pm', '5:00 pm'),
        ('5:15 pm', '5:15 pm'),
        ('5:30 pm', '5:30 pm'),
        ('5:45 pm', '5:45 pm'),
        ('6:00 pm', '6:00 pm'),
        ('6:15 pm', '6:15 pm'),
        ('6:30 pm', '6:30 pm'),
        ('6:45 pm', '6:45 pm'),
        ('7:00 pm', '7:00 pm'),
        ('7:15 pm', '7:15 pm'),
        ('7:30 pm', '7:30 pm'),
        ('7:45 pm', '7:45 pm'),
    ]
    dayOfWeek = models.CharField(max_length=20, choices=dayOfWeekChoices, default=None)
    startTime = models.CharField(max_length=20,  choices=timeOfDay, default=None)
    endTime = models.CharField(max_length=20,  choices=timeOfDay, default=None)
    maximumCapacity = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.className} with {self.instructorName} \n {self.dayOfWeek} \n @  {self.startTime} - {self.endTime}'