import datetime
from accounts.models import Customer
from django.shortcuts import render
from . models import FitnessClass

from datetime import date, timedelta

# Create your views here.
def schedule_view(request):

    sundayList = FitnessClass.objects.all().filter(dayOfWeek = 'Sunday').order_by('startTime')
    mondayList = FitnessClass.objects.all().filter(dayOfWeek = 'Monday').order_by('startTime')
    tuesdayList = FitnessClass.objects.all().filter(dayOfWeek = 'Tuesday').order_by('startTime')
    wednesdayList = FitnessClass.objects.all().filter(dayOfWeek = 'Wednesday').order_by('startTime')
    thursdayList = FitnessClass.objects.all().filter(dayOfWeek = 'Thursday').order_by('startTime')
    fridayList = FitnessClass.objects.all().filter(dayOfWeek = 'Friday').order_by('startTime')
    saturdayList = FitnessClass.objects.all().filter(dayOfWeek = 'Saturday').order_by('startTime')

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dayOrder = []
    datesList = {}
    availableDays = {}

    dayOrder.append(date.today().weekday())
    y = date.today().weekday()
    key = '' + days[y]
    datesList[key] = (datetime.date.today().strftime('%m-%d-%Y'))
    availableDays[key] = f'{key}'

    dayOrder.append((date.today() + timedelta(1)).weekday())
    y = (date.today() + timedelta(1)).weekday()
    key = '' + days[y]    
    datesList[key] = ((date.today() + timedelta(1)).strftime('%m-%d-%Y'))
    availableDays[key] = f'{key}'

    dayOrder.append((date.today() + timedelta(2)).weekday())
    y = (date.today() + timedelta(2)).weekday()
    key = '' + days[y]
    datesList[key] = ((date.today() + timedelta(2)).strftime('%m-%d-%Y'))
    availableDays[key] = f'{key}'

    dayOrder.append((date.today() + timedelta(3)).weekday())
    y = (date.today() + timedelta(3)).weekday()
    key = '' + days[y]    
    datesList[key] = ((date.today() + timedelta(3)).strftime('%m-%d-%Y'))

    dayOrder.append((date.today() + timedelta(4)).weekday())
    y = (date.today() + timedelta(4)).weekday()
    key = '' + days[y]    
    datesList[key] = ((date.today() + timedelta(4)).strftime('%m-%d-%Y'))

    dayOrder.append((date.today() + timedelta(5)).weekday())
    y = (date.today() + timedelta(5)).weekday()
    key = '' + days[y]    
    datesList[key] = ((date.today() + timedelta(5)).strftime('%m-%d-%Y'))

    dayOrder.append((date.today() + timedelta(6)).weekday())
    y = (date.today() + timedelta(6)).weekday()
    key = '' + days[y]    
    datesList[key] = ((date.today() + timedelta(6)).strftime('%m-%d-%Y'))

    statement = ''
    rv = {
        'sundayList':sundayList,
        'mondayList':mondayList,
        'tuesdayList':tuesdayList,
        'wednesdayList':wednesdayList,
        'thursdayList':thursdayList,
        'fridayList':fridayList,
        'saturdayList':saturdayList,
        'statement':statement,
        'datesList':datesList,
        'dayOrder':dayOrder,
        'availableDays':availableDays,
    }
    return render(request, 'fitnessClass/schedule.html', rv)

def verifyAnnualResident():
    return ''