from django.contrib import admin

from .models import Booking
from .models import Guest
from .models import RoomType

admin.site.register(Booking)
admin.site.register(Guest)
admin.site.register(RoomType)

