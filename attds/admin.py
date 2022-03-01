from django.contrib import admin

# Register your models here.
from . models import *
admin.site.register(Teachers)
admin.site.register(Students)
admin.site.register(Attendance)
admin.site.register(Sessions)
admin.site.register(Subjects)
