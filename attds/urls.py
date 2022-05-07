from django.urls import path,re_path
from django.conf import settings
from django.conf.urls.static import static

from . import views

#m=views.Mark()
urlpatterns = [
    path('',views.home,name='home'),
    path('teacher_login',views.teacher_login,name="teacher_login"),
    path('logout',views.logout,name="logout"),
    path('student',views.student,name='student'),
    path('join_session/<int:id>/',views.join_session,name='join_session'),
    path('student_login',views.student_login,name='student_login'),
    path('create_session',views.create_session,name='create_session'),
    path('teacher',views.teacher,name='teacher'),
    path('delete/<int:id>/',views.delete,name='delete'),
    path('update/<int:id>/',views.update,name='update'),
    path(r'^export/csv/$/<int:id>/', views.export_users_csv, name='export_users_csv'),
    


    path('admins',views.admins,name='admins'),
    path('train',views.train,name='train'),
    path('run',views.mark_your_attendance,name='run'),
    path('facecam_feed',views.facecam_feed,name='facecam_feed'),
    #path('student_register',views.student_register,name='student_register'),
    path('stdnt',views.stdnt,name='stdnt'),
    path('create_dataset',views.create_dataset,name='create_dataset'),


    path('cam',views.cam,name='cam'),
    path('livefe',views.livefe,name='livefe'),

]
