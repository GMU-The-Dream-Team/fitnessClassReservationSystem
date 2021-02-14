from datetime import date
from django.db.models.fields import DateField
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
        #(duplicate, duplicateMessage) = checkDuplicateReservation(1, dateFormated, getFitnessClass(classId)) #added to view reservations.html temporarily
        (duplicate, duplicateMessage) = checkDuplicateReservation(getCustomer(request), dateFormated, getFitnessClass(classId)) #original line
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
    statement = []
    
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

def staffReservations_view(request):
    rv = {}
    if request.method == 'GET':
        rv['statement'] = 'This is a get request'
        rv['flag'] = True
        select = FitnessClass.objects.all()
        classList = {}
        counter = 0
        for i in select:
            counter = i.id            
            classList[counter] = i
        rv['classList'] = classList
        return render(request, 'reservations/staffReservations.html', rv)
    else:
        classId = request.POST.get('classId')
        select = Reservation.objects.all().filter(classReserved = getFitnessClass(classId))
        reservedList = {}
        waitList = {}
        overDraftList = {}
        #enter code to send back the classes ID and present the staff memebers with the table 
        counter = 0
        reservedCounter = 0
        overDraftCounter = 0
        waitListCounter = 0
        for i in select:
            (flag, value) = checkDate(i.classDate)
            if flag == True:
                counter = i.id
                if i.reservationStatus == "Reserved":
                    reservedList[counter] = i
                    rv['reservedList'] = reservedList
                    reservedCounter += 1
                elif i.reservationStatus == "WaitList":
                    waitList[counter] = i
                    rv['waitList'] = waitList
                    waitListCounter += 1
                else:
                    overDraftList[counter] = i
                    rv['overDraftList'] = overDraftList
                    overDraftCounter += 1
            else:
                rv['statement'] = value
                rv['flag'] = False
                return render(request, 'reservations/staffReservations.html', rv)
        rv['reservedCounter'] = reservedCounter
        rv['waitListCounter'] = waitListCounter
        rv['overDraftCounter'] = overDraftCounter


        rv['statement'] = 'This is a post request'
        rv['flag'] = False
        return render(request, 'reservations/staffReservations.html', rv)

def availability(classId, date):
    count = Reservation.objects.filter(classDate = date, classReserved = classId).count()
    max = FitnessClass.objects.values_list('maximumCapacity', flat=True).get(id=classId)
    available = int(max) - count
    return (available, max)

# '01-01-2021' --> 2021-01-01
def formatDate(date):
    dateStr = date[6:] + '-' + date[0:2] + '-' + date[3:5]
    return (dateStr)

def checkDate(dateOfClass):
    #classDate = dateOfClass[6:11] + '-' + dateOfClass[0:2] + '-' + dateOfClass[3:5]
    temp_classDate = str(dateOfClass)
    classDate = temp_classDate[0:10]
    todayDate = date.today().strftime('%Y-%m-%d')
    if classDate < todayDate:
        return (False, 'The class date is in past')
    else:
        return (True, 'Today greater than today date')

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

def cancelFunction(dateOfClass, currentWaitNumber):
    list = Reservation.objects.filter(classDate = dateOfClass)
    waitList = []
    id = ''
    for line in list:
        waitNumber = line.waitNumber
        if waitNumber > 0 and waitNumber < currentWaitNumber:
            tempWait = min(waitList)
            if waitNumber < tempWait:
                id = line.id
    return id

def checkDuplicateReservation(customer, dateOfClass, classId):
    count = Reservation.objects.filter(customerReserving = customer, classReserved = classId, classDate = dateOfClass).count()
    if count > 0 :
        return (True, f'* You have already reserved for this class')
    else:
        return (False, '')