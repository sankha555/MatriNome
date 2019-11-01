from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Proposal

class ProposeForm(forms.ModelForm):

    class Meta:
        model = Proposal
        fields = ['message',]
