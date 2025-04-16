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

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['profile_info'].required = False
        return form


admin.site.register(User, UserAdmin)
admin.site.register(Mentorship)
admin.site.register(Session)
admin.site.register(BookingSlot)
