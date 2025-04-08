from django.contrib import admin
from mentorship.models import Mentee, Mentor, Mentorship

# Register your models here.

admin.site.register(Mentee)
admin.site.register(Mentor)
admin.site.register(Mentorship)