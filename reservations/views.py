import time
from django.shortcuts import render, redirect
from datetime import datetime, date, timedelta
from . models import Reservation, WaitList
from fitnessClass.models import FitnessClass
from accounts.models import Customer
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url="accounts:login")
def reserve_view(request):
    if request.method == 'POST':
        statement = ''
        className = request.POST.get('className')
        instructorName = request.POST.get('instructorName')
        startTime = request.POST.get('startTime')
        endTime = request.POST.get('endTime')
        classDate = request.POST.get('date')
        classId = request.POST.get('classId')
        today = (date.today().strftime('%m-%d-%Y'))
        availabilityTitle = 'Available Space'
        dateFormated = formatDate(classDate)        
        (available, max) = availability(classId, dateFormated)
        if available < 1:
            temp_available = f'{-(available)}'
            available = temp_available
            availabilityTitle = 'Position on WaitList'
            available = (int(available) + 1)
        (duplicate, duplicateMessage) = checkDuplicateReservation(getCustomer(request), dateFormated, getFitnessClass(classId))
        rv = {
            'statement': statement,
            'className':className,
            'instructorName':instructorName,
            'startTime':startTime,
            'endTime':endTime,
            'classDate':classDate ,
            'today': today,
            'availabilityTitle': availabilityTitle,
            'available':available,
            'classId':classId,
            'duplicate':duplicate,
            'duplicateMessage':duplicateMessage
        }
        return render(request, 'reservations/reserve.html', rv)
    else:
        return redirect('fitnessClass:schedule')

@login_required(login_url="accounts:login")
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
    reservationInstance.reservationDate = datetime.now().today()
    reservationInstance.reservationTime = datetime.now().time()

    statement = []
    statement.append(f'Reservation made for \n{classDate}')
    statement.append(f'\n {reservationInstance.classReserved}')    
    statement.append(f'by {(reservationInstance.customerReserving)}')

    temp_waitList = WaitList()
    temp_waitList.save()
    nId = temp_waitList.id
    
    if int(max) > 9:
        if int(available) > 10:
            reservationInstance.reservationStatus = 'Reserved'
        elif int(available) <= 10 and int(available) > 0:
            reservationInstance.reservationStatus = 'OverDraft'
        else:
            reservationInstance.reservationStatus = 'WaitList'
            reservationInstance.waitNumber = nId
    else:
        if int(available) > 0:
            reservationInstance.reservationStatus = 'Reserved'
        else:
            reservationInstance.reservationStatus = 'WaitList'
            reservationInstance.waitNumber = nId
    reservationInstance.save()    

    waitList = getWaitListPosition(dateFormated, nId)
    if waitList > 0:
        statement.append(f'Wait List Position: {waitList + 1}')

    return render(request, 'reservations/submission.html', {'statement':statement})    

@login_required(login_url="accounts:login")
def myReservations_view(request):
    returnValue = []  
    if request.method == 'POST':
        reservationId = request.POST.get('reservationId')
        intId = Reservation.objects.all().filter(id = reservationId)
        temp_id = None
        for i in intId:
            temp_id = i.id
        Reservation.objects.filter(id = temp_id).delete()
    currentUser = request.user
    customer = Customer.objects.all().filter(user = currentUser)
    customerId = ''
    for i in customer:
        customerId = i.id
    todaysDate = date.today()
    select = Reservation.objects.all().filter(customerReserving = customerId).order_by('-classDate')
    for i in select:
        if i.reservationDate >= todaysDate:
            returnValue.append(i) 
    return render(request, 'reservations/myReservations.html', {'reservations':returnValue})

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

def getFitnessClass(classId):
    list = FitnessClass.objects.all().filter(id = classId)
    fitnessClass = ''
    for i in list:
        fitnessClass = i
    return fitnessClass

def getWaitListPosition(dateOfClass, currentWaitNumber):
    list = Reservation.objects.filter(classDate = dateOfClass)
    count = 0
    for line in list:
        waitNumber = line.waitNumber
        if waitNumber > 0 and waitNumber < currentWaitNumber:
            count += 1
    return count

def checkDuplicateReservation(customer, dateOfClass, classId):
    count = Reservation.objects.filter(customerReserving = customer, classReserved = classId, classDate = dateOfClass).count()
    if count > 0 :
        return (True, f'Duplicate Reservation, current count of reservations = {count}')
    else:
        return (False, f'Not a Duplicate Reservation, current count of reservations = {count}')
