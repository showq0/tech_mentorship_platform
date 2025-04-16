from django.contrib import admin
from mentorship.models import User, Mentorship, BookingSlot, Session


class UserAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['profile_info'].required = False
        return form


admin.site.register(User, UserAdmin)
admin.site.register(Mentorship)
admin.site.register(Session)
admin.site.register(BookingSlot)
