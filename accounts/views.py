from django.core import exceptions
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from accounts.forms import UserForm
from django.contrib.auth import login, logout
from . models import *

def signup_view(request):
    statement = 'Create User Form Get REquest'
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email').lower().strip()
            username = form.cleaned_data.get('username').lower().strip()
            firstName = form.cleaned_data.get('firstName').lower().strip()
            lastName = form.cleaned_data.get('lastName').lower().strip()
            street = form.cleaned_data.get('street').lower().strip()
            city = form.cleaned_data.get('city').lower().strip()
            state = form.cleaned_data.get('state').lower().strip()           
            zipcode = form.cleaned_data.get('zipcode').lower().strip()
            phoneNumber = form.cleaned_data.get('phoneNumber').lower().strip()
            password = form.cleaned_data.get('password1').strip()
            try:
                user = Account.objects.create_user(email, username, firstName, lastName, street, city, state, zipcode, phoneNumber, password)
            except ValueError as e:
                errorMessage = e
                return render(request, 'accounts/signup.html', {'form': form, 'statement':errorMessage})
            login(request, user)
            return redirect('fitnessClass:schedule')
        else:
            statement = "* Invalid User Account Information, please verify all requirments are met."
    else:
        form = UserForm()
    return render(request, 'accounts/signup.html', { 'form': form, 'statement':statement })
        

    ###### original start ######
    statement = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        custForm = forms.CustomerForm(request.POST)
        if form.is_valid():
            if custForm.is_valid():
                    email = custForm.cleaned_data.get('email').lower().strip()
                    firstName = custForm.cleaned_data.get('firstName').lower().strip()
                    lastName = custForm.cleaned_data.get('lastName').lower().strip()
                    userInfo = [email, firstName, lastName]
                    (flag, value) = checkDuplicateUser(userInfo)
                    if flag == False:
                        form = UserCreationForm()
                        custForm = forms.CustomerForm()
                        statement = value
                        return render(request, 'accounts/signup.html', { 'form': form, 'customerForm': custForm , 'statement':statement})
                    user = form.save(commit=False)                
                    instance = Customer()
                    instance.email = email
                    instance.firstName = firstName
                    instance.lastName = lastName
                    instance.street = custForm.cleaned_data.get('street').lower().strip()
                    instance.city = custForm.cleaned_data.get('city').lower().strip()
                    instance.state = custForm.cleaned_data.get('state').lower().strip()           
                    instance.zipcode = custForm.cleaned_data.get('zipcode').lower().strip()
                    instance.phoneNumber = request.POST.get('phoneNumber').lower().strip()
                    instance.verified = 'UnVerified'
                    instance.user = user
                    user = form.save()                                    
                    instance.save()
                    login(request, user)
                    return redirect('fitnessClass:schedule')
            else:
                statement = "* Invalid Customer Information, please verify all requirements are met."
        else:
            statement = "* Invalid User Account Information, please verify all requirments are met."
    else:
        form = UserCreationForm()
        custForm = forms.CustomerForm()
    return render(request, 'accounts/signup.html', { 'form': form, 'customerForm': custForm , 'statement':statement })
    
    ###### original end ######


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
               return redirect('fitnessClass:schedule')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', { 'form': form })

def logout_view(request):
    if request.method == 'GET':
        logout(request)
        form = AuthenticationForm
        return render(request, 'accounts/login.html', {'form':form})

def checkDuplicateUser(userInfo):
    email = userInfo[0].lower().strip()
    firstName = userInfo[1].lower().strip()
    lastName = userInfo[2].lower().strip()
    count = Customer.objects.all().filter( email = email, firstName = firstName, lastName = lastName)
    if len(count) > 0:
        return(False, '* User account already exists with same customer details')
    return(True, '')