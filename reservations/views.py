from django.shortcuts import render, redirect
from datetime import datetime, date, timedelta
from . models import Reservation
from fitnessClass.models import FitnessClass
from accounts.models import Customer

# Create your views here.
def reserve_view(request):
    statement = ''
    className = request.POST.get('className')
    instructorName = request.POST.get('instructorName')
    startTime = request.POST.get('startTime')
    endTime = request.POST.get('endTime')
    classDate = request.POST.get('date')
    classId = request.POST.get('classId')
    today = (date.today().strftime('%m-%d-%Y'))
    if request.method == 'POST':
        availabilityTitle = 'Available Space'
        dateFormated = formatDate(classDate)        
        (available, max) = availability(classId, dateFormated)
        if available < 0:
            temp_available = f'{-(available)}'
            available = temp_available
            availabilityTitle = 'Wait-List of'
        return render(request, 'reservations/reserve.html', {'statement': statement, 'className':className, 'instructorName':instructorName, 'startTime':startTime, 'endTime':endTime, 'classDate':classDate , 'today': today, 'availabilityTitle': availabilityTitle, 'available':available, 'max':max, 'classId':classId })
    else:
        return redirect('fitnessClass:schedule')

def submission_view(request):
    classId = request.POST.get('classId')
    classDate = request.POST.get('classDate')
    dateFormated = formatDate(classDate)
    (available, max) = availability(classId, dateFormated)
    
    list = FitnessClass.objects.all().filter(id = classId)
    fitnessClass = ''
    for i in list:
        fitnessClass = i
   
    reservationInstance = Reservation()
    reservationInstance.classReserved = fitnessClass
    reservationInstance.customerReserving = getCustomer(request)
    reservationInstance.classDate = dateFormated

    statement = []
    statement.append(f'Reservation made for \n{classDate}')
    statement.append(f'\n {reservationInstance.classReserved}')    
    statement.append(f'by {(reservationInstance.customerReserving)}')


    if int(max) > 9:
        if int(available) > 10:
            reservationInstance.reservationStatus = 'Reserved'
        elif int(available) <= 10 and int(available) > 0:
            reservationInstance.reservationStatus = 'OverDraft'
        else:
            reservationInstance.reservationStatus = 'WaitList'
    else:
        if int(available) > 0:
            reservationInstance.reservationStatus = 'Reserved'
        else:
            reservationInstance.reservationStatus = 'WaitList'
    reservationInstance.save()
    return render(request, 'reservations/submission.html', {'statement':statement})    

def availability(classId, date):
    count = Reservation.objects.filter(reservationDate = date, classReserved = classId).count()
    max = FitnessClass.objects.values_list('maximumCapacity', flat=True).get(id=classId)    
    available = int(max) - count
    return (available, max)

def formatDate(date):
    dateStr = date[6:] + '-' + date[0:2] + '-' + date[3:5]
    return (dateStr)

def getCustomer(request):
    customerId = request.user.id
    list = Customer.objects.all().filter(user = customerId)
    customer = ''
    for i in list:
        customer = i
    return customer

