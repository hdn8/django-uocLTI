from django.contrib import admin
from uocLTI.models import LTIProfile

class LTIProfileAdmin(admin.ModelAdmin):
    pass


admin.site.register(LTIProfile, LTIProfileAdmin)
