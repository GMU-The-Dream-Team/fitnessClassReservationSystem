from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .import models
from django.utils.translation import ugettext_lazy as _

class UserForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = models.Account
        fields = ['username', 'email', 'firstName', 'lastName', 'street', 'city', 'state', 'zipcode', 'phoneNumber']
        labels = {
            'username': _('User Name'),
            'email': _('Email'),
            'firstName' : _('First Name'),
            'lastName': _('Last Name'),
            'street': _('Street Address'),
            'city': _('City'),
            'state': _('State'),
            'zipcode': _('Zipcode'),
            'phoneNumber': _('Phone Number')
        }