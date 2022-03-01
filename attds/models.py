from django.db import models
from django.contrib.auth.models import User,auth
# Create your models here.

class Teachers(models.Model):
    teacher_name = models.CharField(max_length=50)
    dept = models.CharField(max_length=50)
    contact = models.EmailField(max_length=30)
    img = models.ImageField(upload_to='images/')
    userid = models.ForeignKey(User,on_delete=models.CASCADE)

class Students(models.Model):
    reg_num = models.IntegerField()
    name = models.CharField(max_length=50)
    dept = models.CharField(max_length=50)
    sem =  models.IntegerField()
    sec = models.CharField(max_length=1)
    userid = models.ForeignKey(User,on_delete=models.CASCADE)

class Subjects(models.Model):
    sub_code = models.CharField(max_length=20)
    sub_name = models.CharField(max_length=100)
    dept = models.CharField(max_length=50)
    sem = models.IntegerField()
    

class Sessions(models.Model):
    #subject_name = models.CharField(max_length=50)
    #dept = models.CharField(max_length=50)
    #sem = models.IntegerField()
    section = models.CharField(max_length=1)
    start_time = models.DateTimeField()
    duration = models.IntegerField()
    teacher_id = models.ForeignKey(User,on_delete=models.CASCADE)
    subject_code = models.ForeignKey(Subjects,on_delete=models.CASCADE)

class Attendance(models.Model):
    attd_id = models.IntegerField()
    student_id = models.ForeignKey(Students,on_delete=models.CASCADE,default=1)
    session_id = models.ForeignKey(Sessions,on_delete=models.CASCADE,default=1)


#Lets make a subject table, that will contain the
#sub_code, sub_name, dept, sem

