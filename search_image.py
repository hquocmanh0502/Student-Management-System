import os
import tkinter as tk
from tkinter import *
from tkinter import messagebox

import PIL
import mysql.connector
from PIL import ImageTk, Image
from database_str import Database_str
value_from_student=None

def student_id(value):
    global value_from_student
    value_from_student = value
    print(value_from_student)



class StdImage:
    def __init__(self,root):
        self.root = root
        self.root.geometry("800x600+300+50")
        self.root.title("Quản lý ảnh học sinh")
        self.root.iconbitmap('ImageFaceDetect\\gaming.ico')  # icon của giao diện

        # thông tin kết nối database
        self.db = Database_str()

        Left_frame = Frame(root, bd=2, bg="white")
        Left_frame.place(x=20, y=10, width=200, height=550)

        self.lst = tk.Listbox(Left_frame, width=20)
        self.lst.pack(side="left", fill=tk.BOTH, expand=0)
        self.lst.place(x=20,y=20,width=150,height=500)
        self.lst.bind("<<ListboxSelect>>", self.showimg)

        sbr=tk.Scrollbar(Left_frame)
        sbr.pack(side=RIGHT,fill="y")
        sbr.config(command=self.lst.yview)

        self.lst.config(yscrollcommand=sbr.set)

        right_fr = LabelFrame(root, bd=2, bg="white", relief=RIDGE, text="Thông tin học sinh",
                                          font=("times new roman", 12, "bold"))
        right_fr.place(x=230, y=10, width=560, height=550)



        #student info
        self.Student_id_label = Label(right_fr, text="ID học sinh:",
                                     font=("times new roman", 12, "bold"), bg="white")
        self.Student_id_label.grid(row=0, column=0, padx=10, pady=5, sticky=W)

        self.Student_id_atten_label = Label(right_fr, text="", font=("times new roman", 12, "bold"),
                                           bg="white", fg="red2")
        self.Student_id_atten_label.grid(row=0, column=1, padx=10, pady=5, sticky=W)

        # name
        self.stdName_label = Label(right_fr, text="Tên học sinh:",
                                          font=("times new roman", 12, "bold"),
                                          bg="white")
        self.stdName_label.grid(row=1, column=0, padx=10, pady=5, sticky=W)

        self.stdName_atten_label = Label(right_fr, text="", font=("times new roman", 12, "bold"),
                                                bg="white", fg="red2")
        self.stdName_atten_label.grid(row=1, column=1, padx=10, pady=5, sticky=W)

        # class
        self.class_label = Label(right_fr, text="Lớp biên chế:",
                                     font=("times new roman", 12, "bold"),
                                     bg="white")
        self.class_label.grid(row=2, column=0, padx=10, pady=5, sticky=W)

        self.class_atten_label = Label(right_fr, text="",
                                           font=("times new roman", 12, "bold"),
                                           bg="white", fg="red2")
        self.class_atten_label.grid(row=2, column=1, padx=10, pady=5, sticky=W)

        # getStudentInfo
        conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password, database=self.db.database, port=self.db.port)
        my_cursor = conn.cursor()
        my_cursor.execute(
            "select Student_id,Name,Class from student where Student_id=%s ",
            (value_from_student,))
        getInfo = my_cursor.fetchone()

        self.Student_id_atten_label['text']=getInfo[0]
        self.stdName_atten_label['text']=getInfo[1]
        self.class_atten_label['text']=getInfo[2]

        #image_frame
        img_fr = LabelFrame(right_fr, bd=2, bg="white", relief=RIDGE)
        img_fr.place(x=170, y=120, width=235, height=235)

        #image
        self.insertfiles()
        self.canvas = tk.Canvas(img_fr)
        self.canvas.place(x=5,y=5)

        save_btn=Button(right_fr,text="Xóa ảnh",command=self.delete,font=("times new roman",13,"bold"),bg="#000000", fg="white",width=17)
        save_btn.place(x=200,y=450)


    #================Functions=====================
    def insertfiles(self):
        user = str(value_from_student)
        directory = r"./faces"
        file_names = os.listdir(directory)
        name_path = "user." + user + "."
        print(name_path)
        num = 0
        for file_name in file_names:
            if file_name[:7] == str(name_path):
                full_path = os.path.join(directory, file_name)
                # print(full_path)
                num += 1
                self.lst.insert(tk.END, full_path)

        print("số ảnh đã chụp :" + str(num))

    def showimg(self, event):
        n = self.lst.curselection()
        filename = self.lst.get(n)

        self.img_right = PIL.Image.open(filename)
        self.img_right = self.img_right.resize((220, 220), PIL.Image.ANTIALIAS)

        img = ImageTk.PhotoImage(self.img_right)
        # img = ImageTk.PhotoImage(file=filename)

        w, h = img.width(), img.height()
        print(filename)
        self.canvas.image = img
        self.canvas.config(width=w, height=h)
        self.canvas.create_image(0, 0, image=img, anchor=tk.NW)

    def delete(self):

        Exit = messagebox.askyesno("Xóa ảnh", "Bạn có chắc chắn muốn xóa ảnh này?", parent=root)
        if (Exit > 0):
            n = self.lst.curselection()
            filename = self.lst.get(n)
            os.remove(filename)

            self.lst.delete(n)  # clear listbox

            print("số ảnh đã chụp :" + str(self.lst.size()))
            print("Bạn vừa xóa ảnh" + filename)

        else:
            if not Exit:
                return


if __name__=="__main__":
    root=Tk() #khoi tao cua so va gan root vao
    obj=StdImage(root)
    root.mainloop()# cua so hien len
