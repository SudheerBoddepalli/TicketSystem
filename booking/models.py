# booking/models.py
from decimal import Decimal
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

User = get_user_model()

class Venue(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Show(models.Model):
    TITLE_CHOICES = [
        ('movie', 'Movie'),
        ('event', 'Event'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    show_type = models.CharField(max_length=10, choices=TITLE_CHOICES, default='movie')
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    total_seats = models.PositiveIntegerField(default=100, validators=[MinValueValidator(1)])
    available_seats = models.PositiveIntegerField(default=100, validators=[MinValueValidator(0)])
    price = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('150.00'))
    # add image field (poster)
    image = models.ImageField(upload_to='posters/', null=True, blank=True)

    def __str__(self):
        # show date for clarity
        return f"{self.title} ({self.start_time.date()})"


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    seats_booked = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    booked_at = models.DateTimeField(auto_now_add=True)
    # computed field: not editable, allow null while constructing then set before saving/validation
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, editable=False)

    def __str__(self):
        return f"Booking #{self.id} by {self.user} for {self.show}"

    def clean(self):
        """
        Called by full_clean() (used by admin). Ensure total_price is set so validation won't fail.
        Also validate seat availability.
        """
        from django.core.exceptions import ValidationError

        if self.show is None:
            return  # other field errors will handle

        # seat availability check
        if self.seats_booked and self.show.available_seats is not None:
            if self.seats_booked > self.show.available_seats:
                raise ValidationError({'seats_booked': "Not enough seats available for this show."})

        # compute total_price so full_clean won't complain about null
        if self.seats_booked is not None:
            self.total_price = (Decimal(self.seats_booked) * Decimal(self.show.price)).quantize(Decimal('0.01'))

    def save(self, *args, **kwargs):
        # Ensure total_price is correct every time we save
        if self.show is not None and self.seats_booked is not None:
            self.total_price = (Decimal(self.seats_booked) * Decimal(self.show.price)).quantize(Decimal('0.01'))
        super().save(*args, **kwargs)
