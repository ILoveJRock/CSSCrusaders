from django.contrib import admin
from .models import *

admin.site.register(Account)
admin.site.register(Supervisor)
admin.site.register(Instructor)
admin.site.register(TA)
admin.site.register(Course)
admin.site.register(LabSection)
admin.site.register(Course_LabSection)
