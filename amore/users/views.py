from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
import requests
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import RegForm, ProfileUpdateForm

def register(request):
    if request.method == 'POST':
        form = RegForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            messages.success(request, f'Account created successfully for {username}')
            return redirect('home')
    else :
        form = RegForm()
    return render(request, 'users/register.html', {'form' : form})


def profile(request):
    if request.method == 'POST':
            form = ProfileUpdateForm(request.POST,
                                        request.FILES,
                                        instance=request.user.profile)

            if form.is_valid():
                form.save()

    else:
        form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'form' : form
    }

    return render(request, 'users/profile_update.html', context)

# Create your views here.
