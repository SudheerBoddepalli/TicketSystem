from django.contrib import admin
from django.utils.html import format_html
from django import forms
from .models import Venue, Show, Booking
from decimal import Decimal

class ShowAdminForm(forms.ModelForm):
    class Meta:
        model = Show
        fields = '__all__'

    def clean_start_time(self):
        start = self.cleaned_data.get('start_time')
        if start is None:
            raise forms.ValidationError("Start time is required.")
        return start

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')


@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ('title', 'show_type', 'venue', 'start_time', 'available_seats', 'price', 'image_tag')
    list_filter = ('show_type', 'venue')
    fields = ('title', 'description', 'show_type', 'venue', 'start_time', 'end_time', 'total_seats', 'available_seats', 'price', 'image')

    def image_tag(self, obj):
        if getattr(obj, 'image', None):
            return format_html('<img src="{}" style="height:50px;border-radius:4px;" />', obj.image.url)
        return "No Image"
    image_tag.short_description = 'Poster'


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'show', 'seats_booked', 'total_price', 'booked_at')
    list_filter = ('show',)