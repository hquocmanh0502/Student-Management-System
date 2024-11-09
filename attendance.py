import os
from tkinter import *
from tkinter import ttk
import PIL.Image
import PIL.ImageTk
import random
from tkinter import messagebox
import mysql.connector
import numpy as np
import pandas as pd
from PIL import Image, ImageTk
import cv2
import calendar
import time

from datetime import datetime
from time import strftime
import csv
from tkinter import filedialog
from database_str import Database_str

import sys

mydata=[]# mảng data
class Attendance:

    def __init__(self,root):
        self.root=root
        w = 1350#chiều dài giao diện
        h = 700#chiều rộng giao diện

        ws = self.root.winfo_screenwidth()#độ dài màn hình
        hs = self.root.winfo_screenheight()#độ rộng màn
        x = (ws / 2) - (w / 2) #vị trí cách lề trái x px
        y = (hs / 2) - (h / 2) #vị trí cách lề trên y px

        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y)) #kích thước và vị trí hiển thị giao diện
        self.root.title("Quản lý điểm danh")#tiêu đề
        self.root.iconbitmap('ImageFaceDetect\\gaming.ico')#icon giao diện
        self.isClicked=False # biến đã chọn
        today = strftime("%d-%m-%Y")#ngày hôm nay
        self.today=strftime("%d-%m-%Y")
        
        self.db=Database_str()#thông tin kết nối database

        #===========variables=========
        self.var_atten_id=StringVar() #biến kiểu string(chuỗi ký tự) id điểm danh
        self.var_atten_class = StringVar()#lớp học
        self.var_atten_idsv = StringVar()#id học sinh
        self.var_atten_name = StringVar() #tên học sinh
        self.var_atten_timein = StringVar()#thời gian vào
        self.var_atten_timeout = StringVar()#thời gian ra
        self.var_atten_date = StringVar()#ngày
        self.var_atten_attendance = StringVar()#trạng thái
        self.var_atten_lesson=StringVar()#lesson id

        #ảnh nền resize
        img3 = PIL.Image.open(r"ImageFaceDetect\bgnt.png")#mở ảnh trong thư mục
        img3 = img3.resize((1350, 700), PIL.Image.LANCZOS)# chỉnh kích thước ảnh về 1350x700
        self.photoimg3 = ImageTk.PhotoImage(img3)#ép kiểu về ImageTk

        #khai báo label chứa ảnh nền
        bg_img = Label(self.root, image=self.photoimg3)
        bg_img.place(x=0, y=0, width=1350, height=700)#(x=0: cách lề trái 0px, y=0: cách lề trên 0px, width: chiều dài 1350px, height: chiều cao)

        # ==================================heading====================================
        # ====time====
        #hiển thị thời gian hiện tại
        #ảnh thời gian
        img_time = PIL.Image.open(r"ImageFaceDetect\timsearch50.png")#mở ảnh 
        img_time = img_time.resize((27, 27), PIL.Image.LANCZOS)#resize ảnh về kích thước 27x27
        self.photoimgtime = ImageTk.PhotoImage(img_time)
        time_img = Label(self.root, image=self.photoimgtime, bg="white")
        time_img.place(x=43, y=40, width=27, height=27)

        def time():#hàm thay đổi thời gian mỗi 1 giây
            string = strftime('%H:%M:%S %p')
            lbl.config(text=string)
            lbl.after(1000, time)

        lbl = Label(self.root, font=("times new roman", 11, "bold"), bg="white", fg="black")
        lbl.place(x=80, y=35, width=100, height=20)
        time()#chạy hàm time
        lbl1 = Label(self.root, text=today, font=("times new roman", 11, "bold"), bg="white", fg="black")
        lbl1.place(x=80, y=60, width=100, height=20)

        # ====title=========
        self.txt = "Quản lý thông tin điểm danh"
        self.count = 0
        # self.text = ''
        # self.color = ["#4f4e4d", "#f29844", "red2"]
        self.heading = Label(self.root, text=self.txt, font=("times new roman", 22, "bold"), bg="white", fg="black",
                             bd=5, relief=FLAT)
        self.heading.place(x=350, y=22, width=600)

        #frame chính và vị trí
        main_frame = Frame(bg_img, bd=2, bg="white")# nằm trong label bg_img, viền xung quanh 2px, bg: mầu nền trắng
        main_frame.place(x=24, y=90, width=1293, height=586)

        # frame bên trái chứa các label, entry textbox
        Left_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE,
                                font=("times new roman", 12, "bold"))
        Left_frame.place(x=10, y=5, width=390, height=580)

        # text cập nhật điiểm danh
        label_Update_att=Label(Left_frame,bg="#F0FFF0",fg="#483D8B",text="Cập Nhật điểm danh",font=("times new roman", 18, "bold"))
        label_Update_att.place(x=0, y=1, width=386, height=35)

        left_inside_frame = Frame(Left_frame, bd=1, bg="white")
        left_inside_frame.place(x=0, y=60, width=380, height=500)

        #id điểm danh
        auttendanceID_label = Label(left_inside_frame, text="ID Điểm Danh:", font=("times new roman", 12, "bold"),
                                bg="white")
        auttendanceID_label.grid(row=0, column=0, padx=20, pady=5, sticky=W)
        #entry để nhập id điểm danh
        auttendanceID_entry = ttk.Entry(left_inside_frame,textvariable=self.var_atten_id,
                                    font=("times new roman", 12, "bold"),state="readonly")
        auttendanceID_entry.grid(row=0, column=1, padx=20, pady=5, sticky=W)


        #id học sinh
        roll_label = Label(left_inside_frame, text="ID Học sinh:", font=("times new roman", 12, "bold"),
                                    bg="white")
        roll_label.grid(row=1, column=0, padx=20, pady=5, sticky=W)
        #nhập tên học sinh
        roll_entry = ttk.Entry(left_inside_frame, width=20,textvariable=self.var_atten_idsv,
                                        font=("times new roman", 12, "bold"),state="readonly")
        roll_entry.grid(row=1, column=1, padx=20, pady=5, sticky=W)



        #tên hs
        nameLabel = Label(left_inside_frame, text="Tên Học sinh:", font=("times new roman", 12, "bold"),
                                    bg="white")
        nameLabel.grid(row=2, column=0, padx=20, pady=5, sticky=W)

        nameLabel_entry = ttk.Entry(left_inside_frame, width=20,textvariable=self.var_atten_name,
                                        font=("times new roman", 12, "bold"),state="readonly")
        nameLabel_entry.grid(row=2, column=1, padx=20, pady=5, sticky=W)



        #lớp
        classLabel = Label(left_inside_frame, text="Lớp học:", font=("times new roman", 12, "bold"),
                                    bg="white")
        classLabel.grid(row=3, column=0, padx=20, pady=5, sticky=W)

        classLabel_entry = ttk.Entry(left_inside_frame, width=20,textvariable=self.var_atten_class,
                                        font=("times new roman", 12, "bold"),state="readonly")
        classLabel_entry.grid(row=3, column=1, padx=20, pady=5, sticky=W)

        #thời gian vào
        timeLabel = Label(left_inside_frame, text="Giờ vào:", font=("times new roman", 12, "bold"),
                                    bg="white")
        timeLabel.grid(row=4, column=0, padx=20, pady=5, sticky=W)

        timeLabel_entry = ttk.Entry(left_inside_frame, width=20,textvariable=self.var_atten_timein,
                                        font=("times new roman", 12, "bold"))
        timeLabel_entry.grid(row=4, column=1, padx=20, pady=5, sticky=W)

        # thời gian ra
        timeoutLabel = Label(left_inside_frame, text="Giờ ra:", font=("times new roman", 12, "bold"),
                          bg="white")
        timeoutLabel.grid(row=5, column=0, padx=20, pady=5, sticky=W)

        timeoutLabel_entry = ttk.Entry(left_inside_frame, width=20, textvariable=self.var_atten_timeout,
                                    font=("times new roman", 12, "bold"))
        timeoutLabel_entry.grid(row=5, column=1, padx=20, pady=5, sticky=W)

        #ngày
        dateLabel = Label(left_inside_frame, text="Ngày:", font=("times new roman", 12, "bold"),
                          bg="white")
        dateLabel.grid(row=6, column=0, padx=20, pady=5, sticky=W)

        dateLabel_entry = ttk.Entry(left_inside_frame, width=20,textvariable=self.var_atten_date,
                                    font=("times new roman", 12, "bold"),state="readonly")
        dateLabel_entry.grid(row=6, column=1, padx=20, pady=5, sticky=W)

        #trạng thái
        auttendanceLabel = Label(left_inside_frame, text="Điểm danh:", font=("times new roman", 12, "bold"),
                           bg="white")
        auttendanceLabel.grid(row=7, column=0,  padx=20, pady=5, sticky=W)

        self.atten_status=ttk.Entry(left_inside_frame    ,width=20,font=("times new roman", 12, "bold"),textvariable=self.var_atten_attendance)

        self.atten_status.grid(row=7,column=1,pady=5,padx=20)



        #id bài học
        lessonLabel = Label(left_inside_frame, text="ID Bài học:", font=("times new roman", 12, "bold"),
                                 bg="white")
        lessonLabel.grid(row=8, column=0, padx=20, pady=5, sticky=W)

        self.lesson = ttk.Entry(left_inside_frame, width=20, font=("times new roman", 12, "bold"),
                                         state="readonly", textvariable=self.var_atten_lesson)
        self.lesson.grid(row=8, column=1, pady=5, padx=20)



        # btn_frame
        #ảnh nút đỏ
        img_btn2 = PIL.Image.open(r"ImageFaceDetect\btnRed1.png")
        img_btn2 = img_btn2.resize((220, 35), PIL.Image.LANCZOS)
        self.photobtn2 = ImageTk.PhotoImage(img_btn2)
        #nút xem ảnh
        label_Update_att = Button(Left_frame, text="Xem ảnh",command=self.openImage,
                                 font=("times new roman", 12, "bold"),bd=0,bg="white",cursor='hand2' ,activebackground='white',
                        width=220,image=self.photobtn2,fg="white",compound="center")
        label_Update_att.place(x=80, y=480, width=220, height=35)
        #nút xóa ảnh
        update_btn = Button(Left_frame, text="Xóa", command=self.delete_data,
                            font=("times new roman", 12, "bold"),
                            bd=0, bg="white", cursor='hand2', activebackground='white',
                            width=220, image=self.photobtn2, fg="white", compound="center")
        update_btn.place(x=80, y=530,width=220,height=35 )

        #frame chứa các nút nhỏ
        img_btn1 = PIL.Image.open(r"ImageFaceDetect\btnRed1.png")
        img_btn1 = img_btn1.resize((150, 35), PIL.Image.LANCZOS)
        self.photobtn1 = ImageTk.PhotoImage(img_btn1)
        btn_frame = Frame(left_inside_frame, bg="white")
        btn_frame.place(x=0, y=320, width=400, height=105)

        #nhập file csv
        save_btn = Button(btn_frame, text="Nhập file CSV",command=self.importCsv ,font=("times new roman", 11, "bold"), bd=0,bg="white",cursor='hand2' ,activebackground='white',
                        width=150,image=self.photobtn1,fg="white",compound="center")
        save_btn.grid(row=9, column=0,padx=20)

        #xuất ra file csv
        update_btn = Button(btn_frame, text="Xuất file CSV",command=self.exportCsv, font=("times new roman", 11, "bold"),
                            bd=0, bg="white", cursor='hand2', activebackground='white',
                            width=150, image=self.photobtn1, fg="white", compound="center")
        update_btn.grid(row=9, column=1,padx=20)

        #cập nhật thông tin điểm danh
        delete_btn = Button(btn_frame, text="Cập nhật",command=self.update_data ,font=("times new roman", 11, "bold"),
                            bd=0, bg="white", cursor='hand2', activebackground='white',
                            width=150, image=self.photobtn1, fg="white", compound="center")
        delete_btn.grid(row=10, column=0,pady=10)

        #làm mới
        reset_btn = Button(btn_frame, text="Làm mới",command=self.reset_data, font=("times new roman", 11, "bold"),
                           bd=0, bg="white", cursor='hand2', activebackground='white',
                           width=150, image=self.photobtn1, fg="white", compound="center")
        reset_btn.grid(row=10, column=1,pady=10)




        #right_ label
        Right_frame = LabelFrame(main_frame, bd=2, bg="white",
                                 font=("times new roman", 12, "bold"))
        Right_frame.place(x=410, y=5, width=880, height=580)


        #text tìm kiếm theo
        self.var_com_search=StringVar()# biến loại tìm kếm(theo ngày,id điểm danh,..) kiểu string(chuỗi ký tự)
        search_label = Label(Right_frame, text="Tìm kiếm theo :", font=("times new roman", 11, "bold"),
                             bg="white")
        search_label.grid(row=0, column=0, padx=15, pady=5, sticky=W)

        #chọn loại tìm kiếm
        search_combo = ttk.Combobox(Right_frame, font=("times new roman", 11, "bold"),textvariable=self.var_com_search, state="read only",
                                    width=13)
        search_combo["values"] = ("ID Điểm Danh", "Ngày", "ID Học sinh","ID Buổi học")
        search_combo.current(0)
        search_combo.grid(row=0, column=1, padx=2, pady=15, sticky=W)

        self.var_search=StringVar()#biến string nhập tìm kiếm
        search_entry = ttk.Entry(Right_frame,textvariable=self.var_search, width=15, font=("times new roman", 11, "bold"))
        search_entry.grid(row=0, column=2, padx=15, pady=5, sticky=W)

        #nút tìm kiếm
        img_btn3 = PIL.Image.open(r"ImageFaceDetect\btnRed.png")
        img_btn3 = img_btn3.resize((110, 35), PIL.Image.LANCZOS)
        self.photobtn3 = ImageTk.PhotoImage(img_btn3)#ảnh nền màu đỏ bo tròn cho nút
        search_btn = Button(Right_frame,command=self.search_data, text="Tìm kiếm", font=("times new roman", 11, "bold"), bd=0,bg="white",cursor='hand2' ,activebackground='white',
                        width=110,image=self.photobtn3,fg="white",compound="center")# nằm trong Right_frame, command( hàm để chạy chức năng tìm kiếm),fg: màu chữ, compound: vị trí hiển thị của chữ
        search_btn.grid(row=0, column=3, padx=15)

        #nút hiển thị hôm nay( hiển thị dữ liệu hôm nay)
        Today_btn = Button(Right_frame, text="Hôm nay",command=self.today_data, font=("times new roman", 11, "bold"), bd=0,bg="white",cursor='hand2' ,activebackground='white',
                        width=110,image=self.photobtn3,fg="white",compound="center")
        Today_btn.grid(row=0, column=4, padx=15)

        #nút hiển thị tất cả dữ liệu
        showAll_btn = Button(Right_frame, text="Xem tất cả", command=self.fetch_data,font=("times new roman", 11, "bold"), bd=0,bg="white",cursor='hand2' ,activebackground='white',
                        width=110,image=self.photobtn3,fg="white",compound="center")
        showAll_btn.grid(row=0, column=5, padx=15)


        #bảng dữ liệu
        table_frame = Frame(Right_frame, bd=2, relief=RIDGE, bg="white")
        table_frame.place(x=5, y=55, width=860, height=510)

        #scroll bar
        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        self.AttendanceReportTable=ttk.Treeview(table_frame,column=("id","idsv","name","class","time_in","time_out","date","lesson","attendance"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.AttendanceReportTable.xview)
        scroll_y.config(command=self.AttendanceReportTable.yview)

        #đặt tên cột dữ liệu
        self.AttendanceReportTable.heading("id",text="AttendanceID")
        self.AttendanceReportTable.heading("idsv", text="ID Học sinh")
        self.AttendanceReportTable.heading("name", text="Tên Học sinh")
        self.AttendanceReportTable.heading("class", text="Lớp học")
        self.AttendanceReportTable.heading("time_in", text="Giờ vào")
        self.AttendanceReportTable.heading("time_out", text="Giờ ra")
        self.AttendanceReportTable.heading("date", text="Ngày")
        self.AttendanceReportTable.heading("attendance", text="Điểm danh")
        self.AttendanceReportTable.heading("lesson", text="ID Bài học")

        self.AttendanceReportTable["show"]="headings"#hiển thị tên cột lên bảng

        #cập nhật chiều dài các cột
        self.AttendanceReportTable.column("id",width=100)
        self.AttendanceReportTable.column("idsv", width=100)
        self.AttendanceReportTable.column("name", width=100)
        self.AttendanceReportTable.column("class", width=100)
        self.AttendanceReportTable.column("time_in", width=100)
        self.AttendanceReportTable.column("time_out", width=100)
        self.AttendanceReportTable.column("date", width=100)
        self.AttendanceReportTable.column("attendance", width=100)
        self.AttendanceReportTable.column("lesson", width=100)

        self.AttendanceReportTable.pack(fill=BOTH,expand=1)

        self.AttendanceReportTable.bind("<ButtonRelease>",self.get_cursor)# bắt sự kiện khi click vào bảng dữ liệu
        self.fetch_data()  # load du lieu len grid
        #================fetchData======================

        # =======================fetch-data========================
    #hàm lấy tất cả dữ liệu
    def fetch_data(self):
            # global mydata
            mydata.clear()#xóa dữ liệu trong mảng mydata
            conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password, database=self.db.database, port=self.db.port)#kết nối db

            my_cursor = conn.cursor()#dùng duyệt các câu lệnh 
            my_cursor.execute("Select * from attendance") #thực hiện câu lệnh 
            data = my_cursor.fetchall()#lấy tất cả kết quả của câu lệnh

            if len(data) != 0:#nếu có dữ liệu
                self.AttendanceReportTable.delete(*self.AttendanceReportTable.get_children())# xóa hết các phần tử cũ của bảng
                for i in data:#với mỗi dòng dữ liệu trong data

                    self.AttendanceReportTable.insert("", END, values=i)#thêm dữ liệu lên bảng
                    mydata.append(i)#truyền dữ liệu vào mảng


                conn.commit()#xác nhận
            conn.close()#đóng kết nối
    #update du lieu chuan hoa tren bang?:
    
    #import csv

    def importCsv(self):
        global mydata
        mydata.clear()
        fln=filedialog.askopenfilename(initialdir=os.getcwd(),title="Open CSV",filetypes=(("CSV File",".csv"),("ALL File","*.*")),parent=self.root)
        with open(fln) as myfile:
            csvread=csv.reader(myfile,delimiter=",")
            for i in csvread:
                mydata.append(i)
                print(mydata)
        self.fetchData(mydata)


    #xuất dữ liệu ra excel
    def exportCsv(self):
        try:
            # thời gian hiện tại GMT
            current_GMT = time.gmtime()

            # chuyển thời gian về dạng unix time
            ts = calendar.timegm(current_GMT)
            if len(mydata)<1:#nếu ko có dữ liệu trong bảng
                messagebox.showerror("Không có dữ liệu","Không có dữ liệu để xuất file",parent=self.root)#in thông báo
                return  False

            #tạo dataframe có các cột : mã điểm danh,Id,tên học sinh,....
            df = pd.DataFrame(mydata,
                              columns=['Mã Điểm danh', 'ID Học sinh', 'Tên Học sinh', 'Lớp biên chế', 'Giờ vào', 'Giờ ra', 'Ngày', 'ID Buổi học', 'Trạng thái'])

            #file excel để xuất dữ liệu
            writer = pd.ExcelWriter(
                'D:\ML_OpenCV\DiemDanhHs_App\Attendance_CSV\ds__diemdanh_' + str(ts) + '_' + str(
                    self.today) + '.xlsx', engine='xlsxwriter')

            #xuất dữ liệu ra excel (writer : file excel, sheet_name: tên sheet tạo trong excel, index=False: Bỏ số thứ tự,header=True: thêm tên cột)
            df.to_excel(writer, sheet_name='ds', index=False, header=True)

            #lưu
            writer.save()

            #thông báo
            messagebox.showinfo("Xuất Dữ Liệu", "Dữ liệu của bạn đã được xuất đến thư mục Attendance_CSV")


        except Exception as es:#nếu có lỗi hiện thông báo
            messagebox.showerror("Lỗi", f"Due To:{str(es)}", parent=self.root)


    def get_cursor(self,event=""):#hàm sự kiện click vào bảng
        cursor_row=self.AttendanceReportTable.focus()#chọn bảng
        content=self.AttendanceReportTable.item(cursor_row)
        rows=content['values']#lấy giá trị của dòng dữ liệu được click
        self.var_atten_id.set(rows[0])#set giá trị mã học sinh là vị trí 0 của mảng rows
        self.var_atten_idsv.set(rows[1])
        self.var_atten_name.set(rows[2])
        self.var_atten_class.set(rows[3])
        self.var_atten_timein.set(rows[4])
        self.var_atten_timeout.set(rows[5])
        self.var_atten_date.set(rows[6])
        self.var_atten_attendance.set(rows[8])
        self.var_atten_lesson.set(rows[7])

    def reset_data(self):#cài đặt lại các giá trị về rỗng
        self.var_atten_id.set("")
        self.var_atten_idsv.set("")
        self.var_atten_name.set("")
        self.var_atten_class.set("")
        self.var_atten_timein.set("")
        self.var_atten_timeout.set("")
        self.var_atten_date.set("")
        self.var_atten_attendance.set("Status")
        self.var_atten_lesson.set("Lesson")
    def update_data(self):#cập nhật dữ liệu
        if self.var_atten_lesson.get()=="Lesson" or self.var_atten_attendance.get()=="Status" or self.var_atten_id.get()=="":#nếu ko nhập đủ thông tin
            messagebox.showerror("Error","Vui lòng nhập đầy đủ thông tin",parent=self.root)
        else:
            try:
                Update=messagebox.askyesno("Update","Bạn có muốn cập nhật bản ghi này không?",parent=self.root)#hiện thông báo hỏi có muốn cập nhật
                if Update>0:#nếu chọn có
                    conn=mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password, database=self.db.database, port=self.db.port)#kết nói db
                    my_cursor = conn.cursor()

                    #thực hiện câu lệnh update 
                    my_cursor.execute("update attendance set Student_id=%s,Name=%s,Class=%s,Time_in=%s,Time_out=%s,Date=%s,AttendanceStatus=%s,"
                                      "Lesson_id=%s where IdAuttendance=%s",(
                                            self.var_atten_idsv.get(),
                                            self.var_atten_name.get(),
                                            self.var_atten_class.get(),
                                            self.var_atten_timein.get(),
                                            self.var_atten_timeout.get(),
                                            self.var_atten_date.get(),
                                            self.var_atten_attendance.get(),
                                            self.var_atten_lesson.get(),

                                            self.var_atten_id.get()
                                        ))
                else:#nếu ko chọn update 
                    if not Update:
                        return
                #thông báo thành công
                messagebox.showinfo("Thành công","Cập nhật thông tin điểm danh thành công",parent=self.root)
                conn.commit()
                self.fetch_data()
                conn.close()
            except Exception as es:
                messagebox.showerror("Lỗi",f"Due To:{str(es)}",parent=self.root)

    # Delete Function
    def delete_data(self):#hàm xóa dữ liệu
            if self.var_atten_id.get() == "":#nếu bỏ trống id điểm danh
                messagebox.showerror("Lỗi", "Không được bỏ trống ID ", parent=self.root)
            else:
                try:
                    delete = messagebox.askyesno("Xoá bản ghi", "Bạn có muốn xóa bản ghi này ?", parent=self.root)
                    if delete > 0:
                        conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password, database=self.db.database, port=self.db.port)
                        my_cursor = conn.cursor()
                        sql = "delete from attendance where IdAuttendance=%s"#câu lệnh xóa
                        val = (self.var_atten_id.get(),)#lấy id điểm danh
                        my_cursor.execute(sql, val)#thực hiện câu lệnh
                    else:
                        if not delete:
                            return
                    conn.commit()
                    # self.fetch_data()
                    conn.close()
                    messagebox.showinfo("Xóa", "Xóa bản ghi thành công", parent=self.root)
                    self.fetch_data()
                except Exception as es:
                    messagebox.showerror("Lỗi", f"Due To:{str(es)}", parent=self.root)
    def openImage(self):#hàm mở ảnh đã điểm danh
        if self.var_atten_id == "":
            messagebox.showerror("Lỗi", " Vui lòng chọn ID để xem ảnh", parent=self.root)


        elif(self.var_atten_timein.get()=='None' ):#nếu ko điểm danh vào
            if not os.path.exists("DiemDanhImage/ " + self.var_atten_id.get() +"Ra" +".jpg"):#nếu ko có ảnh điểm danh ra:
                messagebox.showerror("Lỗi", "Không tìm thấy ảnh điểm danh", parent=self.root)
            else:#nếu có ảnh điểm danh ra : hiển thị ảnh điểm danh ra
                img = cv2.imread("DiemDanhImage/ " + str(self.var_atten_id.get()) +"Ra"+ ".jpg")
                img = cv2.resize(img, (300, 300))
                cv2.imshow("Out of Class", img)#hiển thị ảnh

        elif(self.var_atten_timeout.get()=='None'):#nếu ko điểm danh ra
            if not os.path.exists("DiemDanhImage/ " + self.var_atten_id.get() + ".jpg"):#nếu khong có ảnh điểm danh vào
                messagebox.showerror("Lỗi", "Không tìm thấy ảnh điểm danh", parent=self.root)
            else:#nếu có ảnh điểm danh vào: hiển thị ảnh điểm danh vào
                img1=cv2.imread("DiemDanhImage/ " + str(self.var_atten_id.get()) + ".jpg")
                img1=cv2.resize(img1,(300,300))
                cv2.imshow("Into Class",img1)
        elif(self.var_atten_timein.get()!='None' and self.var_atten_timeout.get()!='None'):#nếu có cả ảnh điểm danh ra và vào
            img = cv2.imread("DiemDanhImage/ " + str(self.var_atten_id.get()) + "Ra" + ".jpg")
            img = cv2.resize(img, (300, 300))
            img1 = cv2.imread("DiemDanhImage/ " + str(self.var_atten_id.get()) + ".jpg")
            img1 = cv2.resize(img1, (300, 300))
            Hori = np.concatenate((img, img1), axis=1)#ghép 2 ảnh
            cv2.imshow("InAndOutClass", Hori)#hiển thị ảnh
        else:
            messagebox.showerror("Lỗi", "Không tìm thấy ảnh điểm danh", parent=self.root)

    def search_data(self):#hàm tìm kiếm điểm danh
        if self.var_com_search.get()=="" or self.var_search.get()=="":#nếu ko nhập đủ thông tin tìm kiếm
            messagebox.showerror("Lỗi !","Vui lòng nhập thông tin đầy đủ")

        else:#nếu nhập đủ 
            try:
                conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password, database=self.db.database, port=self.db.port)
                my_cursor = conn.cursor()#"ID Điểm Danh", "Ngày", "ID Học sinh"
                if(self.var_com_search.get()=="ID Điểm Danh"):#loại điểm danh là ID Điểm danh thì chuyển về IdAuttendance để truy vấn trong database
                    self.var_com_search.set("IdAuttendance")
                elif(self.var_com_search.get()=="Ngày"):
                    self.var_com_search.set("Date")
                else:
                    if(self.var_com_search.get()=="ID Học sinh"):
                        self.var_com_search.set("Student_id")
                    elif(self.var_com_search.get()=="ID Buổi học"):
                        self.var_com_search.set("Lesson_id")
                mydata.clear()#xóa dữ liệu trong mảng data
                my_cursor.execute("select * from attendance where "+str(self.var_com_search.get())+" Like '%"+str(self.var_search.get())+"%'")#câu lệnh tìm kiếm
                data=my_cursor.fetchall()#lấy tất cả dữ liệu vừa truy vấn vào biến data
                if(len(data)!=0):#nếu có data

                    self.AttendanceReportTable.delete(*self.AttendanceReportTable.get_children())
                    for i in data:
                        self.AttendanceReportTable.insert("",END,values=i)
                        mydata.append(i)
                    messagebox.showinfo("Thông báo","Có "+str(len(data))+" bản ghi thỏa mãn điều kiện",parent=self.root)
                    conn.commit()
                else:
                    self.AttendanceReportTable.delete(*self.AttendanceReportTable.get_children())
                    messagebox.showinfo("Thông báo", " Không có bản ghi nào thỏa mãn điều kiện",parent=self.root)
                conn.close()
            except Exception as es:
                messagebox.showerror("Lỗi", f"Due To:{str(es)}", parent=self.root)
    def today_data(self):#hàm lấy dữ liệu trong ngày
        try:
            conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password, database=self.db.database, port=self.db.port)
            my_cursor = conn.cursor()  # "ID Điểm Danh", "Ngày", "ID Học sinh"
            mydata.clear()#xóa dữ liệu trong mydata
            d1 = strftime("%d/%m/%Y")#ngày hôm nay
            my_cursor.execute("select * from attendance where Date Like '%" + str(
                d1) + "%'")#câu lệnh sql lấy tất cả thông tin trong bảng attendance khi có cọt Date là ngày hôm nay
            data = my_cursor.fetchall()
            if (len(data) != 0):#nếu có dữ liệu

                self.AttendanceReportTable.delete(*self.AttendanceReportTable.get_children())#xóa tất cả các dữ liệu cũ trong bảng
                for i in data:#với mỗi dòng trong dữ liệu
                    self.AttendanceReportTable.insert("", END, values=i)# thêm dữ liệu lên bảng
                    mydata.append(i)#truyền dữ liệu vào mảng mydata để xuất excel
                messagebox.showinfo("Thông báo", "Có " + str(len(data)) + " bản ghi hôm nay",parent=self.root)
                conn.commit()
            else:#nếu ko có dữ liệu
                self.AttendanceReportTable.delete(*self.AttendanceReportTable.get_children())#xóa tất cả dữ liệu trong bảng
                messagebox.showinfo("Thông báo", " Không có bản ghi nào trong hôm nay !",parent=self.root)#thông báo
            conn.close()
        except Exception as es:
            messagebox.showerror("Lỗi", f"Due To:{str(es)}", parent=self.root)

if __name__=="__main__":
    root=Tk() #khoi tao cua so va gan root vao
    obj=Attendance(root)#khởi tại object root
    root.mainloop()# cua so hien len