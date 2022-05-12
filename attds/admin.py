from django.contrib import admin
from .models import Chat

# Register your models here.
from . models import *
admin.site.register(Teachers)
admin.site.register(Students)
admin.site.register(Attendance)
admin.site.register(Sessions)
admin.site.register(Subjects)
admin.site.register(Chat)
