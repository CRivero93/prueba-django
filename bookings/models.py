from django.db import models
from .helpers import to_date, diff_dates, generate_locator
from .constants import phone_format, ROOM_TYPE_CHOICES
from django.core.validators import RegexValidator

class RoomType(models.Model):
    room_type     = models.CharField(max_length=15, choices=ROOM_TYPE_CHOICES)
    price         = models.DecimalField(max_digits=12, decimal_places=2)
    capacity      = models.IntegerField()
    total_rooms   = models.IntegerField()

    def __str__(self):
        return self.room_type

class Guest(models.Model):
    name  = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    phone_regex = RegexValidator(regex=r'^\d{9}$', message=phone_format)
    phone = models.CharField(validators=[phone_regex], max_length=9) 

    @classmethod
    def create(cls, datas):
        guest = cls(name=datas['name'], email=datas['email'], phone=datas['phone']) 
        guest.save()
        return guest
    
    def __str__(self):
        return self.name

class Booking(models.Model):
    entry_date     = models.DateField()
    departure_date = models.DateField()
    room_type      = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='bookings')
    number_guests  = models.IntegerField()
    guest_info     = models.ForeignKey(Guest, on_delete=models.PROTECT)
    total_price    = models.DecimalField(max_digits=12, decimal_places=2)
    locator        = models.CharField(max_length=10, unique=True)

    @classmethod
    def create(cls, datas, room, guest):    
        booking = cls(entry_date=datas['entry_date'], 
                        departure_date=datas['departure_date'],
                            room_type=room, 
                                number_guests=datas['number_guests'],
                                    guest_info=guest,
                                        total_price=room.price * diff_dates(to_date(datas['entry_date']), to_date(datas['departure_date'])),
                                            locator=generate_locator()) 
        booking.save()
        return booking

    def __str__(self):
        return self.locator



    