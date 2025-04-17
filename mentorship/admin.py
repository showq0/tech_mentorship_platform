from django.contrib import admin
from mentorship.models import User, Mentorship, BookingSlot, Session
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
    model = User

    fieldsets = BaseUserAdmin.fieldsets + (
        (None
         ,
         {"fields": ("role", "profile_info"),}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None
         , {"fields": ("role", "profile_info")}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', "role")

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['profile_info'].required = False
        return form


class BookingSlotAdmin(admin.ModelAdmin):
    list_display = ('mentor', "is_booked", "duration_minutes")


admin.site.register(User, UserAdmin)
admin.site.register(Mentorship)
admin.site.register(Session)
admin.site.register(BookingSlot, BookingSlotAdmin)
