from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone

from .models import Show
from .forms import BookingForm

def home(request):
    # timezone-aware now
    now = timezone.now()
    shows = Show.objects.filter(start_time__gte=now).order_by('start_time')
    return render(request, 'booking/home.html', {'shows': shows})

def show_detail(request, pk):
    show = get_object_or_404(Show, pk=pk)
    form = BookingForm()
    return render(request, 'booking/show_detail.html', {'show': show, 'form': form})

@login_required
def book_show(request, pk):
    show = get_object_or_404(Show, pk=pk)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            seats = form.cleaned_data['seats']
            if seats > show.available_seats:
                messages.error(request, 'Not enough seats available.')
                return redirect(reverse('booking:show_detail', args=[pk]))
            total = Decimal(seats) * show.price
            from .models import Booking
            booking = Booking.objects.create(
                user=request.user,
                show=show,
                seats_booked=seats,
                total_price=total
            )
            # decrement available seats
            show.available_seats -= seats
            show.save()
            messages.success(request, f'Booking successful! Booking id: {booking.id}')
            return redirect(reverse('booking:my_bookings'))
    messages.error(request, 'Invalid request.')
    return redirect(reverse('booking:show_detail', args=[pk]))

@login_required
def my_bookings(request):
    bookings = request.user.booking_set.select_related('show').order_by('-booked_at')
    return render(request, 'booking/my_bookings.html', {'bookings': bookings})


# -----------------------
# Auth landing & Signup
# -----------------------

def logout_and_auth(request):
    """
    Log the user out (if logged in) and render a page with Login + Signup forms.
    Clicking signup posts to booking:signup, login posts to the built-in login view.
    """
    if request.user.is_authenticated:
        logout(request)

    signup_form = UserCreationForm()
    return render(request, 'booking/auth_landing.html', {'signup_form': signup_form})


def signup(request):
    """
    Handle user signup. On success, automatically authenticate/login and redirect to home.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                messages.success(request, "Signup successful. Welcome!")
                return redirect('booking:home')
            else:
                messages.warning(request, "Signup succeeded but automatic login failed. Please log in.")
                return redirect('login')
        # if form invalid, re-render the auth landing with errors
        return render(request, 'booking/auth_landing.html', {'signup_form': form})
    # GET -> redirect to landing
    return redirect('booking:logout_and_auth')
