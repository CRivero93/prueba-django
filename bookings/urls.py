from django.urls import path

from .views import BookingsView, NewBookingView, BookingContactView

app_name = 'bookings'
urlpatterns = [
    path('', BookingsView.as_view(), name='index'),
    path('new/', NewBookingView.as_view(), name='new-booking'),
    path('new/room/', BookingContactView.as_view(), name='booking-contact')
    
]