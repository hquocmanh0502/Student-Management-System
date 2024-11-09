import os
import random
from PIL import Image, ImageTk
from tkinter import *
from tkinter import ttk
import PIL.Image
from time import strftime
import calendar
import time

from math import *
from tkinter import messagebox
import mysql.connector
import csv
import pandas as pd
from tkinter import filedialog
from tkcalendar import Calendar, DateEntry
from database_str import Database_str

mydata=[]#mảng dữ liệu cho điểm danh muộn
mydataNot=[]#mảng dữ liệu điểm danh vắng
mydataNotInAtt=[]#mảng dữ liệu học sinh ko điểm danh
class Report:
    def __init__(self,root):
        self.root=root
        w = 1350  # chiều dài giao diện
        h = 700  # chiều rộng giao diện

        ws = self.root.winfo_screenwidth()  # độ dài màn hình
        hs = self.root.winfo_screenheight()  # độ rộng màn
        x = (ws / 2) - (w / 2)  # vị trí cách lề trái x px
        y = (hs / 2) - (h / 2)  # vị trí cách lề trên y px
        self.root.iconbitmap('ImageFaceDetect\\gaming.ico')  # icon của giao diện
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))  # kích thước và vị trí hiển thị giao diện
        self.root.title("Hệ thống nhận diện khuôn mặt")
        self.today = strftime("%d-%m-%Y")#thời gian ngày-tháng-năm hiện tại
        self.today_time = strftime("%d/%m/%Y")

        # thông tin kết nối database
        self.db = Database_str()
        
        #===========variable============
        self.student = StringVar()#biến student để đếm số học sinh trong database sau khi truy vấn
        self.att=StringVar()#số bản điểm danh
        self.late=StringVar()#số lần đi muộn của các học sinh
        self.noatt=StringVar()# số lần vắng của các học sinh

        img3 = PIL.Image.open(r"ImageFaceDetect\bg1.png")#mở ảnh nền
        img3 = img3.resize((1350, 700), PIL.Image.LANCZOS)#resize kích thước ảnh
        self.photoimg3 = ImageTk.PhotoImage(img3)

        bg_img = Label(self.root, image=self.photoimg3)
        bg_img.place(x=0, y=0, width=1350, height=700)

        # ==================================heading====================================
        # =========time=========

        # ========title=========
        self.txt = "Thống kê hệ thống"
        self.count = 0
        self.text = ''
        self.color = ["#4f4e4d", "#f29844", "red2"]
        self.heading = Label(self.root, text=self.txt, font=("times new roman", 18, "bold"), bg="white", fg="black",
                             bd=0, relief=FLAT)
        self.heading.place(x=350, y=20, width=600)
        # self.slider()
        # self.heading_color()

        main_frame = Frame(bg_img, bd=2, bg="white")
        main_frame.place(x=23, y=75, width=1300, height=600)

        # ===================Top_label=====================
        Top_frame=LabelFrame(main_frame, bd=0, bg="white",
                                font=("times new roman", 12, "bold"))
        Top_frame.place(x=5,y=0,width=1280,height=120)
        #===================select_for_txt=================
        conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password, database=self.db.database, port=self.db.port)
        my_cursor = conn.cursor()
        #========student==========
        my_cursor.execute("select count(*) from student")
        count_st = my_cursor.fetchone()
        self.student.set(count_st[0])
        #=======attendance========
        my_cursor.execute("select count(*) from attendance")
        count_att=my_cursor.fetchone()
        self.att.set(count_att[0])
        #=======đi muộn=============
        my_cursor.execute("select  count(Student_id) from attendance where AttendanceStatus like '%Đi muộn%'")
        count_late = my_cursor.fetchone()
        self.late.set(count_late[0])
        #========không điểm danh=======
        #not_in_attendance_table
        my_cursor.execute("select count(student.Student_id) from student,lesson,class where "
                          "student.Class=class.Class and class.Class=lesson.Class  "
                          "and CONCAT(student.Student_id,Lesson_id) not in (select CONCAT(Student_id,Lesson_id) from attendance) "
                          "and STR_TO_DATE(Date,'%d/%m/%Y')<=STR_TO_DATE(%s, '%d/%m/%Y')",(self.today_time,))
        count_noatt = my_cursor.fetchone()
        #có điểm danh nhưng điểm danh quá muộn giờ học
        my_cursor.execute("select  count(Student_id) from attendance where AttendanceStatus like '%Vắng%'")
        count_noatt1 = my_cursor.fetchone()


        a=int(count_noatt[0])+int(count_noatt1[0])
        self.noatt.set(a)
        conn.commit()
        conn.close()

        #student_frame
        student_frame=LabelFrame(Top_frame,bd=1,bg='#27a9e3')
        student_frame.place(x=5,y=0,width=315,height=110)

        img_student = PIL.Image.open(r"ImageFaceDetect\sv.png")
        # img_student = img_student.resize((50, 50), PIL.Image.ANTIALIAS)
        self.photoimgsv = ImageTk.PhotoImage(img_student)
        student_img = Label(student_frame, image=self.photoimgsv, bg="#27a9e3")
        student_img.place(x=20, y=40, width=50, height=50)
        student_text=Label(student_frame,text="Số Học sinh",font=("times new roman", 18, "bold"),fg="white",bg="#27a9e3")
        student_text.place(x=100,y=30)
        student_text = Label(student_frame,textvariable=self.student, font=("times new roman", 15, "bold"),fg="white",bg="#27a9e3")
        student_text.place(x=100, y=70)

        #attendance_success
        att_frame = LabelFrame(Top_frame, bd=1, bg='#28b779')
        att_frame.place(x=335, y=0, width=315, height=110)

        img_att = PIL.Image.open(r"ImageFaceDetect\sodd.png")
        img_att = img_att.resize((50, 50), PIL.Image.LANCZOS)
        self.photoimgatt = ImageTk.PhotoImage(img_att)
        att_img = Label(att_frame, image=self.photoimgatt, bg="#28b779")
        att_img.place(x=20, y=40, width=50, height=50)
        att_text = Label(att_frame, text="Số bản điểm danh", font=("times new roman", 18, "bold"), fg="white",
                             bg="#28b779")
        att_text.place(x=100, y=30)
        att_text = Label(att_frame, textvariable=self.att, font=("times new roman", 15, "bold"), fg="white",
                             bg="#28b779")
        att_text.place(x=100, y=70)

        #late_attendance
        late_frame = LabelFrame(Top_frame, bd=1, bg='#852b99')
        late_frame.place(x=665, y=0, width=315, height=110)

        img_late = PIL.Image.open(r"ImageFaceDetect\late.png")
        # img_student = img_student.resize((50, 50), PIL.Image.ANTIALIAS)
        self.photoimglate = ImageTk.PhotoImage(img_late)
        late_img = Label(late_frame, image=self.photoimglate, bg="#852b99")
        late_img.place(x=20, y=40, width=50, height=50)
        late_text = Label(late_frame, text="Số lần đi muộn", font=("times new roman", 18, "bold"), fg="white",
                         bg="#852b99")
        late_text.place(x=100, y=30)
        late_text = Label(late_frame, textvariable=self.late, font=("times new roman", 15, "bold"), fg="white",
                         bg="#852b99")
        late_text.place(x=100, y=70)

        #no_attendance
        late_frame = LabelFrame(Top_frame, bd=1, bg='#DC143C')
        late_frame.place(x=990, y=0, width=315, height=110)

        img_noatt = PIL.Image.open(r"ImageFaceDetect\vang.png")
        # img_student = img_student.resize((50, 50), PIL.Image.ANTIALIAS)
        self.photoimgnoatt = ImageTk.PhotoImage(img_noatt)
        noatt_img = Label(late_frame, image=self.photoimgnoatt, bg="#DC143C")
        noatt_img.place(x=20, y=40, width=50, height=50)
        noatt_text = Label(late_frame, text="Số lần vắng", font=("times new roman", 18, "bold"), fg="white",
                          bg="#DC143C")
        noatt_text.place(x=100, y=30)
        noatt_text = Label(late_frame, textvariable=self.noatt, font=("times new roman", 15, "bold"), fg="white",
                          bg="#DC143C")
        noatt_text.place(x=100, y=70)

        #====================Left_label====================
        Left_frame = LabelFrame(main_frame, bd=2, bg="white",
                               font=("times new roman", 12, "bold"))
        Left_frame.place(x=10, y=125, width=645, height=470)
        #danh sách hs đi muộn
        self.late_group=LabelFrame(Left_frame,bd=1,bg="white",text="Học sinh đi muộn",font=("times new roman", 11, "bold"),fg="black",relief=RIDGE)
        self.late_group.place(x=0,y=0,width=630,height=220)

        self.var_com_searchlate = StringVar()#biến chọn loại tìm kiếm
        search_combo = ttk.Combobox(self.late_group, font=("times new roman", 11, "bold"),
                                    textvariable=self.var_com_searchlate,
                                    state="read only",
                                    width=11)
        search_combo["values"] = ("ID Học sinh", "Ngày","ID Buổi học","Lớp")
        search_combo.current(0)
        search_combo.bind("<<ComboboxSelected>>", self.callbackLate)
        search_combo.grid(row=0, column=0, padx=10, pady=5, sticky=W)

        self.var_searchlate = StringVar()#biến giá trị tìm kiếm
        self.searchtc_entry = ttk.Entry(self.late_group, textvariable=self.var_searchlate, width=13,
                                   font=("times new roman", 10, "bold"))
        self.searchtc_entry.grid(row=0, column=1, padx=5, pady=0, sticky=W)
        
        #nút tìm kiếm
        img_btn3 = PIL.Image.open(r"ImageFaceDetect\btnRed.png")
        img_btn3 = img_btn3.resize((80, 30), PIL.Image.LANCZOS)
        self.photobtn3 = ImageTk.PhotoImage(img_btn3)
        searchtc_btn = Button(self.late_group, text="Tìm kiếm",
                              font=("times new roman", 10, "bold"), command=self.search_Latedata,
                              bd=0, bg="white", cursor='hand2', activebackground='white',
                              width=80, image=self.photobtn3, fg="white", compound="center")
        searchtc_btn.grid(row=0, column=2, padx=5)
        
        #Xem tất cả hs đi muộn
        showAlltc_btn = Button(self.late_group, text="Xem tất cả",
                               font=("times new roman", 10, "bold"),command=self.fetch_Latedata,
                               bd=0, bg="white", cursor='hand2', activebackground='white',
                               width=80, image=self.photobtn3, fg="white", compound="center"
                               )
        showAlltc_btn.grid(row=0, column=3, padx=5)
        
        #xuất ra file csv 
        exportLate_btn = Button(self.late_group, text="Xuất CSV",
                               font=("times new roman", 10, "bold"), command=self.exportCsv,
                                bd=0, bg="white", cursor='hand2', activebackground='white',
                                width=80, image=self.photobtn3, fg="white", compound="center")
        exportLate_btn.grid(row=0, column=4, padx=10)

        # bảng dữ liệu các học sinh đi muộn
        tabletc_frame = Frame(self.late_group, bd=2, relief=RIDGE, bg="white")
        tabletc_frame.place(x=10, y=38, width=600, height=155)

        # scroll bar
        scroll_x = ttk.Scrollbar(tabletc_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(tabletc_frame, orient=VERTICAL)
        
        #các trường dữ liệu
        self.LateTable = ttk.Treeview(tabletc_frame, column=(
            "studentid", "name","class","date","lessonid", "status"),
                                         xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.LateTable.xview)
        scroll_y.config(command=self.LateTable.yview)
        
        #gán tên cấc cột
        self.LateTable.heading("studentid", text="ID SV")
        self.LateTable.heading("name", text="Tên Học sinh")
        self.LateTable.heading("class", text="Lớp học")
        self.LateTable.heading("date", text="Ngày")

        self.LateTable.heading("lessonid", text="ID Buổi học")
        self.LateTable.heading("status", text="Trạng thái")
        
        #độ dài các cột
        self.LateTable["show"] = "headings"
        self.LateTable.column("studentid", width=100)
        self.LateTable.column("name", width=100)
        self.LateTable.column("date", width=100)
        self.LateTable.column("class", width=100)

        self.LateTable.column("lessonid", width=100)
        self.LateTable.column("status", width=100)

        self.LateTable.pack(fill=BOTH, expand=1)
        
        #hàm hiển thị tất cả hs đi muộn
        self.fetch_Latedata()

        #===========under-left===============
        #danh sách học sinh vắng= có điểm danh nhưng đi quá muộn
        self.noatt_group = LabelFrame(Left_frame, bd=1, bg="white", text="Học sinh vắng",
                                font=("times new roman", 10, "bold"), fg="black", relief=RIDGE)
        self.noatt_group.place(x=0, y=235, width=630, height=220)

        self.var_com_searchnoatt = StringVar()#biến loại điểm danh
        search_combo1 = ttk.Combobox(self.noatt_group, font=("times new roman", 10, "bold"),
                                    textvariable=self.var_com_searchnoatt,
                                    state="read only",
                                    width=12)
        search_combo1["values"] = ("ID Học sinh", "Ngày","ID Buổi học","Lớp")
        search_combo1.current(0)
        search_combo1.bind("<<ComboboxSelected>>", self.callbackTooLate)
        search_combo1.grid(row=0, column=0, padx=10, pady=5, sticky=W)

        self.var_searchnoatt = StringVar()#biến giá trị tìm kiếm
        self.searchnoatt_entry = ttk.Entry(self.noatt_group, textvariable=self.var_searchnoatt, width=13,
                                   font=("times new roman", 10, "bold"))
        self.searchnoatt_entry.grid(row=0, column=1, padx=5, pady=0, sticky=W)

        searchnoatt_btn = Button(self.noatt_group, text="Tìm kiếm",
                              font=("times new roman", 10, "bold"),command=self.search_Notdata,
                                 bd=0, bg="white", cursor='hand2', activebackground='white',
                                 width=80, image=self.photobtn3, fg="white", compound="center")
        searchnoatt_btn.grid(row=0, column=2, padx=5)

        showAllnoatt_btn = Button(self.noatt_group, text="Xem tất cả",
                               font=("times new roman", 10, "bold"),command=self.fetch_Notdata,
                                  bd=0, bg="white", cursor='hand2', activebackground='white',
                                  width=80, image=self.photobtn3, fg="white", compound="center")
        showAllnoatt_btn.grid(row=0, column=3, padx=5)

        exportNoatt_btn = Button(self.noatt_group, text="Xuất CSV",
                                font=("times new roman", 10, "bold"), command=self.exportUnpresetCsv,
                                 bd=0, bg="white", cursor='hand2', activebackground='white',
                                 width=80, image=self.photobtn3, fg="white", compound="center")
        exportNoatt_btn.grid(row=0, column=4, padx=10)

        # table_frame
        tableatt_frame = Frame(self.noatt_group, bd=2, relief=RIDGE, bg="white")
        tableatt_frame.place(x=10, y=38, width=600, height=155)

        # scroll bar
        scroll_x = ttk.Scrollbar(tableatt_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(tableatt_frame, orient=VERTICAL)

        self.NoAttTable = ttk.Treeview(tableatt_frame, column=(
            "studentid", "name","class", "date", "lessonid", "status"),
                                      xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.NoAttTable.xview)
        scroll_y.config(command=self.NoAttTable.yview)

        self.NoAttTable.heading("studentid", text="ID SV")
        self.NoAttTable.heading("name", text="Tên Học sinh")
        self.NoAttTable.heading("class", text="Lớp")
        self.NoAttTable.heading("date", text="Ngày")

        self.NoAttTable.heading("lessonid", text="ID Buổi học")
        self.NoAttTable.heading("status", text="Trạng thái")

        self.NoAttTable["show"] = "headings"
        self.NoAttTable.column("studentid", width=100)
        self.NoAttTable.column("name", width=100)
        self.NoAttTable.column("class", width=100)
        self.NoAttTable.column("date", width=100)

        self.NoAttTable.column("lessonid", width=100)
        self.NoAttTable.column("status", width=100)

        self.NoAttTable.pack(fill=BOTH, expand=1)
        self.fetch_Notdata()
        # self.LateTable.bind("<ButtonRelease>", self.get_cursorLate)

        #===================right_label====================
        #danh sách sinh viên ko điểm danh (ko đi qua camera)
        Right_frame = LabelFrame(main_frame, bd=2, bg="white",
                                font=("times new roman", 12, "bold"))
        Right_frame.place(x=670, y=125, width=615, height=470)

        noatt_lbl = Label(Right_frame, bd=0, bg="white", text="Học sinh không điểm danh", font=("times new roman", 12, "bold"),
                         fg="red2", )
        noatt_lbl.place(x=0, y=0, width=600, height=30)

        self.notinGroup=LabelFrame(Right_frame,bd=0,bg="white")
        self.notinGroup.place(x=0,y=35,width=600,height=420)
        self.var_com_searchNotin = StringVar()#biến loại tìm kiếm
        search_combo2 = ttk.Combobox(self.notinGroup, font=("times new roman", 12, "bold"),
                                    textvariable=self.var_com_searchNotin,
                                    state="read only",
                                    width=12)
        search_combo2["values"] = ("ID Học sinh", "Ngày", "ID Buổi học","Lớp")
        search_combo2.current(0)
        search_combo2.bind("<<ComboboxSelected>>", self.callbackAbsent)#sự kiện khi chọn loại tìm kiếm
        search_combo2.grid(row=0, column=0, padx=10, pady=5, sticky=W)

        self.var_searchNotin = StringVar()
        self.searchtc_entry = ttk.Entry(self.notinGroup, textvariable=self.var_searchNotin, width=13,
                                   font=("times new roman", 11, "bold"))
        self.searchtc_entry.grid(row=0, column=1, padx=5, pady=0, sticky=W)
        #btn tìm
        img_btn2 = PIL.Image.open(r"ImageFaceDetect\btnRed.png")
        img_btn2 = img_btn2.resize((100, 30), PIL.Image.LANCZOS)
        self.photobtn2 = ImageTk.PhotoImage(img_btn2)
        searchtc_btn = Button(self.notinGroup, text="Tìm kiếm",
                              font=("times new roman", 11, "bold"),
                              command=self.search_Notindata,
                              bd=0, bg="white", cursor='hand2', activebackground='white',
                              width=100, image=self.photobtn2, fg="white", compound="center")
        searchtc_btn.grid(row=0, column=2, padx=5)

        showAlltc_btn = Button(self.notinGroup, text="Xem tất cả",
                               font=("times new roman", 11, "bold"), command=self.fetch_Notindata,
                               bd=0, bg="white", cursor='hand2', activebackground='white',
                               width=100, image=self.photobtn2, fg="white", compound="center")
        showAlltc_btn.grid(row=0, column=3, padx=5)

        exportLate_btn = Button(self.notinGroup, text="Xuất CSV",
                                font=("times new roman", 11, "bold"), command=self.exportNotinCsv,
                                bd=0, bg="white", cursor='hand2', activebackground='white',
                                width=100, image=self.photobtn2, fg="white", compound="center")
        exportLate_btn.grid(row=0, column=4, padx=5)

        # table_frame
        tablenotin_frame = Frame(self.notinGroup, bd=2, relief=RIDGE, bg="white")
        tablenotin_frame.place(x=10, y=38, width=585, height=375)

        # scroll bar
        scroll_x = ttk.Scrollbar(tablenotin_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(tablenotin_frame, orient=VERTICAL)

        self.NotInTable = ttk.Treeview(tablenotin_frame, column=(
            "studentid", "name","class", "date", "lessonid","status"),
                                      xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.NotInTable.xview)
        scroll_y.config(command=self.NotInTable.yview)

        self.NotInTable.heading("studentid", text="ID SV")
        self.NotInTable.heading("name", text="Tên Học sinh")
        self.NotInTable.heading("class", text="Lớp")
        self.NotInTable.heading("date", text="Ngày")
        self.NotInTable.heading("lessonid", text="ID Buổi học")
        self.NotInTable.heading("status", text="Trạng thái")


        self.NotInTable["show"] = "headings"
        self.NotInTable.column("studentid", width=100)
        self.NotInTable.column("name", width=100)
        self.NotInTable.column("class", width=100)
        self.NotInTable.column("date", width=100)

        self.NotInTable.column("lessonid", width=100)


        self.NotInTable.pack(fill=BOTH, expand=1)
        self.fetch_Notindata()


    def callbackLate(self,event):#hàm chuyển đổi txtbox khi chọn loại điểm danh
        mls = event.widget.get()
        if(mls=='Ngày'):#loại điểm danh là theo Ngày thì chuyển về dạng DateEntry
            self.searchtc_entry=DateEntry(self.late_group, width=13, bd=0, selectmode='day',textvariable=self.var_searchlate,
                  year=int(strftime("%Y")), month=int(strftime("%m")), font=("times new roman", 10),
                  day=int(strftime("%d")), date_pattern='dd/mm/yyyy')
            self.searchtc_entry.grid(row=0, column=1, padx=5, pady=0, sticky=W)


        else:
            self.searchtc_entry = ttk.Entry(self.late_group, textvariable=self.var_searchlate, width=14,
                                        font=("times new roman", 10, "bold"))
            self.searchtc_entry.grid(row=0, column=1, padx=5, pady=0, sticky=W)
            self.var_searchlate.set("")
            
    def callbackTooLate(self,event1):#hàm chuyển đổi txtbox khi chọn loại điểm danh
        mls = event1.widget.get()
        if(mls=='Ngày'):#loại điểm danh là theo Ngày thì chuyển về dạng DateEntry
            self.searchnoatt_entry=DateEntry(self.noatt_group, width=13, bd=0, selectmode='day',textvariable=self.var_searchnoatt,
                  year=int(strftime("%Y")), month=int(strftime("%m")), font=("times new roman", 10),
                  day=int(strftime("%d")), date_pattern='dd/mm/yyyy')
            self.searchnoatt_entry.grid(row=0, column=1, padx=5, pady=0, sticky=W)


        else:
            self.searchnoatt_entry = ttk.Entry(self.noatt_group, textvariable=self.var_searchnoatt, width=14,
                                        font=("times new roman", 10, "bold"))
            self.searchnoatt_entry.grid(row=0, column=1, padx=5, pady=0, sticky=W)
            self.var_searchnoatt.set("")
    
    #ko điểm danh
    def callbackAbsent(self,event1):#hàm chuyển đổi txtbox khi chọn loại điểm danh
        mls = event1.widget.get()
        if(mls=='Ngày'):#loại điểm danh là theo Ngày thì chuyển về dạng DateEntry
            self.searchtc_entry=DateEntry(self.notinGroup, width=14, bd=0, selectmode='day',textvariable=self.var_searchNotin,
                  year=int(strftime("%Y")), month=int(strftime("%m")), font=("times new roman", 10),
                  day=int(strftime("%d")), date_pattern='dd/mm/yyyy')
            self.searchtc_entry.grid(row=0, column=1, padx=5, pady=0, sticky=W)


        else:
            self.searchtc_entry = ttk.Entry(self.notinGroup, textvariable=self.var_searchNotin, width=15,
                                        font=("times new roman", 10, "bold"))
            self.searchtc_entry.grid(row=0, column=1, padx=5, pady=0, sticky=W)
            self.var_searchNotin.set("")

        

    def fetch_Latedata(self):
            # global mydata
            mydata.clear()
            conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password, database=self.db.database, port=self.db.port)
            my_cursor = conn.cursor()
            my_cursor.execute("select DISTINCT student.Student_id,student.`Name`,student.Class,attendance.Date,lesson.Lesson_id,AttendanceStatus from attendance,lesson,student where   "
                              "AttendanceStatus like '%Đi muộn%' and  attendance.Lesson_id=lesson.Lesson_id and attendance.Student_id=student.Student_id")
            data = my_cursor.fetchall()
            if len(data) != 0:
                self.LateTable.delete(*self.LateTable.get_children())
                for i in data:
                    self.LateTable.insert("", END, values=i)
                    mydata.append(i)
                conn.commit()
            conn.close()
    def search_Latedata(self):
        if self.var_com_searchlate.get()=="" or self.var_searchlate.get()=="":
            messagebox.showerror("Lỗi !","Vui lòng nhập thông tin đầy đủ",parent=self.root)

        else:
            print(self.var_searchlate.get())
            try:
                conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password, database=self.db.database, port=self.db.port)
                my_cursor = conn.cursor()#"ID Điểm Danh", "Ngày", "ID Học sinh"
                if(self.var_com_searchlate.get()=="ID Học sinh"):
                    self.var_com_searchlate.set("student.Student_id")
                elif(self.var_com_searchlate.get()=="Ngày"):
                    self.var_com_searchlate.set("attendance.Date")
                elif (self.var_com_searchlate.get() == "Lớp"):
                    self.var_com_searchlate.set("student.Class")
                else:
                    if(self.var_com_searchlate.get()=="ID Buổi học"):
                        self.var_com_searchlate.set("lesson.Lesson_id")

                mydata.clear()
                my_cursor.execute("select DISTINCT student.Student_id,student.`Name`,student.Class,attendance.Date,lesson.Lesson_id,AttendanceStatus from attendance,lesson,student where   AttendanceStatus like '%Đi muộn%' "
                                  "and  attendance.Lesson_id=lesson.Lesson_id "
                                  "and attendance.Student_id=student.Student_id and  "
                                  +str(self.var_com_searchlate.get())+" Like '%"+str(self.var_searchlate.get())+"%'")
                data=my_cursor.fetchall()
                if(len(data)!=0):
                    self.LateTable.delete(*self.LateTable.get_children())
                    for i in data:
                        self.LateTable.insert("",END,values=i)
                        mydata.append(i)
                    messagebox.showinfo("Thông báo","Có "+str(len(data))+" bản ghi thỏa mãn điều kiện",parent=self.root)
                    conn.commit()
                else:
                    self.LateTable.delete(*self.LateTable.get_children())
                    messagebox.showinfo("Thông báo", " Không có bản ghi nào thỏa mãn điều kiện",parent=self.root)
                conn.close()
            except Exception as es:
                messagebox.showerror("Lỗi", f"Due To:{str(es)}", parent=self.root)
    def exportCsv(self):
        try:
            # Current GMT time in a tuple format
            current_GMT = time.gmtime()

            # ts stores timestamp
            ts = calendar.timegm(current_GMT)
            if len(mydata)<1:
                messagebox.showerror("Không có dữ liệu","Không có dữ liệu để xuất file",parent=self.root)
                return  False

            df = pd.DataFrame(mydata,
                              columns=['ID Học sinh', 'Tên Học sinh', 'Lớp', 'Ngày', 'ID Buổi học','Trạng thái'])

            writer = pd.ExcelWriter(
                './Attendance_CSV/ds_dimuon_' + str(ts) + '_' + str(
                    self.today) + '.xlsx', engine='xlsxwriter')

            df.to_excel(writer, sheet_name='ds', index=False, header=True)

            writer.close()

            messagebox.showinfo("Xuất Dữ Liệu", "Dữ liệu của bạn đã được xuất đến thư mục Attendance_CSV")
        except Exception as es:
            messagebox.showerror("Lỗi", f"Due To:{str(es)}", parent=self.root)

    #===================No ATT=========================
    def fetch_Notdata(self):
            # global mydata
            mydataNot.clear()
            conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password, database=self.db.database, port=self.db.port)
            my_cursor = conn.cursor()
            my_cursor.execute("select DISTINCT student.Student_id,student.`Name`,student.Class,attendance.Date,lesson.Lesson_id,AttendanceStatus from attendance,lesson,student where   "
                              "AttendanceStatus like '%Vắng%' and  attendance.Lesson_id=lesson.Lesson_id and attendance.Student_id=student.Student_id")
            data = my_cursor.fetchall()
            if len(data) != 0:
                self.NoAttTable.delete(*self.NoAttTable.get_children())
                for i in data:
                    self.NoAttTable.insert("", END, values=i)
                    mydataNot.append(i)
                conn.commit()
            conn.close()
    def search_Notdata(self):
        if self.var_com_searchnoatt.get()=="" or self.var_searchnoatt.get()=="":
            messagebox.showerror("Lỗi !","Vui lòng nhập thông tin đầy đủ",parent=self.root)

        else:
            print(self.var_searchnoatt.get())
            try:
                conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password, database=self.db.database, port=self.db.port)
                my_cursor = conn.cursor()#"ID Điểm Danh", "Ngày", "ID Học sinh"
                if(self.var_com_searchnoatt.get()=="ID Học sinh"):
                    self.var_com_searchnoatt.set("student.Student_id")
                elif(self.var_com_searchnoatt.get()=="Ngày"):
                    self.var_com_searchnoatt.set("attendance.Date")
                elif (self.var_com_searchnoatt.get() == "Lớp"):
                    self.var_com_searchnoatt.set("student.class")
                else:
                    if(self.var_com_searchnoatt.get()=="ID Buổi học"):
                        self.var_com_searchnoatt.set("lesson.Lesson_id")

                mydataNot.clear()
                my_cursor.execute("select DISTINCT student.Student_id,student.`Name`,student.Class,attendance.Date,lesson.Lesson_id,AttendanceStatus from attendance,lesson,student where   "
                              "AttendanceStatus like '%Vắng%' and  attendance.Lesson_id=lesson.Lesson_id and attendance.Student_id=student.Student_id and "
                                  +str(self.var_com_searchnoatt.get())+" Like '%"+str(self.var_searchnoatt.get())+"%'")
                data=my_cursor.fetchall()
                if(len(data)!=0):
                    self.NoAttTable.delete(*self.NoAttTable.get_children())
                    for i in data:
                        self.NoAttTable.insert("",END,values=i)
                        mydataNot.append(i)
                    messagebox.showinfo("Thông báo","Có "+str(len(data))+" bản ghi thỏa mãn điều kiện",parent=self.root)
                    conn.commit()
                else:
                    self.NoAttTable.delete(*self.NoAttTable.get_children())
                    messagebox.showinfo("Thông báo", " Không có bản ghi nào thỏa mãn điều kiện",parent=self.root)
                conn.close()
            except Exception as es:
                messagebox.showerror("Lỗi", f"Due To:{str(es)}", parent=self.root)
    def exportUnpresetCsv(self):
        try:
            # Current GMT time in a tuple format
            current_GMT = time.gmtime()

            # ts stores timestamp
            ts = calendar.timegm(current_GMT)
            if len(mydataNot)<1:
                messagebox.showerror("Không có dữ liệu","Không có dữ liệu để xuất file",parent=self.root)
                return  False
            df = pd.DataFrame(mydataNot,
                              columns=['ID Học sinh', 'Tên Học sinh', 'Lớp', 'Ngày', 'ID Buổi học','Trạng thái'])

            writer = pd.ExcelWriter(
                './Attendance_CSV/ds_diemdanh_vang_' + str(ts) + '_' + str(
                    self.today) + '.xlsx', engine='xlsxwriter')

            df.to_excel(writer, sheet_name='ds', index=False, header=True)

            writer.close()

            messagebox.showinfo("Xuất Dữ Liệu", "Dữ liệu của bạn đã được xuất đến thư mục Attendance_CSV")

        except Exception as es:
            messagebox.showerror("Lỗi", f"Due To:{str(es)}", parent=self.root)

    #===========================NOT IN ATT============================
    def fetch_Notindata(self):
            # global mydata
            mydataNotInAtt.clear()
            conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password, database=self.db.database, port=self.db.port)
            my_cursor = conn.cursor()

            my_cursor.execute("select distinct(student.Student_id),student.Name,student.class,Date,class.Class,Lesson_id from student,lesson,class "
                              "where student.Class=class.Class and class.Class=lesson.Class "
                              "and CONCAT(student.Student_id,Lesson_id) not in (select CONCAT(Student_id,Lesson_id) from attendance) "
                              "and STR_TO_DATE(Date,'%d/%m/%Y')<=STR_TO_DATE(%s, '%d/%m/%Y')",(self.today_time,))
            data = my_cursor.fetchall()
            if len(data) != 0:
                self.NotInTable.delete(*self.NotInTable.get_children())
                for i in data:
                    self.NotInTable.insert("", END, values=i)
                    mydataNotInAtt.append(i)
                conn.commit()
            conn.close()
    def search_Notindata(self):
        if self.var_com_searchNotin.get()=="" or self.var_searchNotin.get()=="":
            messagebox.showerror("Lỗi !","Vui lòng nhập thông tin đầy đủ",parent=self.root)

        else:
            try:
                conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password, database=self.db.database, port=self.db.port)
                my_cursor = conn.cursor()#"ID Điểm Danh", "Ngày", "ID Học sinh"
                if(self.var_com_searchNotin.get()=="ID Học sinh"):
                    self.var_com_searchNotin.set("student.Student_id")
                elif(self.var_com_searchNotin.get()=="Ngày"):
                    self.var_com_searchNotin.set("Date")

                elif (self.var_com_searchNotin.get() == "Lớp"):
                    self.var_com_searchNotin.set("student.class")
                else:
                    if(self.var_com_searchNotin.get()=="ID Buổi học"):
                        self.var_com_searchNotin.set("Lesson_id")

                mydataNotInAtt.clear()
                my_cursor.execute("select distinct(student.Student_id),student.Name,student.class,Date,class.Class,Lesson_id from student,lesson,class where "
                                  "student.Class=class.Class and class.Class=lesson.Class"
                              " and CONCAT(student.Student_id,Lesson_id) not in (select CONCAT(Student_id,Lesson_id) from attendance) and "
                              "STR_TO_DATE(Date,'%d/%m/%Y')<=STR_TO_DATE(%s, '%d/%m/%Y') and "
                              +str(self.var_com_searchNotin.get())+" Like '%"+str(self.var_searchNotin.get())+"%'",(self.today_time,))
                data=my_cursor.fetchall()
                if(len(data)!=0):
                    self.NotInTable.delete(*self.NotInTable.get_children())
                    for i in data:
                        self.NotInTable.insert("",END,values=i)
                        mydataNotInAtt.append(i)
                    messagebox.showinfo("Thông báo","Có "+str(len(data))+" bản ghi thỏa mãn điều kiện",parent=self.root)
                    conn.commit()
                else:
                    self.NotInTable.delete(*self.NotInTable.get_children())
                    messagebox.showinfo("Thông báo", " Không có bản ghi nào thỏa mãn điều kiện",parent=self.root)
                conn.close()
            except Exception as es:
                messagebox.showerror("Lỗi", f"Due To:{str(es)}", parent=self.root)
    def exportNotinCsv(self):
        try:
            # Current GMT time in a tuple format
            current_GMT = time.gmtime()

            # ts stores timestamp
            ts = calendar.timegm(current_GMT)

            if len(mydataNotInAtt)<1:
                messagebox.showerror("Không có dữ liệu","Không có dữ liệu để xuất file",parent=self.root)
                return  False
            df = pd.DataFrame(mydataNotInAtt,columns= ['ID Học sinh', 'Tên Học sinh','Lớp','Ngày','Lớp học','ID Buổi học'])

            writer=pd.ExcelWriter('./Attendance_CSV/ds_khong_diemdanh_'+str(ts)+'_'+str(self.today)+'.xlsx',engine='xlsxwriter')

            df.to_excel(writer,sheet_name='ds',index = False, header=True)

            writer.close()

            messagebox.showinfo("Xuất Dữ Liệu","Dữ liệu của bạn đã được xuất đến thư mục Attendance_CSV")
        except Exception as es:
            messagebox.showerror("Lỗi", f"Due To:{str(es)}", parent=self.root)
if __name__=="__main__":
    root=Tk() #khoi tao cua so va gan root vao
    obj=Report(root)
    root.mainloop()# cua so hien len