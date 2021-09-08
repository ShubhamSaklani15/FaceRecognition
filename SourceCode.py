import tkinter as tk
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import mysql.connector
from PIL import Image, ImageTk
from time import strftime


def takeattendance(btn):
    tablename=btn["text"]
    path = 'Image_Dataset'
    images = []
    classNames = []
    myList = os.listdir(path)
    print(myList)

    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
    print(classNames)

    def findEncodings(images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList

    def markAttendance(name):
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="FaceRecog"
        )
        cursor = db.cursor()
        now = datetime.now()
        sql = """INSERT INTO {}(Name,Time) VALUES (%s, %s) """.format(tablename)
        record = (name, now)

        try:
            cursor.execute(sql, record)
            db.commit()
        except:
            db.rollback()

        db.close()

    encodeListKnown = findEncodings(images)
    print('Encoding Complete')

    cap = cv2.VideoCapture(0)
    flag = "false"
    while True:
        success, img = cap.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                # markAttendance(name)
                NAME = name

                for nam in classNames:
                    if NAME == nam.upper():
                        flag = 'true'

        cv2.imshow('Webcam', img)
        if (cv2.waitKey(700) and flag == 'true'):
            break

    markAttendance(NAME)
    print("Record has been Succesfully Stored")

#***************************************************************************************************************************************

class HOME(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        load = Image.open("bg.png")
        photo = ImageTk.PhotoImage(load)
        label = tk.Label(self, image=photo)
        label.image = photo
        label.place(x=0, y=0)

        #time
        def time():
            string = strftime('%H:%M:%S %p')
            lbl.config(text=string)
            lbl.after(1000, time)
        lbl = tk.Label(self, font=('verdana', 35),
                    background='black',
                    foreground='white')
        lbl.place(relx=0.14, rely=0.27, anchor='center')
        time()

        #date
        now = datetime.now().date()
        date_time = now.strftime("%m/%d/%Y")
        date = "DATE:  " + date_time

        text = tk.Label(label, text=date, fg="white", bg="black", font=("Verdana", 28, "bold"))
        text.place(x=80, y=40)

        button1 = tk.Button(label, text="ATTENDANCE", font=("Verdana",15,'bold'), bg="GREEN", fg="WHITE", bd=5, height=1, width=11,
                         command = lambda : controller.show_frame(SUBJECTS))
        button1.place(x=160, y=230)

        button2 = tk.Button(label, text="CLOSE", font=("Verdana",15,'bold'), bg="RED", fg="WHITE", bd=5, height=1, width=11,
                         command = label.destroy)
        button2.place(x=160, y=330)


class SUBJECTS(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        load = Image.open("bg.png")
        photo = ImageTk.PhotoImage(load)
        label = tk.Label(self, image=photo)
        label.image = photo
        label.place(x=0, y=0)
        # time
        def time():
            string = strftime('%H:%M:%S %p')
            lbl.config(text=string)
            lbl.after(1000, time)

        lbl = tk.Label(self, font=('verdana', 35),
                       background='black',
                       foreground='white')
        lbl.place(relx=0.14, rely=0.23, anchor='center')
        time()
        # date
        now = datetime.now().date()
        date_time = now.strftime("%m/%d/%Y")
        date = "DATE:  " + date_time

        text = tk.Label(label, text=date, fg="white", bg="black", font=("Verdana", 28, "bold"))
        text.place(x=80, y=20)

        button1 = tk.Button(label, text="SUBJECT_1", font=("Verdana",15,'bold'), bg="GREEN", fg="WHITE", bd=5, height=1, width=11,
                            command=lambda:takeattendance(button1))
        button1.place(x=80, y=180)

        button2= tk.Button(label, text="SUBJECT_2", font=("Verdana",15,'bold'), bg="GREEN", fg="WHITE", bd=5, height=1, width=11,
                            command=lambda:takeattendance(button2))
        button2.place(x=300, y=180)

        button3 = tk.Button(label, text="SUBJECT_3", font=("Verdana", 15, 'bold'), bg="GREEN", fg="WHITE", bd=5, height=1,
                            width=11,
                            command=lambda:takeattendance(button3))
        button3.place(x=80, y=250)

        button4 = tk.Button(label, text="SUBJECT_4", font=("Verdana", 15, 'bold'), bg="GREEN", fg="WHITE", bd=5, height=1,
                            width=11,
                            command=lambda:takeattendance(button4))
        button4.place(x=300, y=250)

        button5 = tk.Button(label, text="SUBJECT_5", font=("Verdana", 15, 'bold'), bg="GREEN", fg="WHITE", bd=5,
                            height=1,
                            width=11,
                            command=lambda:takeattendance(button5))
        button5.place(x=80, y=320)

        button6 = tk.Button(label, text="BACK", font=("Verdana", 15, 'bold'), bg="RED", fg="white", bd=5,
                            height=1,
                            width=11,
                            command=lambda: controller.show_frame(HOME))
        button6.place(x=300, y=320)


class TIME(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        load = Image.open("bg.png")
        photo = ImageTk.PhotoImage(load)
        label = tk.Label(self, image=photo)
        label.image = photo
        label.place(x=0, y=0)

        def time():
            string = strftime('%H:%M:%S %p')
            lbl.config(text=string)
            lbl.after(1000, time)

        lbl = tk.Label(self, font=('verdana', 40, 'bold'),
                    background='black',
                    foreground='white')
        lbl.place(relx=0.36, rely=0.2, anchor='center')
        time()


        button3 = tk.Button(label, text="BACK", font=("Verdana",15,'bold'), bg="Black", fg="white", bd=5, height=1, width=11,
                            command=lambda: controller.show_frame(HOME))
        button3.place(x=490, y=230)

        button4 = tk.Button(label, text="CLOSE", font=("Verdana",15,'bold'), bg="Black", fg="white", bd=5, height=1, width=11,
                            command=label.destroy)
        button4.place(x=750, y=230)

class CALCULATE(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        load = Image.open("bg.png")
        photo = ImageTk.PhotoImage(load)
        label = tk.Label(self, image=photo)
        label.image = photo
        label.place(x=0, y=0)
        def text():
            inputtxt = tk.Text(self,background="black",font=('verdana', 8, 'bold'),fg="white",height=5,width=120)
            inputtxt.pack(anchor='center')

        button1 = tk.Button(label, text="TYPE", font=("Verdana",15,'bold'), bg="Black", fg="white", bd=5, height=1, width=11,
                            command=text())
        button1.place(x=490, y=230)

        button2 = tk.Button(label, text="SPEAK", font=("Verdana",15,'bold'), bg="Black", fg="white", bd=5, height=1, width=11,
                            command=label.destroy)
        button2.place(x=750, y=230)


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        window = tk.Frame(self)
        window.pack()

        window.grid_rowconfigure(0, minsize=500)
        window.grid_columnconfigure(0, minsize=2000)

        self.frames = {}
        for F in (HOME, SUBJECTS, TIME,CALCULATE):
            frame = F(window, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HOME)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()
        self.title("ATTENDANCE")


app = Application()
app.maxsize(1000, 435)
app.mainloop()