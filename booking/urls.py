from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    path('', views.home, name='home'),
    path('show/<int:pk>/', views.show_detail, name='show_detail'),
    path('show/<int:pk>/book/', views.book_show, name='book_show'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),

    # custom signup and logout-then-auth landing
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/logout-and-auth/', views.logout_and_auth, name='logout_and_auth'),
]
