
import http
import threading
from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from requests import session
from .models import *

from matplotlib import pyplot as plt, rcParams
from sklearn.manifold import TSNE
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
#from mysqlx import Session
#from attds.models import Attendance, Students, Subjects, Teachers, Sessions
#from django.contrib import messages
#from django.contrib.auth.models import User
from datetime import date
import time
from datetime import datetime
import numpy as np


import face_recognition
import threading

import csv
import imutils
from imutils.video import VideoStream
from imutils.face_utils import rect_to_bb
from imutils.face_utils import FaceAligner

from imutils import face_utils
import os
from face_recognition.face_recognition_cli import image_files_in_folder
import pickle
import cv2
#from cv2 import *
import dlib
from django.views.decorators import gzip
from django.http.response import StreamingHttpResponse



from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import cv2
import threading


#from recognition.camera import FaceDetect
from collections import Counter
#model libraries

# Create your views here.

import re
import base64
#import PIL.Image as Image 
#import io

#import Augmentor
from numpy import asarray
#from PIL import Image

#from .models import Chat

def home(request):
    print("sdfeferrf")
    return render(request,'index.html')

def logout(request):
    auth.logout(request)
    return redirect("/")

def teacher(request):
    #get user details
    d = Teachers.objects.filter(userid=request.user.id)
    #if its not the teacher and its the admin, then logout the admin.
    if not d:
        auth.logout(request)
        return render(request,'index.html')
    
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
        s=Subjects.objects.filter(sub_code=sub_code.upper())

        #if wrong subject code is given, then just give message to teachers
        if not s:
            messages.info(request, ('wrong'))
            return redirect("teacher")
            
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
        auth.logout(request)
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



def open_cam(request):
    print("opening")
    #return render(request,'index.html')
    return HttpResponse("<h1>World</h1>")
   
def mark_your_attendance(request):
    return 201900185


def join_session(request,id):
    if request.user.is_authenticated:
        #check if user has already given the attendence or not
        #find if there is any data in Attendence table, where 
        #student_id = request.user.id and session_id = id
        d = Students.objects.get(userid=request.user.id)
        s = Sessions.objects.get(pk=id)
        atd = Attendance.objects.filter(student_id=d,session_id=s)

        if len(atd)==1:
            #message user that they have already given its attendance.
            messages.success(request, ('Given'))
            return redirect("student")



        #check if user is actually a student of this session or not.
        #if yes, then direct user to cam page, else send a message in the student page.
        
        #match department, semester, and section of session and student
        #if all matches, then take user to cam page.
        
        d_dept=d.dept
        d_sem=d.sem
        d_sec=d.sec
        s_dept=s.subject_code.dept
        s_sem=s.subject_code.sem
        s_sec=s.section
        
        if d_dept==s_dept and d_sem==s_sem and (d_sec==s_sec or s_sec=='ELECTIVE'):
            #print('abc')
            #out=open_camera(request)
            #print('zyz')
            #return render(request,'demo.html')
            out=mark_your_attendance(request)
            if str(d.reg_num)==out:
                d=Attendance(attd_id=1234,student_id=d,session_id=s)
                messages.success(request, ('Taken'))
                d.save()
            else:
                messages.success(request, ('unknown'))
            #return render(request,'student.html')
            return redirect("student")
        else:
            #message user that they are not a member of the session.
            messages.success(request, ('Notmember'))
            return redirect("student")

        #return HttpResponse("<h1>Hello</h1>")
def admins(request):
    return render(request,'admin.html')
    

def create_dataset(request):
    id=request.GET['regno']
    Dataset = 'C:/Users/DCQUASTER JACK/projects/fras/attds/Face_Recognition_Data/Dataset/'
    #id = username
    if((os.path.exists(Dataset+id))==False):
        os.makedirs(Dataset+id)
        directory=Dataset+id

	# Detect face
	#Loading the HOG face detector and the shape predictpr for allignment
    print("[INFO] Loading the facial detector")
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('attds/Face_Recognition_Data/shape_predictor_68_face_landmarks.dat')   #Add path to the shape predictor ######CHANGE TO RELATIVE PATH LATER
    fa = FaceAligner(predictor , desiredFaceWidth = 96)
	#capture images from the webcam and process and detect the face
	# Initialize the video stream
    print("[INFO] Initializing Video stream")
    vs = VideoStream(src=0).start()
	#time.sleep(2.0) ####CHECK######

	# Our identifier
	# We will put the id here and we will store the id with a face, so that later we can identify whose face it is
	
	# Our dataset naming counter
    sampleNum = 0
	# Capturing the faces one by one and detect the faces and showing it on the window
    while(True):
		# Capturing the image
		#vs.read each frame
        frame = vs.read()
		#Resize each image
        frame = imutils.resize(frame ,width = 800)
		#the returned img is a colored image but for the classifier to work we need a greyscale image
		#to convert
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		#To store the faces
		#This will detect all the images in the current frame, and it will return the coordinates of the faces
		#Takes in image and some other parameter for accurate result
        faces = detector(gray_frame,0)
		#In above 'faces' variable there can be multiple faces so we have to get each and every face and draw a rectangle around it.
        for face in faces:
            print("inside for loop")
            (x,y,w,h) = face_utils.rect_to_bb(face)
            face_aligned = fa.align(frame,gray_frame,face)
			# Whenever the program captures the face, we will write that is a folder
			# Before capturing the face, we need to tell the script whose face it is
			# For that we will need an identifier, here we call it id
			# So now we captured a face, we need to write it in a file
            sampleNum = sampleNum+1
			# Saving the image dataset, but only the face part, cropping the rest
            if face is None:
                print("face is none")
                continue
            cv2.imwrite(directory+'/'+str(sampleNum)+'.jpg'	, face_aligned)
            face_aligned = imutils.resize(face_aligned ,width = 400)
			#cv2.imshow("Image Captured",face_aligned)
			# @params the initial point of the rectangle will be x,y and
			# @params end point will be x+width and y+height
			# @params along with color of the rectangle
			# @params thickness of the rectangle
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),1)
			# Before continuing to the next loop, I want to give it a little pause
			# waitKey of 100 millisecond
            cv2.waitKey(50)

		#Showing the image in another window
		#Creates a window with window name "Face" and with the image img
        cv2.imshow("Add Images",frame)
		#Before closing it we need to give a wait command, otherwise the open cv wont work
		# @params with the millisecond of delay 1
        cv2.waitKey(1)
		#To get out of the loop
        if(sampleNum>100):
            break
	
	#Stoping the videostream
    vs.stop()
	# destroying all the windows
    cv2.destroyAllWindows()
    return render(request,'student.html')





def visualize(username="Elon Musk"):
    id=username
    if os.path.exists('attds/Face_Recognition_Data/Training_Dataset/{}/'.format(id)==False):
        os.makedirs('attds/Face_Recognition_Data/Training_Dataset/{}/'.format(id))
        directory='attds/Face_Recognition_Data/Training_Dataset/{}/'.format(id)
        print("[INFO] Loading the facial detector")
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor('attds/Face_Recognition_Data/shape_predictor_68_face_landmarks.dat')   #Add path to the shape predictor ######CHANGE TO RELATIVE PATH LATER
        fa = FaceAligner(predictor , desiredFaceWidth = 96)
        #capture images from the webcam and process and detect the face
        # Initialize the video stream
        print("[INFO] Initializing Video stream")
        vs = VideoStream(src=0).start()
        #time.sleep(2.0) ####CHECK######

        # Our identifier
        # We will put the id here and we will store the id with a face, so that later we can identify whose face it is
        
        # Our dataset naming counter
        sampleNum = 0
        # Capturing the faces one by one and detect the faces and showing it on the window
        while(True):
            # Capturing the image
            #vs.read each frame
            frame = vs.read()
            #Resize each image
            frame = imutils.resize(frame ,width = 800)
            #the returned img is a colored image but for the classifier to work we need a greyscale image
            #to convert
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            #To store the faces
            #This will detect all the images in the current frame, and it will return the coordinates of the faces
            #Takes in image and some other parameter for accurate result
            faces = detector(gray_frame,0)
            #In above 'faces' variable there can be multiple faces so we have to get each and every face and draw a rectangle around it.
            
            
                


            for face in faces:
                print("inside for loop")
                (x,y,w,h) = face_utils.rect_to_bb(face)

                face_aligned = fa.align(frame,gray_frame,face)
                # Whenever the program captures the face, we will write that is a folder
                # Before capturing the face, we need to tell the script whose face it is
                # For that we will need an identifier, here we call it id
                # So now we captured a face, we need to write it in a file
                sampleNum = sampleNum+1
                # Saving the image dataset, but only the face part, cropping the rest
                
                if face is None:
                    print("face is none")
                    continue


                

                cv2.imwrite(directory+'/'+str(sampleNum)+'.jpg'	, face_aligned)
                face_aligned = imutils.resize(face_aligned ,width = 400)
                #cv2.imshow("Image Captured",face_aligned)
                # @params the initial point of the rectangle will be x,y and
                # @params end point will be x+width and y+height
                # @params along with color of the rectangle
                # @params thickness of the rectangle
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),1)
                # Before continuing to the next loop, I want to give it a little pause
                # waitKey of 100 millisecond
                cv2.waitKey(50)

            #Showing the image in another window
            #Creates a window with window name "Face" and with the image img
            cv2.imshow("Add Images",frame)
            #Before closing it we need to give a wait command, otherwise the open cv wont work
            # @params with the millisecond of delay 1
            cv2.waitKey(1)
            #To get out of the loop
            if(sampleNum>300):
                break
        
        #Stoping the videostream
        vs.stop()
        # destroying all the windows
        cv2.destroyAllWindows()
         


def predict(face_aligned,svc,threshold=0.7):
    face_encodings=np.zeros((1,128))
    try:
        x_face_locations=face_recognition.face_locations(face_aligned)
        faces_encodings=face_recognition.face_encodings(face_aligned,known_face_locations=x_face_locations)
        if(len(faces_encodings)==0):
            return ([-1],[0])
    except:
        return ([-1],[0])
    prob=svc.predict_proba(faces_encodings)
    result=np.where(prob[0]==np.amax(prob[0]))
    if(prob[0][result[0]]<=threshold):
        return ([-1],prob[0][result[0]])
    
    #print(result[0],prob[0][result[0]])
    return (result[0],prob[0][result[0]])


def vizualize_Data(embedded, targets,):
	
	X_embedded = TSNE(n_components=2).fit_transform(embedded)

	for i, t in enumerate(set(targets)):
		idx = targets == t
		plt.scatter(X_embedded[idx, 0], X_embedded[idx, 1], label=t)

	plt.legend(bbox_to_anchor=(1, 1));
	rcParams.update({'figure.autolayout': True})
	plt.tight_layout()	
	plt.savefig('./recognition/static/recognition/img/training_visualisation.png')
	plt.close()


#class Mark:
def mark_your_attendance(request):
    op=[]
    detector=dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(r'C:\Users\DCQUASTER JACK\projects\fras\attds\Face_Recognition_Data\shape_predictor_68_face_landmarks.dat')
    #Add path to the shape predictor ######CHANGE TO RELATIVE PATH LATER
    svc_save_path=r"C:\Users\DCQUASTER JACK\projects\fras\attds\Face_Recognition_Data\svc.sav"	
    with open(svc_save_path, 'rb') as f:
        svc = pickle.load(f)
        fa = FaceAligner(predictor , desiredFaceWidth = 96)
        encoder=LabelEncoder()
        encoder.classes_ = np.load(r'C:\Users\DCQUASTER JACK\projects\fras\attds\Face_Recognition_Data\classes.npy')
    
    faces_encodings = np.zeros((1,128))
    no_of_faces = len(svc.predict_proba(faces_encodings)[0])
    count = dict()
    present = dict()
    log_time = dict()
    start = dict()
    for i in range(no_of_faces):
        count[encoder.inverse_transform([i])[0]] = 0
        present[encoder.inverse_transform([i])[0]] = False
    vs = VideoStream(src=0).start()
    #fps=FPS().start()
    sampleNum = 0
    startTime = time.time()
    timeElapsed = time.time()  - startTime
    secElapsed = int(timeElapsed)
    rt=0
    while(secElapsed<20):
        timeElapsed = time.time() - startTime
        secElapsed = int(timeElapsed)
        frame = vs.read()
        frame = imutils.resize(frame ,width = 800)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray_frame,0)
        print(faces)
        for face in faces:
            print("INFO : inside for loop")
            (x,y,w,h) = face_utils.rect_to_bb(face)
            face_aligned = fa.align(frame,gray_frame,face)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),1)		
            (pred,prob)=predict(face_aligned,svc)
            if(pred!=[-1]):
                person_name=encoder.inverse_transform(np.ravel([pred]))[0]
                pred=person_name
                if count[pred] == 0:
                    start[pred] = time.time()
                    count[pred] = count.get(pred,0) + 1
                if count[pred] == 4 and (time.time()-start[pred]) > 1.2:
                    count[pred] = 0 
                else:
                    #if count[pred] == 4 and (time.time()-start) <= 1.5:
                    present[pred] = True
                    #log_time[pred] = datetime.datetime.now()
                    log_time[pred] =2
                    count[pred] = count.get(pred,0) + 1
                    print(pred, present[pred], count[pred])
                    op.append(pred)
                    cv2.putText(frame, str(person_name)+ str(prob), (x+6,y+h-6), cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),1)
            else:
                person_name="unknown"
                cv2.putText(frame, str(person_name), (x+6,y+h-6), cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),1)

            #cv2.putText()
            # Before continuing to the next loop, I want to give it a little pause
            # waitKey of 100 millisecond
            #cv2.waitKey(50)

        #Showing the image in another window
        #Creates a window with window name "Face" and with the image img
        cv2.imshow("Mark Attendance - In - Press q to exit",frame)
        #Before closing it we need to give a wait command, otherwise the open cv wont work
        # @params with the millisecond of delay 1
        #cv2.waitKey(1)
        #To get out of the loop
        key=cv2.waitKey(50) & 0xFF

        if len(op)>10:
            c = Counter(op)
            c.most_common(1)
            rt=c.most_common(1)[0][0]
            break
            #check if prediction is mathcing with person logged in
            #if yes, then mark the attendance of the user for specific session.
            #if not, then send the message to the user, Invalid User.
        if(key==ord("q")):
            break
        #if frame:
        #    fps.update()
        #    ret,jpeg=cv2.imencode('.jpeg',frame)
        #    yield jpeg.tobytes()
    #Stoping the videostream
    vs.stop()

    # destroying all the windows
    cv2.destroyAllWindows()
    #update_attendance_in_db_in(present)
    return rt



def mark_your_attendance_out(request):
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('face_recognition_data/shape_predictor_68_face_landmarks.dat')   #Add path to the shape predictor ######CHANGE TO RELATIVE PATH LATER
    svc_save_path="face_recognition_data/svc.sav"	
    with open(svc_save_path, 'rb') as f:
        svc = pickle.load(f)
    fa = FaceAligner(predictor , desiredFaceWidth = 96)
    encoder=LabelEncoder()
    encoder.classes_ = np.load('face_recognition_data/classes.npy')
    faces_encodings = np.zeros((1,128))
    no_of_faces = len(svc.predict_proba(faces_encodings)[0])
    count = dict()
    present = dict()
    log_time = dict()
    start = dict()
    for i in range(no_of_faces):
        count[encoder.inverse_transform([i])[0]] = 0
        present[encoder.inverse_transform([i])[0]] = False
        
    vs = VideoStream(src=0).start()
    sampleNum = 0
    while(True):	
        frame = vs.read()
        frame = imutils.resize(frame ,width = 800)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray_frame,0)
        for face in faces:
            print("INFO : inside for loop")
            (x,y,w,h) = face_utils.rect_to_bb(face)
            face_aligned = fa.align(frame,gray_frame,face)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),1)
            (pred,prob)=predict(face_aligned,svc)
            if(pred!=[-1]):
                person_name=encoder.inverse_transform(np.ravel([pred]))[0]
                pred=person_name
                if count[pred] == 0:
                    start[pred] = time.time()
                    count[pred] = count.get(pred,0) + 1
                if count[pred] == 4 and (time.time()-start[pred]) > 1.5:
                    count[pred] = 0
                else:
                    #if count[pred] == 4 and (time.time()-start) <= 1.5:
                    present[pred] = True
                    log_time[pred] = datetime.datetime.now()
                    count[pred] = count.get(pred,0) + 1
                    print(pred, present[pred], count[pred])
                cv2.putText(frame, str(person_name)+ str(prob), (x+6,y+h-6), cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),1)
            else:
                person_name="unknown"
                cv2.putText(frame, str(person_name), (x+6,y+h-6), cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),1)

			
			
			#cv2.putText()
			# Before continuing to the next loop, I want to give it a little pause
			# waitKey of 100 millisecond
			#cv2.waitKey(50)

		#Showing the image in another window
		#Creates a window with window name "Face" and with the image img
        cv2.imshow("Mark Attendance- Out - Press q to exit",frame)
		#Before closing it we need to give a wait command, otherwise the open cv wont work
		# @params with the millisecond of delay 1
		#cv2.waitKey(1)
		#To get out of the loop
        key=cv2.waitKey(50) & 0xFF
        if(key==ord("q")):
            break
	
	#Stoping the videostrea
    vs.stop()

	# destroying all the windows
    cv2.destroyAllWindows()
    return redirect('home')



#@login_required
def train(request):
	#if request.user.username!='admin':
	#	return redirect('not-authorised')
    
	training_dir=r'C:\Users\DCQUASTER JACK\projects\fras\attds\Face_Recognition_Data\Dataset'

	X=[]
	y=[]
	i=0

	for person_name_i in os.listdir(training_dir):
		print(str(person_name_i))
		curr_directory=os.path.join(training_dir,person_name_i)
		if not os.path.isdir(curr_directory):
			continue
		for imagefile in image_files_in_folder(curr_directory):
			print(str(imagefile))
			image=cv2.imread(imagefile)
			try:
				X.append((face_recognition.face_encodings(image)[0]).tolist())		
				y.append(person_name_i)
				i+=1
			except:
				print("removed")
				os.remove(imagefile)

	targets=np.array(y)
	encoder = LabelEncoder()
	encoder.fit(y)
	y=encoder.transform(y)
	X1=np.array(X)
	print("shape: "+ str(X1.shape))
	np.save(r'C:\Users\DCQUASTER JACK\projects\fras\attds\Face_Recognition_Data\classes.npy', encoder.classes_)
	svc = SVC(kernel='linear',probability=True)
	svc.fit(X1,y)
	svc_save_path=r"C:\Users\DCQUASTER JACK\projects\fras\attds\Face_Recognition_Data\svc.sav"
	with open(svc_save_path, 'wb') as f:
		pickle.dump(svc,f)
	
	#vizualize_Data(X1,targets)
	
	messages.success(request, ('Training Complete'))
    #return redirect("student")
    #messages.success(request, f'Training Complete.')
   
	return redirect("admins")

#train()
#mark_your_attendance()
#visualize()

#for admin page.
def admins(request):
    return render(request,'admin.html')

def gen(camera):
    while True:
        frame = camera.mark_your_attendance(2)
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def facecam_feed(request):
    if request.method=='POST':    
        print("keshabh")
        dataUrlPattern = re.compile('data:image/(png|jpeg);base64,(.*)$')
        ImageData = request.POST['imagedata']
        ImageData = dataUrlPattern.match(ImageData).group(2)
        if ImageData == None or len(ImageData) == 0:
            print("are bhai error hai")
            pass
        ImageData = base64.b64decode(ImageData)
        #_, jpeg = cv2.imencode('.jpg', ImageData)
        img=Image.open(io.BytesIO(ImageData))
        frames=[]
        for i in range(100):
            frames.append(img)
        #img.show()
        #img=np.array(img)

        #for i in range(100):
        #    cv2.imwrite(r'C:\Users\DCQUASTER JACK\projects\fras\attds\Face_Recognition_Data\Output\data'+str(i)+'.jpg', img)
        

        #p = Augmentor.Pipeline(r'C:\Users\DCQUASTER JACK\projects\fras\attds\Face_Recognition_Data\Test')
        #p.zoom(probability = 0.2, min_factor=0.5, max_factor=1.2)
        #p.flip_top_bottom(probability = 0.1)
        #p.random_brightness(probability = 0.7, min_factor=0.7, max_factor=1.2)
        #p.sample(100)




        

        op=[]
        print("abc")
        detector=dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor(r'C:\Users\DCQUASTER JACK\projects\fras\attds\Face_Recognition_Data\shape_predictor_68_face_landmarks.dat')
        #Add path to the shape predictor ######CHANGE TO RELATIVE PATH LATER
        svc_save_path=r"C:\Users\DCQUASTER JACK\projects\fras\attds\Face_Recognition_Data\svc.sav"	
        with open(svc_save_path, 'rb') as f:
            svc = pickle.load(f)
            fa = FaceAligner(predictor , desiredFaceWidth = 96)
            encoder=LabelEncoder()
            encoder.classes_ = np.load(r'C:\Users\DCQUASTER JACK\projects\fras\attds\Face_Recognition_Data\classes.npy')
        
        faces_encodings = np.zeros((1,128))
        no_of_faces = len(svc.predict_proba(faces_encodings)[0])
        count = dict()
        present = dict()
        log_time = dict()
        start = dict()
        for i in range(no_of_faces):
            count[encoder.inverse_transform([i])[0]] = 0
            present[encoder.inverse_transform([i])[0]] = False
        #vs = VideoStream(src=0).start()
        #fps=FPS().start()
        sampleNum = 0
        frames=[]
        #dire=os.path.join(r'C:\Users\DCQUASTER JACK\projects\fras\attds\Face_Recognition_Data\Output')
        #for imagefile in image_files_in_folder(dire):
        #    frames.append(cv2.imread(imagefile))
            
        ind=0
        while(ind<99):	
            #frame = np.array(frames[ind])
            frame = img
            frame = np.array(img)
            frame = imutils.resize(frame ,width = 800)
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = detector(gray_frame,1)
            print("face : ", faces)
            for face in faces:
                print("INFO : inside for loop")
                (x,y,w,h) = face_utils.rect_to_bb(face)
                face_aligned = fa.align(frame,gray_frame,face)
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),1)		
                (pred,prob)=predict(face_aligned,svc)
                if(pred!=[-1]):
                    person_name=encoder.inverse_transform(np.ravel([pred]))[0]
                    pred=person_name
                    if count[pred] == 0:
                        start[pred] = time.time()
                        count[pred] = count.get(pred,0) + 1
                    if count[pred] == 4 and (time.time()-start[pred]) > 1.2:
                        count[pred] = 0 
                    else:
                        #if count[pred] == 4 and (time.time()-start) <= 1.5:
                        present[pred] = True
                        #log_time[pred] = datetime.datetime.now()
                        log_time[pred] =2
                        count[pred] = count.get(pred,0) + 1
                        print(pred, present[pred], count[pred])
                        op.append(pred)
                        cv2.putText(frame, str(person_name)+ str(prob), (x+6,y+h-6), cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),1)
                else:
                    person_name="unknown"
                    cv2.putText(frame, str(person_name), (x+6,y+h-6), cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),1)
            ind+=1

    r"""
        op=[]
        print("abc")
        detector=dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor(r'C:\Users\DCQUASTER JACK\projects\fras\attds\Face_Recognition_Data\shape_predictor_68_face_landmarks.dat')
        #Add path to the shape predictor ######CHANGE TO RELATIVE PATH LATER
        svc_save_path=r"C:\Users\DCQUASTER JACK\projects\fras\attds\Face_Recognition_Data\svc.sav"	
        with open(svc_save_path, 'rb') as f:
            svc = pickle.load(f)
            fa = FaceAligner(predictor , desiredFaceWidth = 96)
            encoder=LabelEncoder()
            encoder.classes_ = np.load(r'C:\Users\DCQUASTER JACK\projects\fras\attds\Face_Recognition_Data\classes.npy')
        
        faces_encodings = np.zeros((1,128))
        no_of_faces = len(svc.predict_proba(faces_encodings)[0])
        count = dict()
        present = dict()
        log_time = dict()
        start = dict()
        for i in range(no_of_faces):
            count[encoder.inverse_transform([i])[0]] = 0
            present[encoder.inverse_transform([i])[0]] = False

        frame = np.array(img)
        frame = imutils.resize(frame ,width = 800)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray_frame,0)
        print(faces)
        for face in faces:
            print("INFO : inside for loop")
            (x,y,w,h) = face_utils.rect_to_bb(face)
            face_aligned = fa.align(frame,gray_frame,face)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),1)
            (pred,prob)=predict(face_aligned,svc)
            if(pred!=[-1]):
                person_name=encoder.inverse_transform(np.ravel([pred]))[0]
                pred=person_name
                if count[pred] == 0:
                    start[pred] = time.time()
                    count[pred] = count.get(pred,0) + 1
                if count[pred] == 4 and (time.time()-start[pred]) > 1.5:
                    count[pred] = 0
                else:
                    #if count[pred] == 4 and (time.time()-start) <= 1.5:
                    present[pred] = True
                    log_time[pred] = datetime.datetime.now()
                    count[pred] = count.get(pred,0) + 1
                    print(pred, present[pred], count[pred])
                cv2.putText(frame, str(person_name)+ str(prob), (x+6,y+h-6), cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),1)
            else:
                person_name="unknown"
                cv2.putText(frame, str(person_name), (x+6,y+h-6), cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),1)

            
        return HttpResponse("<h1>Hello</h1>")
    else:
        return HttpResponse("<h1>World</h1>")




    """





def stdnt(request):
    return render(request,'student_register.html')


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(-1)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@gzip.gzip_page
def livefe(request):
    try:
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:  # This is bad! replace it with proper handling
        pass




def cam(request):
    return render(request,'cam.html')



def video(request,room,created):
    return render(request,'video.html',{'room':room,'created':created})

def demo(request):
    if request.method == 'POST':
        room = request.POST['room']
        get_room = Chat.objects.filter(room_name=room)
        if get_room:
            c = get_room[0]
            number = c.allowed_users
            if int(number) < 2:
                number = 2
                return redirect(f'/video/{room}/join/')
        else:
            create = Chat.objects.create(room_name=room,allowed_users=1)
            if create:
                return redirect(f'/video/{room}/created/')
    return render(request,'demo.html')


