import os
import pickle

import numpy as np
from PIL import Image, ImageTk
from tkinter import *
from tkinter import ttk
import PIL.Image
import PIL.ImageTk
import PIL.ImageOps
from tkinter import messagebox
import mysql.connector
import cv2
from datetime import datetime
from time import strftime
from database_str import Database_str
import sys

value_from_home = None# chứa id giảng viên truyền từ form main_upd.py
def new_tcid(value):#hàm lấy thông tin id giáo viên khi đăng nhập vào form main_upd.py
    global value_from_home
    value_from_home = value



class Face_Recognition:
    # panel=None
    # camara=cv2.VideoCapture(0)
    # btnOpen=None
    # btnClose = None
    #
    # check=1
    # camara.set(3, 800) ##chiều dài
    # camara.set(4, 580)  ##chiều rộng
    # camara.set(10, 150)
    def __init__(self,root):
        w = 1350  # chiều dài giao diện
        h = 700  # chiều rộng giao diện
        self.root = root
        ws = self.root.winfo_screenwidth()  # độ dài màn hình
        hs = self.root.winfo_screenheight()  # độ rộng màn
        x = (ws / 2) - (w / 2)  # vị trí cách lề trái x px
        y = (hs / 2) - (h / 2)  # vị trí cách lề trên y px

        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))  # kích thước và vị trí hiển thị giao diện
        self.root.title("Điểm danh học sinh")  # tiêu đề
        self.root.iconbitmap('ImageFaceDetect\\gaming.ico')  # icon giao diện
        self.isClicked=False  #biến islicked=false để đóng mở camera, khi cam mở isClicked=true;
        self.teacherid = None #biến id giáo viên

        img3 = PIL.Image.open(r"ImageFaceDetect\bg1.png")#ảnh nền
        img3 = img3.resize((1350, 700), PIL.Image.LANCZOS)#réize
        self.photoimg3 = ImageTk.PhotoImage(img3)

        # thông tin kết nối database
        self.db = Database_str()


        bg_img = Label(self.root, image=self.photoimg3)#label nền
        bg_img.place(x=0, y=0, width=1350, height=700)#vị trí và kích thước của label

        heading = Label(bg_img, text="Hệ thống điểm danh khuôn mặt", font=("yu gothic ui", 20, "bold"), bg="white",
                        fg="red2",
                        bd=0, relief=FLAT)#tiêu đề chữ màu đỏ
        heading.place(x=400, y=15, width=550, height=30)

        self.current_image = None


        #teacher _ ID
        print(value_from_home)
        self.teacher_id=value_from_home #Chọn teacher id = id người  đăng nhập vào hệ thống
        #lesson_id
        self.lessonid=None# biến id buổi học
        #self
        self.className=None

        today = strftime("%d/%m/%Y")#time_today
        subject_array = [] #mảng để chứa thông tin môn,buổi học
        #lấy ra thông tin buổi học có trong ngày
        if(value_from_home=="0" or value_from_home==None):#đăng nhập admin (nếu value_from_home =0 hoặc none thì coi như đăng nhập với quyền admin)
        	#kết nối database
            conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password, database=self.db.database, port=self.db.port)
            my_cursor = conn.cursor()
            self.teacher_id=0#chọn id giáo viên=0 (0 là mã dùng cho admin)
            my_cursor.execute(
                "SELECT DISTINCT Class,Lesson_Id  from lesson where  Date=%s",
                (today,))#câu lệnh lấy ra danh sách buổi học,môn học trong ngày
            subject_ls = my_cursor.fetchall()
            for i in subject_ls:
                print(i)
                t = str(i).replace("'", "", 4).replace("(", "").replace(")", "").replace(" ",
                                                                                         "")  ##loại bỏ các ký tự thừa để hiển thị tên môn,buổi học
                # print(t)
                subject_array.append(t)#truyền các dòng dữ liệu vừa truy vấn đc vào mảng
        else:# nếu đăng nhập bằng tk giáo viên
            conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password, database=self.db.database, port=self.db.port)
            my_cursor = conn.cursor()
            my_cursor.execute(
                "SELECT DISTINCT Class,Lesson_Id  from lesson where  Date=%s",
                (today, ))
            subject_ls = my_cursor.fetchall()
            for i in subject_ls:
                t = str(i).replace("'", "", 4).replace("(", "").replace(")", "").replace(" ", "")
                # print(t)
                subject_array.append(t)

        #=======================================LEFT FRAME=========================================
        #frame chứa màn hình nhận diện gồm camera và các nút mở, đóng cam
        Left_frame = LabelFrame(self.root, bd=2, bg="white", relief=RIDGE, text="Màn hình nhận diện",
                                font=("times new roman", 11, "bold"))#tạo frame (self.root là nằm trong giao diện app,bd=2:  bo viền 2px)
        Left_frame.place(x=30, y=70, width=780, height=540)#vị trú của frame

        self.panel = ttk.Label(Left_frame,borderwidth=2, relief="groove")

        self.panel.place(x=8, y=50, width=760, height=420)

        #Chọn buổi học để điểm danh
        self.choose_frame = LabelFrame(Left_frame, bd=1, bg="white", relief=RIDGE,
                                  font=("times new roman", 11, "bold"))
        self.choose_frame.place(x=8, y=0, width=760, height=40)

        #txt chọn buổi học
        search_label = Label(self.choose_frame, text="Chọn Lớp,Buổi học: ", font=("times new roman", 11, "bold"),
                             bg="white")
        search_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)


        self.selectsub=StringVar()
        self.lesson_combo = ttk.Combobox(self.choose_frame,textvariable=self.selectsub ,font=("times new roman", 12, "italic"), state="readonly",
                                    width=18)
        self.lesson_combo["values"] = subject_array#các giá trị trong combobox là các giá trị của mảng subject_array đã truyền
        self.lesson_combo.current()#giá trị ban đầu của combobox là rỗng
        self.lesson_combo.bind("<<ComboboxSelected>>", self.callbackFunc)
        self.lesson_combo.grid(row=0, column=1, padx=5, pady=10, sticky=W)

        #choose attendance_value
        choose_type_att=Label(self.choose_frame, text="Chọn loại Điểm Danh: ", font=("times new roman", 12, "bold"),
                             bg="white")
        choose_type_att.grid(row=0, column=2, padx=35, pady=10, sticky=W)

        self.type_attendance=StringVar()#loại điểm danh
        self.type_combo=ttk.Combobox(self.choose_frame,textvariable=self.type_attendance ,font=("times new roman", 11, "bold"), state="readonly",
                                    width=18)
        self.type_combo["values"] = ("Vào","Ra")
        self.type_combo.current(0)
        self.type_combo.grid(row=0, column=3, padx=0, pady=10, sticky=W)


        #thông báo điểm danh
        self.notify_frame = LabelFrame(Left_frame, bd=1, bg="white", relief=RIDGE,
                                       font=("times new roman", 11, "bold"))
        self.notify_frame.place(x=8, y=480, width=760, height=35)
        self.notify_label = Label(self.notify_frame, text="Thông báo: Vui lòng chọn Môn/ID Buổi học để mở Camera điểm danh !!!", font=("times new roman", 11, "bold"),
                             bg="white",fg="red")
        self.notify_label.grid(row=0, column=0, padx=10, pady=5, sticky=W)

        #nút camera
        img_btn1 = PIL.Image.open(r"ImageFaceDetect\btnOpen.png")#ảnh nút mở camera
        img_btn1 = img_btn1.resize((350, 45), PIL.Image.LANCZOS)
        self.photobtn1 = ImageTk.PhotoImage(img_btn1)
        self.btnOpen= Button(self.root ,bg="white", cursor="hand2",
                      borderwidth=0,image=self.photobtn1,command=self.face_recog,fg="white",disabledforeground="black")
        self.btnOpen.place(x=30, y=620, width=350, height=45)
        if self.selectsub.get()=="":#nếu chưa chọn môn học,buổi học thì ko cho mở cam
            self.btnOpen['state'] = "disabled"

        img_btn2 = PIL.Image.open(r"ImageFaceDetect\btnClose.png")#ảnh nút đóng camera
        img_btn2 = img_btn2.resize((350, 45), PIL.Image.LANCZOS)
        self.photobtn2 = ImageTk.PhotoImage(img_btn2)
        self.btnClose = Button(self.root, cursor="hand2",
                      borderwidth=0,image=self.photobtn2, bg="white",command=self.is_clicked, fg="white")
        self.btnClose.place(x=460, y=620, width=350, height=45)


        #Right_frame

        #frame chứa trạng thái điểm danh bao gồm các thông tin như ảnh điểm danh, thời gian điểm danh,tên học sinh
        self.Right_frame = LabelFrame(self.root, bd=2, bg="white", relief=RIDGE, text="Điểm danh thành công",
                                font=("times new roman", 12, "bold"))
        self.Right_frame.place(x=900, y=70, width=400, height=380)

        self.img_right = PIL.Image.open(r"ImageFaceDetect\unknown_student.png")#ảnh điểm danh mặc định khi ko có ai điểm danh
        self.img_right = self.img_right.resize((190, 190), PIL.Image.LANCZOS)
        self.photoimg_left = ImageTk.PhotoImage(self.img_right)

        #label chứa ảnh
        self.f_lbl = Label(self.Right_frame, image=self.photoimg_left,bg="white",borderwidth=2, relief="groove",highlightcolor="darkblue")
        self.f_lbl.place(x=110, y=10, width=190, height=190)

        self.studentID_atten_info=Label(self.Right_frame, bg="white",
                                font=("times new roman", 12, "bold"))
        self.studentID_atten_info.place(x=5, y=220, width=380, height=120)

        #id học sinh
        self.studentID_label = Label(self.studentID_atten_info, text="ID Học sinh:", font=("times new roman", 11, "bold"), bg="white")
        self.studentID_label.grid(row=0, column=0, padx=10,pady=7, sticky=W)

        self.studentID_atten_label = Label(self.studentID_atten_info, text="", font=("times new roman", 11, "bold"),
                                bg="white")
        self.studentID_atten_label.grid(row=0, column=1, padx=10, pady=7, sticky=W)


        #tên hoc sinh
        self.studentname_label = Label(self.studentID_atten_info, text="Tên Học sinh:", font=("times new roman", 11, "bold"),
                                     bg="white")
        self.studentname_label.grid(row=1, column=0, padx=10, pady=7, sticky=W)

        self.studentname_atten_label = Label(self.studentID_atten_info, text="", font=("times new roman", 11, "bold"),
                                           bg="white")
        self.studentname_atten_label.grid(row=1, column=1, padx=10, pady=7, sticky=W)


        #thời gian điểm danh
        self.studentclass_label = Label(self.studentID_atten_info, text="Thời gian:",
                                       font=("times new roman", 11, "bold"),
                                       bg="white")
        self.studentclass_label.grid(row=2, column=0, padx=10, pady=7, sticky=W)

        self.studentclass_atten_label = Label(self.studentID_atten_info, text="",
                                             font=("times new roman", 11, "bold"),
                                             bg="white")
        self.studentclass_atten_label.grid(row=2, column=1, padx=10, pady=7, sticky=W)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        #======================Class-info==============================
        #frame chứa thông tin buổi học
        self.RightU_frame = LabelFrame(self.root, bd=2, bg="white", relief=RIDGE, text="Thông tin buổi học",
                                      font=("times new roman", 11, "bold"))
        self.RightU_frame.place(x=900, y=465, width=400, height=180)

        #Lớp
        self.className_label = Label(self.RightU_frame, text="Lớp :",
                                     font=("times new roman", 11, "bold"), bg="white")
        self.className_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)

        self.className_atten_label = Label(self.RightU_frame, text="", font=("times new roman", 11, "bold"),
                                           bg="white",fg="red2")
        self.className_atten_label.grid(row=0, column=1, padx=10, pady=10, sticky=W)

        # môn/buổi học
        self.subject_lesson_label = Label(self.RightU_frame, text="ID Buổi học:",
                                       font=("times new roman", 11, "bold"),
                                       bg="white")
        self.subject_lesson_label.grid(row=1, column=0, padx=10, pady=10, sticky=W)

        self.subject_lesson_atten_label = Label(self.RightU_frame, text="", font=("times new roman", 11, "bold"),
                                             bg="white",fg="red2")
        self.subject_lesson_atten_label.grid(row=1, column=1, padx=10, pady=10, sticky=W)

        # thời gian
        self.classtime_label = Label(self.RightU_frame, text="Thời gian:",
                                        font=("times new roman", 11, "bold"),
                                        bg="white")
        self.classtime_label.grid(row=2, column=0, padx=10, pady=10, sticky=W)

        self.classtime_atten_label = Label(self.RightU_frame, text="",
                                              font=("times new roman", 11, "bold"),
                                              bg="white",fg="red2")
        self.classtime_atten_label.grid(row=2, column=1, padx=10, pady=10, sticky=W)



        #=============Kiểm tra xem ngày hôm nay có môn học nào điểm danh ko=====
        if not subject_array:#nếu ko có
            self.lesson_combo['state'] = "disabled"#combobox ko đc bấm chọn
            self.notify_label[
                'text'] = "Bạn không có môn học nào cần điểm danh hôm nay"#thông báo ko có môn học hôm nay
            self.btnOpen['state']= "disabled"#nút mở camera ko hoạt động

    def is_clicked(self):#nếu chưa bấm nút mở camera
        self.isClicked=True
        self.lesson_combo['state'] = "readonly"
        self.type_combo['state']="readonly"
        self.notify_label[
            'text'] = "Vui lòng chọn ID Buổi học/Tên môn học để điểm danh"
        self.notify_label['fg']="red"

        print("Camera is Closed")

    def on_closing(self):#đóng cam
        self.isClicked = True
        self.root.destroy()

    def callbackFunc(self,event):#hiển thị thông tin buổi học
        mls = event.widget.get()
        # print(mls)

        if self.selectsub.get()=="":#nếu ko chọn buổi học
            self.btnOpen['state'] = "disabled" #nút mở camera bị vô hiệu
        else:
            c = str(mls).split(",")
            self.className=str(c[0])
            self.lessonid=str(c[1])#thông tin id buổi học
            # self.subject_name=str(c[0]) # tên lớp học
            # print(self.subject_name)
            self.btnOpen['state']="normal"
            conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password, database=self.db.database, port=self.db.port)
            my_cursor = conn.cursor()
            #truy vấn thông tin buổi học
            my_cursor.execute("select Time_start,Time_end,Class from lesson where Lesson_id=%s ",
                              (self.lessonid,))
            getInfo=my_cursor.fetchone()
            timeclass=str(getInfo[0])+" - "+str(getInfo[1])
            class_name=getInfo[2]
            subles=self.lessonid
            self.className_atten_label['text']=class_name
            self.subject_lesson_atten_label['text']=subles
            self.classtime_atten_label['text']=timeclass
        # print(self.lessonid)


    #===========attendance===================
    def mark_attendance(self,i,r,n,d,face_cropped):#hàm điểm danh (i: mã học sinh, r:CMND, n:Tên học sinh, d: Lớp học , facc_cropped: khuôn mặt đc cắt ra)
        img_id=0
        self.lesson_combo['state']="disabled"#các combobox ko thể chọn trong lúc điểm danh
        self.type_combo['state']="disabled"
        while True:# khi camera mở lên không có lỗi
            #Them data len csdl
            now = datetime.now()
            d1 = strftime("%d/%m/%Y")#ngày hôm nay
            dtString = now.strftime("%H:%M:%S")#thời điểm hiện tại giờ:phút:giây
            ma="SV"+str(i)+d1+self.lessonid#mã điểm danh =SV+str(i)+ngày hôm nay+id buổi học ()
            masp=ma.replace("/","")
            # print(masp)
            img_id+=1

            # kiểm tra xem Học sinh có trong ds lớp hay không thông qua lesson_id
            conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password, database=self.db.database, port=self.db.port)
            my_cursor = conn.cursor()
            my_cursor.execute(
                "select Student_id from student where "
                "Class='" + self.className+"'")

            chkStudent = my_cursor.fetchall()
            chkarray = []#mảng chứa thông tin id học sinh trong lớp học
            for cks in chkStudent:

                chkarray.append(cks[0])

            if(i not in chkarray):
                self.notify_label['text']="Thông báo: Học sinh "+n+" Không có trong danh sách lớp"
                print("Học sinh:" + n + " không có trong danh sách lớp học ")
            else:#nếu học sinh có trong lớp học
                try:
                	#kết nối db
                        conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password, database=self.db.database, port=self.db.port)

                        my_cursor = conn.cursor()
                        my_cursor.execute("select Date,Lesson_id from attendance where Student_id=" + str(i))#kiểm tra thông tin học sinh trong bảng điểm danh

                        idn = my_cursor.fetchall()
                        a = [] #mảng ngày
                        b=[]   #mảng lesson_id

                        for i1 in idn:
                            str2 = ''.join(i1[0])
                            # str1=''.join(i1[1])
                            a.append(str2)#ngày điểm danh
                            b.append(str(i1[1]))#buổi học điểm danh
                        #nếu chọn loại điểm danh là ra hoặc vào
                        if(self.type_attendance.get()=="Vào"):
                            if((d1 not in a)) or ((self.lessonid not in b)):# nếu ngày hôm nay học sinh  chưa điểm danh hoặc học sinh chưa điểm danh buổi học dc chọn

                                my_cursor = conn.cursor()
                                #thêm thông tin bản điểm danh lên cơ sở dữ liệu
                                my_cursor.execute("insert into attendance values(%s,%s,%s,%s,%s,%s,%s,%s,%s)", (
                                    masp,
                                    str(i),
                                    n,
                                    d,
                                    dtString,
                                    None,
                                    d1,
                                    self.lessonid,
                                    "",
                                ))
                                #lưu ảnh điểm danh ra thư mục
                                cv2.imwrite("DiemDanhImage/ " + masp + ".jpg",
                                           face_cropped)
                                #=============================Check_attendance===============================
                                #hiển thị ảnh điểm danh thành công
                                self.img_right = PIL.Image.open(r"DiemDanhImage/ " + masp + ".jpg")
                                self.img_right = self.img_right.resize((190, 190), PIL.Image.LANCZOS)
                                self.photoimg_left = ImageTk.PhotoImage(self.img_right)

                                self.f_lbl = Label(self.Right_frame, image=self.photoimg_left, bg="white", borderwidth=1,
                                                   relief="groove")
                                self.f_lbl.place(x=110, y=10, width=190, height=190)

                                # id học sinh
                                self.studentID_label = Label(self.studentID_atten_info, text="ID Học sinh:",
                                                             font=("times new roman", 11, "bold"), bg="white")
                                self.studentID_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)
                                self.studentID_atten_label = Label(self.studentID_atten_info, text=i,
                                                                   font=("times new roman", 11, "bold"),
                                                                   bg="white", relief="sunken", width=20, justify="left")
                                self.studentID_atten_label.grid(row=0, column=1, padx=15, pady=10, sticky=W)

                                # tên học sinh
                                self.studentname_label = Label(self.studentID_atten_info, text="Tên Học sinh:",
                                                               font=("times new roman", 11, "bold"),
                                                               bg="white")
                                self.studentname_label.grid(row=1, column=0, padx=10, pady=10, sticky=W)

                                self.studentname_atten_label = Label(self.studentID_atten_info, text=n,
                                                                     font=("times new roman", 11, "bold"), relief="sunken",
                                                                     width=18,
                                                                     bg="white", justify="left")
                                self.studentname_atten_label.grid(row=1, column=1, padx=15, pady=10, ipadx=10)

                                # lớp học
                                self.studentclass_label = Label(self.studentID_atten_info, text="Thời gian:",
                                                                font=("times new roman", 11, "bold"),
                                                                bg="white")
                                self.studentclass_label.grid(row=2, column=0, padx=10, pady=10, sticky=W)
                                self.studentclass_atten_label = Label(self.studentID_atten_info, text=dtString,
                                                                      font=("times new roman", 11, "bold"),
                                                                      bg="white", relief="sunken", width=20, justify="left")
                                self.studentclass_atten_label.grid(row=2, column=1, padx=15, pady=10, sticky=W)
                            else:#nếu đã điểm danh rồi
                                # print("Sinh vien:" + n+ " Đã điểm danh ngày "+d1+ ". Vui lòng ra khỏi Camera !!")
                                self.notify_label['text'] = "Thông báo: Học sinh: " + n + " đã điểm danh vào lớp thành công hôm nay "
                                self.notify_label['fg']="green"

                                #=====================Change_AttendanceStatus===================================
                                #kiểm tra thời gian vào
                                my_cursor = conn.cursor()
                                my_cursor.execute("Select Time_in from attendance where Student_id=%s and Lesson_id=%s ",(str(i),(self.lessonid),))
                                ckTime_in = my_cursor.fetchone()
                                time_in = ckTime_in[0]
                                # print(time_in)

                                # -======Timestart========
                                #lấy ra thời gian bắt đầu buổi học
                                my_cursor.execute("Select Time_start from lesson where Lesson_id=%s ",(self.lessonid,))
                                ckStart_in = my_cursor.fetchone()
                                time_start = ckStart_in[0]
                                # print(time_start)
                                if(time_in<time_start):#nếu thời gian điểm danh vào nhỏ hơn thời gian bắt đầu ->Cập nhật trangh thái thành có mặt
                                    my_cursor.execute(
                                        "update  attendance set AttendanceStatus=%s where Student_id=%s and Lesson_id=%s",
                                        ("Có mặt", str(i), (self.lessonid),))
                                else:
                                    a = datetime.strptime(str(time_in - time_start), '%H:%M:%S').time()#thời gian học sinh điểm danh muộn hơn so với thời gia bắt đầu
                                    b = datetime.strptime('0:00:00', '%H:%M:%S').time()#thoi gian dc phep diem danh co mat 15 phut
                                    c = datetime.strptime('0:50:00', '%H:%M:%S').time()# thoi gian dc phep diem danh muon
                                    d = datetime.strptime('1:00:00', '%H:%M:%S').time()#thoi gian cho phep sv vang 1 tiet

                                    if (b < a < c):#nếu thời gian đi muộn lớn hơn 15 phút và nhỏ hơn 50phuts thì cập nhật trạng thái đi muộn

                                        stt="Đi muộn " + str(a.minute)+" phút"
                                        # print(stt)
                                        my_cursor.execute("update  attendance set AttendanceStatus=%s where Student_id=%s and Lesson_id=%s",
                                                          (stt,str(i),(self.lessonid),))
                                    elif (c < a < d):#nếu thời gian đi muộn lớn hơn 50 và nhỏ hơn 1 tiếng -> vắng 1 tiết
                                        my_cursor.execute("update  attendance set AttendanceStatus=%s where Student_id=%s and Lesson_id=%s",
                                                          ("Vắng 1 tiết",str(i),(self.lessonid),))
                                    else:#nếu thời gian đi muộn lớn hơn 1 tiếng -> Vắng
                                        my_cursor.execute("update  attendance set AttendanceStatus=%s where Student_id=%s and Lesson_id=%s",
                                                          ("Vắng",str(i),(self.lessonid),))
                                    # print("Vắng")
                            conn.commit()
                            # self.fetch_data()
                            conn.close()
                            # messagebox.showinfo("Thành công", "Thêm thông tin Học sinh thành công", parent=self.root)
                        elif(self.type_attendance.get()=="Ra"):#Loại điểm danh ra khỏi lớp : tương tự điểm dah vào
                            conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password, database=self.db.database, port=self.db.port)

                            my_cursor = conn.cursor()
                            my_cursor.execute("select IdAuttendance from attendance")
                            idatt = my_cursor.fetchall()
                            att=[]
                            for ida in idatt:
                                att.append(str(ida[0]))
                            if(masp not in att):
                                if ((d1 not in a)) or ((self.lessonid not in b)):

                                    my_cursor = conn.cursor()
                                    my_cursor.execute("insert into attendance values(%s,%s,%s,%s,%s,%s,%s,%s,%s)", (
                                        masp,
                                        str(i),
                                        n,
                                        d,
                                        None,
                                        dtString,
                                        d1,
                                        self.lessonid,
                                        "Có mặt",
                                    ))
                                    cv2.imwrite("DiemDanhImage/ " + masp +"Ra"+ ".jpg",
                                                face_cropped)
                                    # =============================Check_attendance===============================

                                    self.img_right = PIL.Image.open(r"DiemDanhImage\ " + masp +"Ra" +".jpg")
                                    self.img_right = self.img_right.resize((190, 190), PIL.Image.LANCZOS)
                                    self.photoimg_left = ImageTk.PhotoImage(self.img_right)

                                    self.f_lbl = Label(self.Right_frame, image=self.photoimg_left, bg="white",
                                                       borderwidth=1,
                                                       relief="groove")
                                    self.f_lbl.place(x=110, y=10, width=190, height=190)

                                    # stdID
                                    self.studentID_label = Label(self.studentID_atten_info, text="ID Học sinh:",
                                                                 font=("times new roman", 11, "bold"), bg="white")
                                    self.studentID_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)
                                    self.studentID_atten_label = Label(self.studentID_atten_info, text=i,
                                                                       font=("times new roman", 11, "bold"),
                                                                       bg="white", relief="sunken", width=20,
                                                                       justify="left")
                                    self.studentID_atten_label.grid(row=0, column=1, padx=15, pady=10, sticky=W)

                                    # name
                                    self.studentname_label = Label(self.studentID_atten_info, text="Tên Học sinh:",
                                                                   font=("times new roman", 11, "bold"),
                                                                   bg="white")
                                    self.studentname_label.grid(row=1, column=0, padx=10, pady=10, sticky=W)

                                    self.studentname_atten_label = Label(self.studentID_atten_info, text=n,
                                                                         font=("times new roman", 11, "bold"),
                                                                         relief="sunken",
                                                                         width=18,
                                                                         bg="white", justify="left")
                                    self.studentname_atten_label.grid(row=1, column=1, padx=15, pady=10, ipadx=10)

                                    # class
                                    self.studentclass_label = Label(self.studentID_atten_info, text="Thời gian:",
                                                                    font=("times new roman", 11, "bold"),
                                                                    bg="white")
                                    self.studentclass_label.grid(row=2, column=0, padx=10, pady=10, sticky=W)
                                    self.studentclass_atten_label = Label(self.studentID_atten_info, text=dtString,
                                                                          font=("times new roman", 11, "bold"),
                                                                          bg="white", relief="sunken", width=20,
                                                                          justify="left")
                                    self.studentclass_atten_label.grid(row=2, column=1, padx=15, pady=10, sticky=W)
                                else:
                                    # print(
                                    #     "Sinh vien:" + n + " Đã điểm danh ngày " + d1 + ". Vui lòng ra khỏi Camera !!")
                                    self.notify_label[
                                        'text'] = "Thông báo: Học sinh: " + n + " đã điểm danh ra thành công môn học "
                                    self.notify_label['fg'] = "green"

                                    # =====================Change_AttendanceStatus===================================
                                    my_cursor = conn.cursor()
                                    my_cursor.execute(
                                        "Select Time_out from attendance where Student_id=%s and Lesson_id=%s ",
                                        (str(i), (self.lessonid),))
                                    ckTime_out = my_cursor.fetchone()
                                    time_out = ckTime_out[0]
                                    # print(time_out)

                                    # -======Timeend========

                                    my_cursor.execute("Select Time_end from lesson where Lesson_id=%s ",
                                                      (self.lessonid,))
                                    ckend_in = my_cursor.fetchone()
                                    time_end = ckend_in[0]
                                    # print(time_start)
                                    if(time_end<time_out):
                                        my_cursor.execute(
                                            "update  attendance set AttendanceStatus=%s where Student_id=%s and Lesson_id=%s",
                                            ("Có mặt", str(i), (self.lessonid),))
                                    else:
                                        a = datetime.strptime(str(time_end - time_out), '%H:%M:%S').time()
                                        b = datetime.strptime('0:15:00',
                                                              '%H:%M:%S').time()  # thoi gian dc phep diem danh co mat trc 15p
                                        c = datetime.strptime('0:50:00',
                                                              '%H:%M:%S').time()  # thoi gian dc phep diem danh muon

                                        if (a < b):
                                            my_cursor.execute(
                                                "update  attendance set AttendanceStatus=%s where Student_id=%s and Lesson_id=%s",
                                                ("Có mặt", str(i), (self.lessonid),))
                                        elif (b < a < c):
                                            my_cursor.execute(
                                                "update  attendance set AttendanceStatus=%s where Student_id=%s and Lesson_id=%s",
                                                ("Vắng 1 tiết", str(i), (self.lessonid),))
                                        else:
                                            my_cursor.execute(
                                                "update  attendance set AttendanceStatus=%s where Student_id=%s and Lesson_id=%s",
                                                ("Vắng", str(i), (self.lessonid),))

                            else:
                                my_cursor = conn.cursor()
                                my_cursor.execute("select Time_out from attendance where IdAuttendance=%s",(masp,))
                                timeout_check=my_cursor.fetchone()
                                if(timeout_check[0]==None):
                                    my_cursor = conn.cursor()
                                    my_cursor.execute(
                                        "update  attendance set Time_out=%s where Student_id=%s and Lesson_id=%s",
                                        (dtString, str(i), (self.lessonid),))
                                    cv2.imwrite("DiemDanhImage/ " + masp + "Ra" + ".jpg",
                                                face_cropped)
                                    # =============================Check_attendance===============================

                                    self.img_right = PIL.Image.open(r"DiemDanhImage\ " + masp + "Ra" + ".jpg")
                                    self.img_right = self.img_right.resize((190, 190), PIL.Image.LANCZOS)
                                    self.photoimg_left = ImageTk.PhotoImage(self.img_right)

                                    self.f_lbl = Label(self.Right_frame, image=self.photoimg_left, bg="white",
                                                       borderwidth=1,
                                                       relief="groove")
                                    self.f_lbl.place(x=110, y=10, width=190, height=190)

                                    # stdID
                                    self.studentID_label = Label(self.studentID_atten_info, text="ID Học sinh:",
                                                                 font=("times new roman", 11, "bold"), bg="white")
                                    self.studentID_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)
                                    self.studentID_atten_label = Label(self.studentID_atten_info, text=i,
                                                                       font=("times new roman", 11, "bold"),
                                                                       bg="white", relief="sunken", width=20,
                                                                       justify="left")
                                    self.studentID_atten_label.grid(row=0, column=1, padx=15, pady=10, sticky=W)

                                    # name
                                    self.studentname_label = Label(self.studentID_atten_info, text="Tên Học sinh:",
                                                                   font=("times new roman", 11, "bold"),
                                                                   bg="white")
                                    self.studentname_label.grid(row=1, column=0, padx=10, pady=10, sticky=W)

                                    self.studentname_atten_label = Label(self.studentID_atten_info, text=n,
                                                                         font=("times new roman", 11, "bold"),
                                                                         relief="sunken",
                                                                         width=18,
                                                                         bg="white", justify="left")
                                    self.studentname_atten_label.grid(row=1, column=1, padx=15, pady=10, ipadx=10)

                                    # class
                                    self.studentclass_label = Label(self.studentID_atten_info, text="Thời gian:",
                                                                    font=("times new roman", 11, "bold"),
                                                                    bg="white")
                                    self.studentclass_label.grid(row=2, column=0, padx=10, pady=10, sticky=W)
                                    self.studentclass_atten_label = Label(self.studentID_atten_info, text=dtString,
                                                                          font=("times new roman", 11, "bold"),
                                                                          bg="white", relief="sunken", width=20,
                                                                          justify="left")
                                    self.studentclass_atten_label.grid(row=2, column=1, padx=15, pady=10, sticky=W)
                                else:
                                    # print(
                                    #     "Sinh vien:" + n + " Đã điểm danh ngày " + d1 + ". Vui lòng ra khỏi Camera !!")
                                    self.notify_label[
                                        'text'] = "Thông báo: Học sinh: " + n + " đã điểm danh ra thành công môn học "
                                    self.notify_label['fg'] = "green"
                                    # =====================Change_AttendanceStatus===================================
                                    my_cursor = conn.cursor()
                                    my_cursor.execute(
                                        "Select Time_out from attendance where Student_id=%s and Lesson_id=%s ",
                                        (str(i), (self.lessonid),))
                                    ckTime_out = my_cursor.fetchone()
                                    time_out = ckTime_out[0]
                                    # print(time_out)

                                    # -======Timestart========

                                    my_cursor.execute("Select Time_end from lesson where Lesson_id=%s ",
                                                      (self.lessonid,))
                                    ckend_in = my_cursor.fetchone()
                                    time_end = ckend_in[0]
                                    # print(time_start)
                                    if (time_end < time_out):
                                        my_cursor.execute(
                                            "update  attendance set AttendanceStatus=%s where Student_id=%s and Lesson_id=%s",
                                            ("Có mặt", str(i), (self.lessonid),))
                                    else:
                                        a = datetime.strptime(str(time_end - time_out), '%H:%M:%S').time()
                                        b = datetime.strptime('0:15:00',
                                                              '%H:%M:%S').time()  # thoi gian dc phep diem danh co mat trc 15p
                                        c = datetime.strptime('0:50:00',
                                                              '%H:%M:%S').time()  # thoi gian dc phep diem danh muon

                                        if (a < b):
                                            my_cursor.execute(
                                                "update  attendance set AttendanceStatus=%s where Student_id=%s and Lesson_id=%s",
                                                ("Có mặt", str(i), (self.lessonid),))
                                        elif (b < a < c):
                                            my_cursor.execute(
                                                "update  attendance set AttendanceStatus=%s where Student_id=%s and Lesson_id=%s",
                                                ("Vắng 1 tiết", str(i), (self.lessonid),))
                                        else:
                                            my_cursor.execute(
                                                "update  attendance set AttendanceStatus=%s where Student_id=%s and Lesson_id=%s",
                                                ("Vắng", str(i), (self.lessonid),))


                            conn.commit()
                            conn.close()


                except Exception as es:
                        messagebox.showerror("Error", f"Due To:{str(es)}", parent=self.root)
            if img_id==1:
                break


    def face_recog(self):#hàm nhận diện khuôn mặt
            self.isClicked=False#nếu đã mở cam
            faceDetectionModel = "./models/res10_300x300_ssd_iter_140000_fp16.caffemodel"
            faceDetectionProto = "./models/deploy.prototxt"
            faceDescriptor = "./models/openface.nn4.small2.v1.t7"

            dectectorModel = cv2.dnn.readNetFromCaffe(faceDetectionProto, faceDetectionModel)
            descriptorModel = cv2.dnn.readNetFromTorch(faceDescriptor)
            face_recognition_model = pickle.load(open("./ml_face_person_identity.pkl", mode = "rb"))
            def draw_boundray(img):#xác định khuôn mặt trong khung hình
                image = img
                h, w = img.shape[:2]
                img_blob = cv2.dnn.blobFromImage(img, 1, (300, 300), (104, 177, 123), swapRB = False, crop = False)
                dectectorModel.setInput(img_blob)
                detections = dectectorModel.forward()

                if len(detections) > 0:
                    for i, confidence in enumerate(detections[0, 0, :, 2]):
                        if confidence > 0.5:
                            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                            startx, starty, endx, endy = box.astype(int)

                            cv2.rectangle(image, (startx, starty), (endx, endy), (0, 255, 0))

                            # feature extraction
                            face_roi = img[starty:endy, startx:endx]
                            print(len(face_roi))
                            if len(face_roi) != 0:
                                face_blob = cv2.dnn.blobFromImage(face_roi, 1 / 255, (96, 96), (0, 0, 0), swapRB = True,
                                                              crop = True)
                                descriptorModel.setInput(face_blob)
                                vectors = descriptorModel.forward()

                                # predict with machine learning
                                face_name = face_recognition_model.predict(vectors)[0]
                                face_score = face_recognition_model.predict_proba(vectors).max()

                                if face_score > 0.9:
                                    text_face = '{} : {:.0f} %'.format(face_name, 100 * face_score)
                                    cv2.putText(image, text_face, (startx, starty), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255),
                                                2)

                                    # kết nối database
                                    conn = mysql.connector.connect(host = self.db.host, user = self.db.user,
                                                                   password = self.db.password, database = self.db.database,
                                                                   port = self.db.port)
                                    my_cursor = conn.cursor()

                                    # tên học sinh
                                    my_cursor.execute("select Name from student where Student_id=" + str(face_name))
                                    n = my_cursor.fetchone()

                                    n = "+".join(n)

                                    # CMND
                                    my_cursor.execute("select Roll from student where Student_id=" + str(face_name))
                                    r = my_cursor.fetchone()
                                    r = "+".join(r)

                                    # lớp học
                                    my_cursor.execute("select Class from student where Student_id=" + str(face_name))
                                    d = my_cursor.fetchone()
                                    d = "+".join(d)

                                    # id học sinh
                                    my_cursor.execute("select Student_id from student where Student_id=" + str(face_name))
                                    i = my_cursor.fetchone()
                                    i = i[0]

                                    face_cropped = cv2.resize(image, (190, 190))  # resize ảnh

                                    self.mark_attendance(i,r,n,d,face_cropped)#Lưu thông tin điểm danh lên database

                                else:
                                    text_face = '{} : {:.0f} %'.format(face_name, 100 * face_score)
                                    cv2.putText(image, "Unknown", (startx, starty), cv2.FONT_HERSHEY_PLAIN, 2,
                                                (255, 255, 255),
                                                2)

                            # self.mark_attendance(i,r,n,d,face_cropped)#Lưu thông tin điểm danh lên database
                        # else:
                        #     box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                        #     startx, starty, endx, endy = box.astype(int)
                        #     cv2.putText(image, "Unknown", (startx, starty), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255),
                        #                 2)
                        #
                        #     cv2.rectangle(image, (startx, starty), (endx, endy), (0, 255, 0))

                return image

            def recognize(img):#nhận diện khuôn mặt
                draw_boundray(img)
                return img


            self.camara=cv2.VideoCapture(0)#mở camera : 0 là webcam
            self.camara.set(3, 800) ##chiều dài cam
            self.camara.set(4, 580)  ##chiều rộng cam
            self.camara.set(10, 150)  #độ sáng
            while True:#nếu mở thành công

                ret,img=self.camara.read()
                img=recognize(img)#truyền hàm nhận diện vào camera
                # cv2.imshow("Welcome to face REg",img)
                img=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)#chuyển ảnh trong khung hình về dạng gray để nhận diện
                img = PIL.Image.fromarray(img, mode='RGB')
                img = PIL.ImageTk.PhotoImage(img)  # convert image for tkinter
                self.panel['image']=img
                # self.panel.update()
                self.panel.update()


                if (self.isClicked==True): ##Nếu bấm đóng cam thì thoát khỏi cam
                    break
            self.camara.release()
            cv2.destroyAllWindows()



if __name__=="__main__":
    root=Tk() #khoi tao cua so va gan root vao
    obj=Face_Recognition(root)
    root.mainloop()# cua so hien len