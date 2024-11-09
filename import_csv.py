from PIL import Image, ImageTk,ImageDraw
from tkinter import *
from tkinter import ttk
import PIL.Image ,PIL.ImageDraw
import csv
from tkinter import filedialog
import os
import mysql.connector
from tkinter import messagebox
import pandas as pd
from database_str import Database_str
mydata=[]
class InsertData:
    def __init__(self,root):
        self.root=root
        self.root.title("Quản lý thông tin")#tiêu đề
        self.root.geometry("900x550+0+0")
        self.root.config(bg="#021e2f")
        left_lbl = Label(self.root, bg="#08A3D2", bd=0)
        left_lbl.place(x=0, y=0, relheight=1, width=400)
        self.root.iconbitmap('ImageFaceDetect\\gaming.ico')  # icon của giao diện
        right_lbl = Label(self.root, bg="white", bd=2)
        right_lbl.place(x=200, y=0, relheight=1, relwidth=1)

        # ===========Frame===========
        # thông tin kết nối database
        self.db = Database_str()

        img_btn1 = PIL.Image.open(r"ImageFaceDetect\btnRed1.png")
        img_btn1 = img_btn1.resize((120, 30), PIL.Image.LANCZOS)
        self.photobtn1 = ImageTk.PhotoImage(img_btn1)


        title = Label(right_lbl, text="Thêm danh sách học sinh: ", font=("times new roman", 12, "bold"), bg="white",
                      fg="black").place(x=50, y=40)

        #chọn file danh sách hoc sinh
        btn_choose = Button(right_lbl, text="Choose File...", command=self.insert_stu, font=("times new roman", 11, "normal"),
                           bd=0,image=self.photobtn1,fg="white", compound="center",
                            cursor="hand2").place(x=280, y=40, width=120, height=30)

        title1 = Label(right_lbl, text="Thêm danh sách buổi học: ", font=("times new roman", 12, "bold"), bg="white",
                      fg="black").place(x=50, y=100)

        #chọn file danh sách buổi học
        btn_choose2  = Button(right_lbl, text="Choose File...", command=self.insert_less,
                           font=("times new roman", 11, "normal"),
                            bd=0,image=self.photobtn1,fg="white", compound="center",
                           bg="#DCDCDC", cursor="hand2").place(x=280, y=100, width=120, height=30)



        #Xóa tất cả học sinh
        btn_choose4  = Button(right_lbl, text="Xoá", command=self.delete_student,
                           font=("times new roman", 11, "normal"),
                           bd=0,image=self.photobtn1,fg="white", compound="center",
                           bg="#DCDCDC", cursor="hand2").place(x=430, y=40, width=120, height=30)

        #xóa tất cả buổi học
        btn_choose5  = Button(right_lbl, text="Xoá", command=self.delete_lesson,
                           font=("times new roman", 11, "normal"),
                            bd=0,image=self.photobtn1,fg="white", compound="center",
                           bg="#DCDCDC", cursor="hand2").place(x=430, y=100, width=120, height=30)






    #thêm danh sách học sinh từ file csv
    def insert_stu(self):
        try:
            global mydata
            mydata.clear()
            fln = filedialog.askopenfilename(initialdir=os.getcwd() + "/ListCSV", title="Open CSV",
                                             filetypes=(("Excel File", ".xlsx"), ("ALL File", "*.*")), parent=self.root)
            print(fln)

            df = pd.read_excel(fln)#đọc file excel đã chọn

            for index, row in df.iterrows():#truyền dữ liệu trong file excel ra biến mydata
                mydata.append((row[0], row[1], row[2],row[3], row[4], row[5],row[6], row[7].replace("'",""), row[8],row[9], row[10],row[11]))

            conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password, database=self.db.database, port=self.db.port)
            my_cursor = conn.cursor()

            #câu lệnh thêm danh sách sinh viên
            sql_insert_query = "insert into student values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            my_cursor.executemany(sql_insert_query, mydata)
            conn.commit()
            messagebox.showinfo("Thông báo", "Thêm danh sách sinh viên!!!")
            conn.close()
        except Exception as es:
            messagebox.showerror("Error", f"Due To:{str(es)}", parent=self.root)

    def insert_less(self):
        try:
            global mydata
            mydata.clear()
            fln = filedialog.askopenfilename(initialdir=os.getcwd() + "/ListCSV", title="Open CSV",
                                             filetypes=(("Excel File", ".xlsx"), ("ALL File", "*.*")), parent=self.root)


            df = pd.read_excel(fln)

            for index, row in df.iterrows():
                mydata.append((row[0], row[1], row[2], str(row[3]).replace("'",""), row[4]))
            # print(mydata[1])
            print(mydata)
            conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password,
                                           database=self.db.database, port=self.db.port)
            my_cursor = conn.cursor()
            sql_insert_query = "insert into lesson values(%s,%s,%s,%s,%s)"#câu lệnh thêm  danh sách buổi học
            my_cursor.executemany(sql_insert_query, mydata)
            conn.commit()
            messagebox.showinfo("Thông báo", "Thêm danh sách buổi học thành công!!!")
            conn.close()
        except Exception as es:
            messagebox.showerror("Error", f"Due To:{str(es)}", parent=self.root)



    def delete_student(self):#hàm xóa học sinh
            try:
                delete=messagebox.askyesno("Xoá học sinh","Bạn có muốn xóa tất cả học sinh?",parent=self.root)
                if delete>0:
                        conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password, database=self.db.database, port=self.db.port)
                        my_cursor = conn.cursor()
                        sql="delete from student"
                        my_cursor.execute(sql)
                else:
                    if not delete:
                        return
                conn.commit()

                conn.close()
                messagebox.showinfo("Xóa","Xóa sinh viên thành công",parent=self.root)
            except Exception as es:
                messagebox.showerror("Lỗi",f"Due To:{str(es)}",parent=self.root)

    def delete_lesson(self):#hàm xóa tất cả buổi học
            try:
                delete=messagebox.askyesno("Xoá buổi học","Bạn có muốn xóa danh sách buổi học này?",parent=self.root)
                if delete>0:
                        conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password, database=self.db.database, port=self.db.port)
                        my_cursor = conn.cursor()
                        sql="delete from lesson"

                        my_cursor.execute(sql)
                else:
                    if not delete:
                        return
                conn.commit()

                conn.close()
                messagebox.showinfo("Xóa","Xóa danh sách buổi học thành công",parent=self.root)
            except Exception as es:
                messagebox.showerror("Lỗi",f"Due To:{str(es)}",parent=self.root)



if __name__ == "__main__":
    root = Tk()  # khoi tao cua so va gan root vao
    obj = InsertData(root)
    root.mainloop()  # cua so hien len