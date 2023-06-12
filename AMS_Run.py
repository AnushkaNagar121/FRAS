import tkinter as tk
from tkinter import *
import cv2
import csv
import os
import csv
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time

# Window is our Main frame of system
window = tk.Tk()
window.title("Face Recognition Attendance System")
window.geometry('1280x720')
window.configure(background='black')
#add='http://10.0.19041.1387/video'


# GUI for manually fill attendance
def manually_fill():
    global sb
    sb = tk.Tk()
    sb.title("Enter subject name...")
    sb.geometry('580x320')
    sb.configure(background='black')


    def err_screen_for_subject():

        def ec_delete():
            ec.destroy()
        global ec
        ec = tk.Tk()
        ec.geometry('300x100')
        ec.title('Warning!!')
        ec.configure(background='snow')
        Label(ec, text='Please enter your subject name!!!', fg='red',bg='white', font=('times', 16, ' bold ')).pack()
        Button(ec, text='OK', command=ec_delete, fg="black", bg="lawn green", width=9, height=1, activebackground="Red",font=('times', 15, ' bold ')).place(x=90, y=50)

    def fill_attendance():
        ts = time.time()                                     
        Date = datetime.datetime.fromtimestamp(ts).strftime('%d_%m_%Y')
        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        Time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        Hour, Minute, Second = timeStamp.split(":")
        # Creatting csv of attendance

        # Create table for Attendance
        global subb
        subb = SUB_ENTRY.get()
        DB_table_name = str(subb + "_" + Date)

        # Connect to the database
        import mysql.connector as connector

        try:
            global cursor
            connection = connector.connect(host='localhost', user='root', password='anushka', db='manually_fill_attendance')
            cursor = connection.cursor()
        except Exception as e:
            print(e)

        sql = "CREATE TABLE "+ DB_table_name + """
                        (
                         ENROLLMENT int NOT NULL,
                         NAME VARCHAR(50) NOT NULL,
                         TIME VARCHAR(20) NOT NULL,
                         PRIMARY KEY (ENROLLMENT)
                        );
                        """

        try:
            cursor.execute(sql)  # for create a table
        except Exception as ex:
            print(ex)  

        if subb == '':
            err_screen_for_subject()
         
        else:
            sb.destroy()
            MFW = tk.Tk()
            MFW.title("Manually attendance of " + str(subb))
            MFW.geometry('880x470')
            MFW.configure(background='black')
        

            def del_errsc2():
                errsc2.destroy()

            def err_screen1():
                global errsc2
                errsc2 = tk.Tk()
                errsc2.geometry('330x100')
                errsc2.title('Warning!!')
                errsc2.configure(background='snow')
                Label(errsc2, text='Please enter Student & Enrollment!!!', fg='black', bg='white',
                      font=('times', 16, ' bold ')).pack()
                Button(errsc2, text='OK', command=del_errsc2, fg="black", bg="lawn green", width=9, height=1,
                       activebackground="Red", font=('times', 15, ' bold ')).place(x=90, y=50)

            def testVal(inStr, acttyp):
                if acttyp == '1':  # insert
                    if not inStr.isdigit():
                        return False
                return True

            ENR = tk.Label(MFW, text="Enter Enrollment", width=15, height=2, fg="black", bg="grey",
                           font=('times', 15))
            ENR.place(x=30, y=100)
            global STU_NAME 
            STU_NAME = tk.Label(MFW, text="Enter Student name", width=15, height=2, fg="black", bg="grey",
                                font=('times', 15))
            STU_NAME.place(x=30, y=200)

            global ENR_ENTRY
            ENR_ENTRY = tk.Entry(MFW, width=20, validate='key',bg="white", fg="black", font=('times', 18))
            ENR_ENTRY['validatecommand'] = (ENR_ENTRY.register(testVal), '%P', '%d')
            ENR_ENTRY.place(x=290, y=105)

            def remove_enr():
                ENR_ENTRY.delete(first=0, last=22)

            STUDENT_ENTRY = tk.Entry(MFW, width=20, bg="white", fg="black", font=('times', 18))
            STUDENT_ENTRY.place(x=290, y=205)

            def remove_student():
                STUDENT_ENTRY.delete(first=0, last=22)

            # get important variable
            def enter_data_DB():
                ENROLLMENT = ENR_ENTRY.get()
                STUDENT = STUDENT_ENTRY.get()
                if ENROLLMENT == '':
                    err_screen1()
                elif STUDENT == '':
                    err_screen1()
                else:
                    time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    Hour, Minute, Second = time.split(":")
                    Insert_data = "INSERT INTO " + DB_table_name + \
                        " (ENROLLMENT,NAME,TIME) VALUES ( %s , %s , %s )"
                    VALUES = (str(ENROLLMENT),str(STUDENT),str(time))
                    try:
                        cursor.execute(Insert_data, VALUES)
                    except Exception as e:
                        print(e)
                        f = 'Student Data already exists'
                        Notifi.configure(text=f, bg="Red", width=21)
                        Notifi.place(x=450, y=400)
                        MFW.destroy()
 
                    ENR_ENTRY.delete(first=0, last=22)
                    STUDENT_ENTRY.delete(first=0, last=22)

            def create_csv():
                import csv
                try:
                  cursor.execute("select * from " + DB_table_name + ";")
                  csv_name ='Attendance/Manually Attendance/'+DB_table_name+'.csv'
                  with open(csv_name, "w") as csv_File:
                    csv_writer = csv.writer(csv_File)
                    csv_writer.writerow([i[0] for i in cursor.description])  # write headers
                    csv_writer.writerows(cursor)
                    O = "CSV created Successfully"
                    Notifi.configure(text=O, bg="Green", fg="white", width=33, font=('times', 18, 'bold'))
                    Notifi.place(x=180, y=380)
                except Exception as e:
                    print(e)
                    f = 'Already Exists'
                    Notifi.configure(text=f, bg="Red", width=21)
                    Notifi.place(x=450, y=400)  
                import csv
                import tkinter
                root = tkinter.Tk()
                root.title("Attendance of " + subb)
                root.configure(background='black')
                    
                with open(csv_name, newline="") as file:
                    reader = csv.reader(file)
                    r = 0
                    for col in reader:
                        c = 0
                        for row in col:
                            # i've added some styling
                            label = tkinter.Label(root, width=18, height=1, fg="black", font=('times', 13, ' bold '),
                                                  bg="white", text=row, relief=tkinter.RIDGE)
                            label.grid(row=r, column=c)
                            c += 1
                        r += 1
                root.mainloop()

            Notifi = tk.Label(MFW, text="CSV created Successfully", bg="Green", fg="white", width=33,
                              height=2, font=('times', 19, 'bold'))

            c1ear_enroll = tk.Button(MFW, text="Clear", command=remove_enr, fg="white", bg="black", width=10,
                                     height=1,
                                     activebackground="white", font=('times', 15, ' bold '))
            c1ear_enroll.place(x=690, y=100)

            c1ear_student = tk.Button(MFW, text="Clear", command=remove_student, fg="white", bg="black", width=10,
                                      height=1,
                                      activebackground="white", font=('times', 15, ' bold '))
            c1ear_student.place(x=690, y=200)

            DATA_SUB = tk.Button(MFW, text="Enter Data", command=enter_data_DB, fg="black", bg="orange1", width=20,
                                 height=2,
                                 activebackground="white", font=('times', 15, ' bold '))
            DATA_SUB.place(x=170, y=300)

            MAKE_CSV = tk.Button(MFW, text="Convert to CSV", command=create_csv, fg="black", bg="orange1", width=20,
                                 height=2,
                                 activebackground="white", font=('times', 15, ' bold '))
            MAKE_CSV.place(x=570, y=300)

            MFW.mainloop()

    SUB = tk.Label(sb, text="Enter Subject : ", width=15, height=2,fg="black", bg="orange1", font=('times', 15, ' bold '))
    SUB.place(x=30, y=100)

    global SUB_ENTRY
    SUB_ENTRY = tk.Entry(sb, width=20, bg="white",fg="black", font=('times', 23))
    SUB_ENTRY.place(x=250, y=105)

    fill_manual_attendance = tk.Button(sb, text="Fill Attendance", command=fill_attendance, fg="black", bg="orange1", width=20, height=2,activebackground="white", font=('times', 15, ' bold '))
    fill_manual_attendance.place(x=250, y=160)
    sb.mainloop()

# For clear textbox


def clear():
    txt.delete(first=0, last=22)


def clear1():
    txt2.delete(first=0, last=22)


def del_sc1():
    sc1.destroy()


def err_screen():
    global sc1
    sc1 = tk.Tk()
    sc1.geometry('300x100')
    sc1.title('Warning!!')
    sc1.configure(background='black')
    Label(sc1, text='Enrollment & Name required!!!', fg='black',
          bg='white', font=('times', 16)).pack()
    Button(sc1, text='OK', command=del_sc1, fg="black", bg="orange", width=9,
           height=1, activebackground="Red", font=('times', 15, ' bold ')).place(x=90, y=70)

# Error screen2


def del_sc2():
    sc2.destroy()


def err_screen1():
    global sc2
    sc2 = tk.Tk()
    sc2.geometry('300x100')
    sc2.title('Warning!!')
    sc2.configure(background='black')
    Label(sc2, text='Please enter your subject name!!!', fg='black',bg='white', font=('times', 16)).pack()
    Button(sc2, text='OK', command=del_sc2, fg="black", bg="lawn green", width=9,height=1, activebackground="Red", font=('times', 15, ' bold ')).place(x=90, y=50)

# For take images for datasets

def take_img():
    l1 = txt.get()
    l2 = txt2.get()
    if l1 == '':
        err_screen()
    elif l2 == '':
        err_screen()
    else:
        try:
            
            cam = cv2.VideoCapture(0)
            #cam.open(add)
            detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            Enrollment = txt.get()
            Name = txt2.get()
            sampleNum = 0
            while (True):
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    # incrementing sample number
                    sampleNum = sampleNum + 1
                    # saving the captured face in the dataset folder
                    cv2.imwrite("TrainingImage/ " + Name + "." + Enrollment + '.' + str(sampleNum) + ".jpg",
                                gray[y:y+h ,x: x+w])
                    print("Images Saved for Enrollment :")
                    cv2.imshow('Frame', img)
                # wait for 100 miliseconds
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                
                # # break if the sample number is more than 200
                elif sampleNum > 200:
                    break

            cam.release()
            cv2.destroyAllWindows()

            ts = time.time()
            Date = datetime.datetime.fromtimestamp(ts).strftime('%d_%m_%Y')
            Time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            header =["ENROLLMENT","NAME","TIME"]
            row = [Enrollment,Name,Time ]
            with open('Details/StudentDetails.csv', 'a+') as csvFile:
                writer = csv.writer(csvFile, delimiter=',')
                writer.writerow(header)
                writer.writerow(row)
                csvFile.close()
            res = "Images Saved for Enrollment : " + Enrollment + " Name : " + Name
            Notification.configure(text=res, bg="SpringGreen3", width=50, font=('times', 18, 'bold'))
            Notification.place(x=250, y=400)
        except FileExistsError as F:
            f= 'Student Data already exists'
            Notification.configure(text=f, bg="Red", width=21)
            Notification.place(x=450, y=400)

# for choose subject and fill attendance
def subjectchoose():
    def Fillattendances():
        sub = tx.get()
        now = time.time()  # For calculate seconds of video
        future = now + 20
        if time.time() < future:
            if sub == '':
                err_screen1()
            else:
                recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()

                try:
                    recognizer.read("TrainingImageLabel"+os.sep+"Trainner.yml")
    
                except:
                    e = 'Model not found,Please train model'
                    Notifica.configure(text=e, bg="red", fg="black", width=33, font=('times', 15, 'bold'))
                    Notifica.place(x=20, y=250)
                
                harcascadePath = "haarcascade_frontalface_default.xml"
                faceCascade = cv2.CascadeClassifier(harcascadePath)
                
                df = pd.read_csv("Details"+ os.sep +"StudentDetails.csv")
                # Initialize and start realtime video capture
                cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
                #cam.open(add)
                cam.set(3, 640)  # set video width
                cam.set(4, 480)  # set video height
                # Define min window size to be recognized as a face
                minW = 0.1 * cam.get(3)
                minH = 0.1 * cam.get(4)

                font = cv2.FONT_HERSHEY_SIMPLEX
                col_names = ['ENROLLMENT', 'NAME', 'TIME']
                attendance = pd.DataFrame(columns=col_names)

                while True:
                    ret, im = cam.read()
                    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                    faces = faceCascade.detectMultiScale(gray, 1.2, 5,minSize = (int(minW), int(minH)),flags = cv2.CASCADE_SCALE_IMAGE)
                    for (x, y, w, h) in faces:
                        #global Id
                        Id, conf = recognizer.predict(gray[y:y + h, x:x + w])
                        if (conf < 100):

                            aa = df.loc[df['ENROLLMENT'] == Id]['NAME'].values
                            confstr = "  {0}%".format(round(100 - conf))
                            tt = str(Id)+"-"+aa

                        else:
                           Id = 'Unknown'
                           tt = str(Id)
                           confstr = "  {0}%".format(round(100 - conf))

                        if (100-conf) > 67:
                           ts = time.time()
                           date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                           timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                           aa = str(aa)[2:-2]
                           attendance.loc[len(attendance)] = [Id, aa, timeStamp]

                        tt = str(tt)[2:-2]
                        if(100-conf) > 67:
                           tt = tt + " [Pass]"
                           cv2.putText(im, str(tt), (x+5,y-5), font, 1, (255, 255, 255), 2)
                        else:
                           cv2.putText(im, str(tt), (x + 5, y - 5), font, 1, (255, 255, 255), 2)

                        if (100-conf) > 50:
                           cv2.putText(im, str(confstr), (x + 5, y + h - 5), font,1, (0, 255, 0),1 )
                        elif (100-conf) > 50:
                           cv2.putText(im, str(confstr), (x + 5, y + h - 5), font, 1, (0, 255, 255), 1)
                        else:
                           cv2.putText(im, str(confstr), (x + 5, y + h - 5), font, 1, (0, 0, 255), 1)

                    if time.time() > future:
                        break

                    attendance = attendance.drop_duplicates(['ENROLLMENT'], keep='first')
                    cv2.imshow('Filling attedance..', im)
                    key = cv2.waitKey(30) & 0xff
                    if key == 27:
                        break

                ts = time.time()
                Subject = tx.get()
                date = datetime.datetime.fromtimestamp(ts).strftime('%d_%m_%Y')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                Hour, Minute, Second = timeStamp.split(":")
                fileName = "Attendance/" + Subject + "_" + date +".csv"
                attendance = attendance.drop_duplicates(['ENROLLMENT'], keep='first')
                print(attendance)
                attendance.to_csv(fileName, index=False)


                # Create table for Attendance
                DB_Table_name = str(Subject + "_" + date)
               
                
                import mysql.connector as connector

                # Connect to the database
                try:
                    global cursor
                    connection = connector.connect(host='localhost', user='root', password='anushka', db='face_recog_fill')
                    cursor = connection.cursor()
                except Exception as e:
                    print(e)

                
                sql = "CREATE TABLE " + DB_Table_name + """
                (
                 ENROLLMENT int NOT NULL,
                 NAME VARCHAR(50) NOT NULL,
                 TIME VARCHAR(20) NOT NULL,
                 PRIMARY KEY (ENROLLMENT)
                     );
                """
                # Now enter attendance in Database
                insert_data = "INSERT INTO " + DB_Table_name + " (ENROLLMENT,NAME,TIME) VALUES (%s,%s,%s)"
                VALUES = (str(Id),str(aa), str(timeStamp))
                try:
                    cursor.execute(sql)  # for create a table
                    # For insert data into table
                    cursor.execute(insert_data, VALUES)
                except Exception as ex:
                    print(ex)  
                
                M = 'Attendance filled Successfully'
                Notifica.configure(text=M, bg="Green", fg="white",width=33, font=('times', 15, 'bold'))
                Notifica.place(x=20, y=250)

                cam.release()
                cv2.destroyAllWindows()

                import csv
                import tkinter
                root = tkinter.Tk()
                root.title("Attendance of " + Subject)
                root.configure(background='black')
                cs =fileName
                with open(cs, newline="") as file:
                    reader = csv.reader(file)
                    r = 0
                    for col in reader:
                        c = 0
                        for row in col:
                            # i've added some styling
                            label = tkinter.Label(root, width=14, height=1, fg="black", font=('times', 15, ' bold '),
                                                  bg="white", text=row, relief=tkinter.RIDGE)
                            label.grid(row=r, column=c)
                            c += 1
                        r += 1
                root.mainloop()
                print(attendance)

    # windo is frame for subject chooser
    windo = tk.Tk()
    windo.title("Enter subject name...")
    windo.geometry('580x320')
    windo.configure(background='black')
    Notifica = tk.Label(windo, text="Attendance filled Successfully", bg="Green", fg="white", width=33,
                        height=2, font=('times', 15, 'bold'))


    sub = tk.Label(windo, text="Enter Subject : ", width=15, height=2,fg="black", bg="grey", font=('times', 15, ' bold '))
    sub.place(x=30, y=100)

    tx = tk.Entry(windo, width=20, bg="white",fg="black", font=('times', 23))
    tx.place(x=250, y=105)
    
    fill_a = tk.Button(windo, text="Fill Attendance", fg="white", command=Fillattendances, bg="orange", width=20, height=2,activebackground="white", font=('times', 15, ' bold '))
    fill_a.place(x=250, y=160)

    windo.mainloop()

def admin_panel2():
    win = tk.Tk()
 
    win.title("Attendance Status")
    win.geometry('880x420')
    win.configure(background='black')
    
    def Attf():
        username = un_entr.get()
        password = pw_entr.get()
        if   username =='':  
            valid4 = 'Please enter the Username'
            Nt.configure(text=valid4, bg="pink", fg="black",width=38, font=('times', 19, 'bold'))
            Nt.place(x=120, y=350)

        elif username == 'anushka':
            if   password =='':  
                valid3 = 'Please enter the Password'
                Nt.configure(text=valid3, bg="pink", fg="black",width=38, font=('times', 19, 'bold'))
                Nt.place(x=120, y=350)
             
            elif password == 'anushka123':
                win.destroy()
                import subprocess
                subprocess.Popen(
                r'explorer /select,"C:\Users\Asus\Desktop\FRAS SYSTEM\Face-Recognition-Attendance-System-main\Attendance\-------Check atttendance-------"')
            else:    
              valid2 = 'Incorrect Password'
              Nt.configure(text=valid2, bg="red", fg="white",width=38, font=('times', 19, 'bold'))
              Nt.place(x=120, y=350)
        else:
            valid3 = 'Incorrect Username'
            Nt.configure(text=valid3, bg="red", fg="white",width=38, font=('times', 19, 'bold'))
            Nt.place(x=120, y=350)


    Nt = tk.Label(win ,bg="black", fg="white", width=40,height=2, font=('times', 19, 'bold'))
    Nt.place(x=120, y=350)

    un = tk.Label(win, text="Enter username : ", width=15, height=2, fg="black", bg="grey",font=('times', 15, ' bold '))
    un.place(x=30, y=50)

    pw = tk.Label(win, text="Enter password : ", width=15, height=2, fg="black", bg="grey",font=('times', 15, ' bold '))
    pw.place(x=30, y=150)

    def c00():
        un_entr.delete(first=0, last=22)

    un_entr = tk.Entry(win, width=20, bg="white", fg="black",font=('times', 23))
    un_entr.place(x=290, y=55)

    def c11():
        pw_entr.delete(first=0, last=22)

    pw_entr = tk.Entry(win, width=20, show="*", bg="white",fg="black", font=('times', 23))
    pw_entr.place(x=290, y=155)

    c0 = tk.Button(win, text="Clear", command=c00, fg="white", bg="black", width=10, height=1,
                   activebackground="white", font=('times', 15, ' bold '))
    c0.place(x=690, y=55)

    c1 = tk.Button(win, text="Clear", command=c11, fg="white", bg="black", width=10, height=1,
                   activebackground="white", font=('times', 15, ' bold '))
    c1.place(x=690, y=155)

    Status1 = tk.Button(win, text="Check Sheet", fg="black", bg="orange1", width=45 , height=1,
                      activebackground="Red", command=Attf, font=('times', 25, ' bold '))
    Status1.place(x=20, y=260)
    
    win.mainloop()


def admin_panel():
    win = tk.Tk()
 
    win.title("Student detail")
    win.geometry('880x420')
    win.configure(background='black')
    
    def log_in():
        username = un_entr.get()
        password = pw_entr.get()

        if   username =='':  
            valid4 = 'Please enter the Username'
            Nt.configure(text=valid4, bg="pink", fg="white",width=38, font=('times', 19, 'bold'))
            Nt.place(x=120, y=350)

        elif username == 'anushka':
            if   password =='':  
                valid3 = 'Please enter the Password'
                Nt.configure(text=valid3, bg="pink", fg="white",width=38, font=('times', 19, 'bold'))
                Nt.place(x=120, y=350)
            elif password == 'anushka123':
                win.destroy()

                import csv
                import tkinter
                root = tkinter.Tk()
                root.title("Student Details")
                root.configure(background='black')
                
                cs = "Details"+ os.sep +'StudentDetails.csv'
                with open(cs, newline="") as file:
                    reader = csv.reader(file)
                    r = 0

                    for col in reader:
                        c = 0
                        for row in col:
                            # i've added some styling
                            label = tkinter.Label(root, width=14, height=1, fg="black", font=('times', 15, ' bold '),
                                                  bg="white", text=row, relief=tkinter.RIDGE)
                            label.grid(row=r, column=c)
                            c += 1
                        r += 1
                root.mainloop()
            
            else:    
              valid2 = 'Incorrect Password'
              Nt.configure(text=valid2, bg="red", fg="white",width=38, font=('times', 19, 'bold'))
              Nt.place(x=120, y=350)
        
        else:
            valid3 = 'Incorrect Username'
            Nt.configure(text=valid3, bg="red", fg="white",width=38, font=('times', 19, 'bold'))
            Nt.place(x=120, y=350)

    Nt = tk.Label(win,bg="black", fg="white", width=40,height=2, font=('times', 19, 'bold'))
    Nt.place(x=120, y=350)

    un = tk.Label(win, text="Enter username : ", width=15, height=2, fg="black", bg="grey",font=('times', 15, ' bold '))
    un.place(x=30, y=50)

    pw = tk.Label(win, text="Enter password : ", width=15, height=2, fg="black", bg="grey",font=('times', 15, ' bold '))
    pw.place(x=30, y=150)

    def c00():
        un_entr.delete(first=0, last=22)

    un_entr = tk.Entry(win, width=20, bg="white", fg="black",font=('times', 23))
    un_entr.place(x=290, y=55)

    def c11():
        pw_entr.delete(first=0, last=22)

    pw_entr = tk.Entry(win, width=20, show="*", bg="white",fg="black", font=('times', 23))
    pw_entr.place(x=290, y=155)

    c0 = tk.Button(win, text="Clear", command=c00, fg="white", bg="black", width=10, height=1,
                   activebackground="white", font=('times', 15, ' bold '))
    c0.place(x=690, y=55)

    c1 = tk.Button(win, text="Clear", command=c11, fg="white", bg="black", width=10, height=1,
                   activebackground="white", font=('times', 15, ' bold '))
    c1.place(x=690, y=155)

    Login = tk.Button(win, text="Log In", fg="black", bg="orange1", width=45,
                      height=2,
                      activebackground="Red", command=log_in, font=('times', 25, ' bold '))
    Login.place(x=20, y=260)

    win.mainloop()

# For train the model
def trainimg():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    global detector
    detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    try:
        global faces, Id
        faces, Id = getImagesAndLabels("TrainingImage")
    except Exception as e:
        l = 'please make "TrainingImage" folder & put Images'
        Notification.configure(text=l, bg="SpringGreen3",width=50, font=('times', 18, 'bold'))
        Notification.place(x=350, y=400)

    recognizer.train(faces, np.array(Id))
    try:
        recognizer.save(r"TrainingImageLabel\Trainner.yml")
    except Exception as e:
        q = 'Please make "TrainingImageLabel" folder'
        Notification.configure(text=q, bg="SpringGreen3",width=50, font=('times', 18, 'bold'))
        Notification.place(x=350, y=400)

    res = "Model Trained"  # +",".join(str(f) for f in Id)
    Notification.configure(text=res, bg="olive drab",width=50, font=('times', 18, 'bold'))
    Notification.place(x=250, y=400)


def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # create empth face list
    faceSamples = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8')
        # getting the Id from the image

        Id = int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces = detector.detectMultiScale(imageNp)
        # If a face is there then append that in the list as well as Id of it
        for (x, y, w, h) in faces:
            faceSamples.append(imageNp[y:y + h, x:x + w])
            Ids.append(Id)
    return faceSamples, Ids


window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)



def on_closing():
    from tkinter import messagebox
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        window.destroy()


window.protocol("WM_DELETE_WINDOW", on_closing)

message = tk.Label(window, text="FACE  RECOGNITION  ATTENDANCE  SYSTEM ", bg="black", fg="orange", width=44,
                   height=3, font=('times', 38, ' bold '))

message.place(x=0, y=20)

Notification = tk.Label(window, text="All things good", bg="Green", fg="white", width=15,height=3, font=('times', 17))

lbl = tk.Label(window, text="ENTER  ENROLLMENT: ", width=20, height=3,fg="white", bg="black", font=('times', 18, 'bold'))
lbl.place(x=200, y=200)


def testVal(inStr, acttyp):
    if acttyp == '1':  # insert
        if not inStr.isdigit():
            return False
    return True


txt = tk.Entry(window, validate="key", width=20, bg="white",fg="black", font=('times', 25))
txt['validatecommand'] = (txt.register(testVal), '%P', '%d')
txt.place(x=550, y=210)

lbl2 = tk.Label(window, text="ENTER  NAME: ", width=20, fg="white",bg="black", height=3, font=('times', 18, ' bold '))
lbl2.place(x=200, y=300)

txt2 = tk.Entry(window, width=20, bg="white",fg="black", font=('times', 25))
txt2.place(x=550, y=310)

clearButton = tk.Button(window, text="CLEAR", command=clear, fg="white", bg="black",
                        width=10, height=2, activebackground="white", font=('times', 16, ' bold '))
clearButton.place(x=950, y=210)

clearButton1 = tk.Button(window, text="CLEAR", command=clear1, fg="white", bg="black",
                         width=10, height=2, activebackground="white", font=('times', 16, ' bold '))
clearButton1.place(x=950, y=310)

AP = tk.Button(window, text="REGISTERED STUDENTS", command=admin_panel, fg="black",
               bg="orange1", width=27, height=2, activebackground="white", font=('times', 16, ' bold '))
AP.place(x=940, y=615)


AS = tk.Button(window, text="ATTENDANCE STATUS", command=admin_panel2, fg="black",
               bg="orange1", width=48, height=2, activebackground="white", font=('times', 16, ' bold '))
AS.place(x=320, y=615)

Q = tk.Button(window, text=" QUIT ", command=on_closing, fg="black",
               bg="orange1", width=20, height=2, activebackground="white", font=('times', 16, ' bold '))
Q.place(x=50, y=615)


takeImg = tk.Button(window, text="TAKE  IMAGES", command=take_img, fg="black", bg="orange1",
                    width=20, height=3, activebackground="white", font=('times', 16, ' bold '))
takeImg.place(x=50, y=500)    

trainImg = tk.Button(window, text="TRAIN  IMAGES", fg="black", command=trainimg, bg="orange1",
                     width=20, height=3, activebackground="white", font=('times', 16, ' bold '))
trainImg.place(x=320, y=500) 

FA = tk.Button(window, text="AUTOMATIC  ATTENDANCE", fg="black", command=subjectchoose,
               bg="orange1", width=25, height=3, activebackground="white", font=('times', 16, ' bold '))
FA.place(x=600, y=500)

quitWindow = tk.Button(window, text="MANUALLY  FILL  ATTENDANCE", command=manually_fill, fg="black",
                       bg="orange1", width=27, height=3, activebackground="white", font=('times', 16, ' bold '))
quitWindow.place(x=940, y=500)

window.mainloop()