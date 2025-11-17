from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.urls import reverse

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created. Please login.')
            return redirect(reverse('login'))
    else:
        form = UserCreationForm()
    return render(request, 'booking/signup.html', {'form': form})
