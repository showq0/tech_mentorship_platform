from django.contrib import admin
from mentorship.models import Mentorship, BookingSlot, Session


class BookingSlotAdmin(admin.ModelAdmin):
    list_display = ('mentor', "is_booked", "duration_minutes")


admin.site.register(Mentorship)
admin.site.register(Session)
admin.site.register(BookingSlot, BookingSlotAdmin)
