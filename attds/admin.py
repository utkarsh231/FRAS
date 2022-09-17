from django.contrib import admin
from import_export.admin import ImportExportMixin

from django.contrib.auth.admin import UserAdmin as BaseAdmin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from django.contrib.auth.models import User

class UserResource(resources.ModelResource):
    class Meta:
        model = User
        

class UserAdmin(BaseAdmin, ImportExportModelAdmin):
    resource_class = UserResource

admin.site.unregister(User)
admin.site.register(User, UserAdmin)


# Register your models here.
from . models import *
class TeachersAdmin (ImportExportMixin, admin.ModelAdmin):
    list_display=['teacher_name','dept','contact','img','userid']
admin.site.register(Teachers,TeachersAdmin)
class StudentsAdmin (ImportExportMixin, admin.ModelAdmin):
    list_display=['reg_num','name','dept','sem','sec','userid']
admin.site.register(Students,StudentsAdmin)
class AttendanceAdmin (ImportExportMixin, admin.ModelAdmin):
    list_display=['attd_id','student_id','session_id']
admin.site.register(Attendance,AttendanceAdmin)
class SessionsAdmin (ImportExportMixin, admin.ModelAdmin):
    list_display=['section','start_time','duration','teacher_id','subject_code']
admin.site.register(Sessions,SessionsAdmin)
class SubjectsAdmin (ImportExportMixin, admin.ModelAdmin):
    list_display=['sub_code','sub_name','dept','sem']
admin.site.register(Subjects,SubjectsAdmin)