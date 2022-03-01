# Mini-Project  
**DATAFLOW**  
<img width="902" alt="image" src="https://user-images.githubusercontent.com/55504424/151784749-89627cca-609e-4421-bfc9-32c72b51537c.png">   
**HOMEPAGE**  
<img width="629" alt="image" src="https://user-images.githubusercontent.com/55504424/151784840-eecf5a52-3f9a-437f-8414-8481386f3e85.png">  
**TEACHERS LOGIN PAGE**  
<img width="629" alt="image" src="https://user-images.githubusercontent.com/55504424/152151476-670f3c95-8209-4203-bd81-25c619af4f0d.png">  
**sTUDENTS SESSION PAGE**  
<img width="518" alt="image" src="https://user-images.githubusercontent.com/55504424/152150193-98712090-43c6-4672-9275-20528e91e597.png">  
**TEACHER SESSION CREATING PAGE**
<img width="866" alt="image" src="https://user-images.githubusercontent.com/55504424/152643788-4f01b1bc-71dc-47bc-809a-da47be1d9283.png">   
**AFTER CREATE BUTTON IS PRESSED**
<img width="960" alt="image" src="https://user-images.githubusercontent.com/55504424/152643843-f8d703fa-5e2f-4b03-b91f-8c3397ca850c.png">   





## DESCRIPTION
1. 1st page will have 2 buttons , 1 for student and other for teacher.   
2. If student button is pressed, it will take us to a session page( A session page will have multiple sessions started by multiple teachers).  
  2a. In the session page, we will select the session of our teacher, then it will ask us to enter our registration number.  
  2b. If the resgistration number is correct, then it will allow us to the anoter page.  
  2c. In this new page, we will have options to open camera and take picture, once the pciture is clicked by the student, the system will notify the user  
     Messages from the server could be:   
     a) Attendance Taken for {{Student Name}}.  
     b) Invalid Picture, take the picture again.  
     c) No such user in the database.  
3. if teacher button is pressed, then it will ask teacher to enter their pass key/ password.  
4. if the password is correct, it will take teache to new page.  
5. this new page, will have multiple options for teacher:  
   a) To create a session( Input: Session name, session time;  Ouput: session created).  
      The session created by the teacher will expire after the alloted time by the teacher.  
      The created session can be modified and deleted by the teacher.  
   b) To upload the xslx file of students registration number.( stuents with these registration number will only be allowed to open the session of specific teacher).  
   c) A teacher might take multiple classes, so teache can upload multiple xlsx file. And when session is created, teacher will have option to allow only students from only one of the uploaded xlsx file from mulitple xlsx files.  
   d)After the session time is over, teacher will see the download option for the session, it will donwload the attendance of students.  
   e)There will be a option for techer to rename the file name of xlsx file. By default file name will be current date and session name.  
   f)Everytime new session is created by teacher, it will modify the same xlsx file by deleting all previous content and moifying it with new content.  

### NOTE:
1. Students can only login to the specific session , if the teacher has uploaded the xlsx file with the registration numbers of students.( so that no other students from other class can login for the session).  
2. The passkey/password for the teacaher's account will be provided by the Admin, which can be modified upon teacher's request.   
3. while creating session, session time will be set for any date and time( i.e it can be live or scheduled).   
4. By default, session data will be set to today's date(date when teacher is creating session), and default session start time will be current  time and session end time will be current time + 30 minutes.  
5. On Students session page, all the classes will be shown whether live or schedules,  
   Live class will be provided red live indicator and end time will be mentioned for each session ( Ex: This session will expire in 30 min(it will be a running time) or we will show the exact session expire time Ex:" This session will expire at 2:30 pm").
   Out of both live and schedules session links, live will be active while scheduled will be disabled.
   Scheduled button will be disabled(It wont work when pressed, it will only work when its session time matches with the current time). In this we will show session time for which it will be valid or active.   
6. The sessions in student page will be shown in sorted order of date and time.
7. The sessions will be either shown in tabular format or box format.
8. Session name once put by teacher will become permanent and will be shown as an input every next time, teacher puts the name( so that teacher just once have to create sessio name, and that session name will be used as default name everytime.)    
9. Every new session name input will be stored in the database and will be shown as dropown while entering the session name by teacher.  
10. Teacher will have options to edit and delete the created sessions.  

11. Data to be shown in student session page:   
     1) Live   
     2) Session name :either( subject code or subject name) or both, and section(it is must)    
     3) Teacher name(who created the session).   
     4) Running time or time left in live sessions.  
     5) Start time(could be date+time) will be shown in the scheduled one.( At what time ,this session will be live).   
   
      
