from django.shortcuts import render, get_object_or_404, redirect
from .models import Booking, RoomType, Guest
from .forms import NewBookingForm, ContactForm
from django.views import View
from django.urls import reverse
from .helpers import diff_dates
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponseRedirect
from .constants import select_dates, no_rooms_available
import json
from django.db.models import Q

# Create your views here.

def index_view(request):
    return redirect('/bookings/')

class BookingsView(View):
    template_name = "bookings/index.html"

    def get_bookings(self):
        return Booking.objects.all() 

    def get(self, request, *args, **kwargs):
        context  = {"booking_list": self.get_bookings()}
        return render(request, self.template_name, context)

class NewBookingView(View):
    template_name = "bookings/new_booking.html"
    def get(self, request, *args, **kwargs):
        context = {"form": NewBookingForm()}  
        if "message" in request.session:
            context["message"] = request.session["message"]
            del request.session["message"] 
        return render(request, self.template_name, context)       

    def post(self, request, *args, **kwargs):
        booking_form = NewBookingForm(request.POST)  
        context = {"form" : booking_form}
        if booking_form.is_valid():
            request.session["datas"] = json.dumps(booking_form.cleaned_data, cls=DjangoJSONEncoder)
            rooms = self.filter_rooms(booking_form.cleaned_data)
            if len(rooms) > 0: 
                context["rooms"] = rooms 
            else: 
                context["message"] = no_rooms_available

        return render(request, self.template_name, context)

    def filter_rooms(self, datas):
        filtered_rooms = []
        rooms = RoomType.objects.filter(capacity__gte=datas.get("number_guests"))
        for room in rooms:
            room_bookings = room.bookings.filter(Q(entry_date__range=(datas.get("entry_date"), datas.get("departure_date"))) |  
                                                Q(departure_date__range=(datas.get("entry_date"), datas.get("departure_date")))).count()

            if room_bookings >= room.total_rooms:
                continue
            room.total_available = room.total_rooms - room_bookings
            room.price *= diff_dates(datas.get("entry_date"), datas.get("departure_date"))
            filtered_rooms.append(room)
        return filtered_rooms

class BookingContactView(View):
    template_name = "bookings/booking_contact.html"

    def get(self, request, *args, **kwargs):
        request.session["message"] = select_dates
        return HttpResponseRedirect(reverse("bookings:new-booking"))
     
    def post(self, request, *args, **kwargs):
        if "choice" in request.POST:
            try:
                selected_room = RoomType.objects.get(pk=int(request.POST["choice"]))
            except (KeyError, RoomType.DoesNotExist):
                request.session["message"] = select_dates
                return HttpResponseRedirect(reverse("bookings:new-booking"))
            else:
                request.session["selected_room"] = int(request.POST["choice"])
                context = {"form": ContactForm()} 
            return render(request, self.template_name, context)
        else:
            contact_form = ContactForm(request.POST)
            context = {"form": contact_form} 
            if contact_form.is_valid():
                guest = Guest.create(contact_form.cleaned_data)
                room = get_object_or_404(RoomType, pk=request.session["selected_room"]) 
                Booking.create(json.loads(request.session["datas"]), room, guest)
                return HttpResponseRedirect(reverse("bookings:index"))

            return render(request, self.template_name, context)
