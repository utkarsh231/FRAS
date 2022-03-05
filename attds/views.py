import http
from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
#from mysqlx import Session
from attds.models import Attendance, Students, Subjects, Teachers, Sessions
from django.contrib import messages
from django.contrib.auth.models import User
from datetime import date
import time
import csv
from datetime import datetime
# Create your views here.

def home(request):
    return render(request,'index.html')

def logout(request):
    auth.logout(request)
    return redirect("/")

def teacher(request):
    #get user details
    d = Teachers.objects.filter(userid=request.user.id)
    #get all sessions details created by the user logged in
    s = Sessions.objects.filter(teacher_id=request.user.id)
    mn=[]
    #get all the start_time and dur from each sessions and turn it into miliseconds format.
    for i in range(len(s)):
        starttime = int(round(s[i].start_time.timestamp()*1000))
        timelimit = int(s[i].duration*60*1000)
        #if starttime > current time i.e for the scheduled time
        #then set start_time = 0
        if starttime>int(time.time()*1000):
            #make a list of all the scheduled time
            mn.append(starttime)
            s[i].duration = s[i].start_time
            s[i].start_time = 0 #for scheduled time
        elif starttime+timelimit<int(time.time()*1000):
            s[i].duration = str(s[i].start_time.strftime("%b. %d, %Y"))[:14]
            s[i].start_time = 1 #for expired time
        else:
            s[i].start_time=starttime +  timelimit
        #get the min of scheduled time
    try:
        
        date = str(datetime.fromtimestamp(min(mn) / 1e3)).split(" ")[1].split(":")
        hr=int(date[0])
        minu=int(date[1])
        sec=int(date[2])
    except:
        hr=0
        minu=0
        sec=0
    return render(request,'teacher.html',{'user':d[0],'sessions':s,'hr':hr,'minu':minu,'sec':sec})

def teacher_login(request):
    #fetch the submitted login details 
        username = request.POST['user'].lower()
        password = request.POST['pass']
        user=authenticate(username=username,password=password)
        if user:
            auth.login(request,user)
        else:
            #for invalid user/pass
            #notify the user with a message.
            messages.info(request,'Invalid username or password')
            return redirect("/")
        #fetch teacher details from teachers table where users= loggedin user
        d = Teachers.objects.filter(userid=request.user.id)
        if not d:
            return redirect("/")
        #user is logged in
        # now take the user to teachers page.
        messages.success(request, ('logged'))
        return redirect("teacher")

def create_session(request):    
        #fetch all the details from teachers form page.
        sub_code = request.POST['sub_code']
        sec = request.POST['sec'].upper()
        stime = request.POST['stime']
        dur = request.POST['dur']
        #get the subject whose sub_code is sub_code
        s=Subjects.objects.filter(sub_code=sub_code)
        #insert all the data in the session table
        d= Sessions(section=sec,start_time=stime,duration=dur,subject_code=s[0],teacher_id=request.user)
        d.save()
        #after the session data is fed into the database, then redirect the user to the teachers page
        messages.info(request,'created')
        return redirect("teacher")




def student(request):
    #get logged in student details else pass Null data
    try:
        d = Students.objects.filter(userid=request.user.id)[0]
    except:
        d=[]
    #get all sessions 
    s = Sessions.objects.all()
    mn=[]
    #get all the start_time and dur from each sessions and turn it into miliseconds format.
    for i in range(len(s)):
        starttime = int(round(s[i].start_time.timestamp()*1000))
        timelimit = int(s[i].duration*60*1000)
        #if starttime > current time i.e for the scheduled time
        #then set start_time = 0
        if starttime>int(time.time()*1000):
            #make a list of all the scheduled time
            mn.append(starttime)
            s[i].duration = s[i].start_time
            s[i].start_time = 0 #for scheduled time
        elif starttime+timelimit<int(time.time()*1000):
            s[i].duration = str(s[i].start_time.strftime("%b. %d, %Y"))[:14]
            s[i].start_time = 1 #for expired time
        else:
            s[i].start_time=starttime +  timelimit
        #get the min of scheduled time
    try:
        
        date = str(datetime.fromtimestamp(min(mn) / 1e3)).split(" ")[1].split(":")
        hr=int(date[0])
        minu=int(date[1])
        sec=int(date[2])
    except:
        hr=0
        minu=0
        sec=0
    return render(request,'student.html',{'stu_data':d,'sessions':s,'hr':hr,'minu':minu,'sec':sec})

    
    #return render(request,'join_session.html',{'stu_data':d})

def student_login(request):
    stu = request.POST['user']
    passw = request.POST['pass']
    #authenticate the user
    user=authenticate(username=stu,password=passw)
    #if user exists, then login the user and open the join_session with user details
    if user:
        auth.login(request,user)
        messages.success(request, ('logged'))
    else:
        messages.success(request, ('invalid'))
    #redirect the user to join_session page
    return redirect("student")

#delete sessions 
def delete(request,id):
    if request.method=='GET':
        d = Sessions.objects.get(pk=id)
        #delete all the attendance table data related of this session.
        a = Attendance.objects.filter(session_id=id)
        a.delete()
        d.delete()
        messages.info(request,"deleted")
    return redirect("teacher")

#update sessions
def update(request,id):
    sub_code = request.POST['sub_code']
    sec = request.POST['sec'].upper()
    stime = request.POST['stime']
    dur = request.POST['dur']
    s=Subjects.objects.filter(sub_code=sub_code)
    u = Sessions.objects.get(pk=id)
    u.section=sec
    u.start_time=stime
    u.duration=dur
    u.subject_code=s[0]
    #delete all the attendance table data related of this session.
    a = Attendance.objects.filter(session_id=id)
    a.delete()
    
    u.save()
    messages.info(request,'updated')
    return redirect("teacher")

def export_users_csv(request,id):
    #fetch the session with the pk=id to retriev the date of session
    session = Sessions.objects.get(pk=id)
    file_name = session.start_time.strftime("%d-%m-%Y")+'.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + file_name

    #writing the header in the csv file
    writer = csv.writer(response)
    writer.writerow(['Reg_Num', 'Name', 'Attendance'])
    
    #fetch the data to be filled in csv

    #get the data of all the students for whom the session is made.
    students = Students.objects.filter(sec=session.section,dept=session.subject_code.dept,sem=session.subject_code.sem)
    #get the name of the students and their respective registration number in the list.
    students_data = []
    for i in students:
        temp=[]
        temp.append(str(i.reg_num))
        temp.append(i.name)
        students_data.append(temp)
    


    #get all attendance data where session id matches
    attendance_data = Attendance.objects.filter(session_id = id)
    #get all students from the class who has given attendance
    students_attended = []
    for i in attendance_data:
        students_attended.append(i.student_id.name)
    

    #check for all the students from students_data, if they are present in students_attended
    # if yes, insert value 'Present' else 'Absent'
    for i in students_data:
        if i[1] in students_attended:
            i.append('Present')
        else:
            i.append('Absent')

    #sort the data w.r.t student name
    students_data=sorted(students_data, key = lambda x: x[1]) 

    #users = User.objects.all().values_list('username', 'first_name','email')
    
    for student in students_data:
        writer.writerow(tuple(student))

    return response


def join_session(request,id):
    if request.user.is_authenticated:
        #check if user has already given the attendence or not
        #find if there is any data in Attendence table, where 
        #student_id = request.user.id and session_id = id
        atd = Attendance.objects.filter(student_id=Students.objects.get(userid=request.user.id).id,session_id=id)
        if len(atd)==1:
            #message user that they have already given its attendance.
            messages.success(request, ('Given'))
            return redirect("student")



        #check if user is actually a student of this session or not.
        #if yes, then direct user to cam page, else send a message in the student page.
        
        #match department, semester, and section of session and student
        #if all matches, then take user to cam page.
        d = Students.objects.get(userid=request.user.id)
        s = Sessions.objects.get(pk=id)
        d_dept=d.dept
        d_sem=d.sem
        d_sec=d.sec
        s_dept=s.subject_code.dept
        s_sem=s.subject_code.sem
        s_sec=s.section
        if d_dept==s_dept and d_sem==s_sem and d_sec==s_sec:
            return render(request,'cam.html')
        else:
            #message user that they are not a member of the session.
            messages.success(request, ('Notmember'))
            return redirect("student")

        #return HttpResponse("<h1>Hello</h1>")
    
    