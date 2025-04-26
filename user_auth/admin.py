from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from user_auth.models import User


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


admin.site.register(User, UserAdmin)
