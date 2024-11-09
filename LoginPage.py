from tkinter import Checkbutton, messagebox, Toplevel

from customtkinter import *
from PIL import Image
import mysql.connector

from main_upd import new_print, Face_Recognition_System
from database_str import Database_str


class LoginPage(object):
    def __init__(self, window):

        # Màn hình
        self.window = window
        self.window.title("Login Page")
        self.window.config(bg = "white")
        self.window.resizable(False, False)
        bg_img = CTkImage(dark_image = Image.open("bg1.jpg"), size = (500, 500))
        bg_lab = CTkLabel(self.window, image = bg_img, text = "")
        bg_lab.grid(row = 0, column = 0)

        # =============biến kiểu string email,password============
        self.var_email = StringVar()
        self.var_password = StringVar()

        # Frame đăng nhập
        self.frame1 = CTkFrame(self.window, fg_color = "#D9D9D9", bg_color = "white", height = 350, width = 300,
                               corner_radius = 20) 
        self.frame1.grid(row = 0, column = 1, padx = 40)

        # Tiêu đề
        self.title = CTkLabel(self.frame1, text = "Ứng dụng quản lý học sinh", text_color = "white", font = ("", 30, "bold"),
                              fg_color = "#4158D0", corner_radius = 32, height = 50)
        self.title.grid(row = 0, column = 0, pady = 30, padx = 10)

        # Nhập tài khoản
        self.username_entry = CTkEntry(self.frame1, text_color = "white", placeholder_text = "Tài khoản",
                                       fg_color = "black", placeholder_text_color = "white",
                                       font = ("", 16, "bold"), width = 200, corner_radius = 15, height = 45,
                                       textvariable = self.var_email)
        self.username_entry.grid(row = 1, column = 0, sticky = "nwe", padx = 30)

        # Nhập mật khẩu
        self.password_entry = CTkEntry(self.frame1, text_color = "white", placeholder_text = "Mật khẩu",
                                       fg_color = "black", placeholder_text_color = "white",
                                       font = ("", 16, "bold"), width = 200, corner_radius = 15, height = 45,
                                       show = "*", textvariable = self.var_password)
        self.password_entry.grid(row = 2, column = 0, sticky = "nwe", padx = 30, pady = 20)

        # cr_acc = CTkLabel(frame1,text="Create Account!",text_color="black",cursor="hand2",font=("",15))
        # cr_acc.grid(row=3,column=0,sticky="w",pady=20,padx=40)

        # Button đăng nhập
        self.l_btn = CTkButton(self.frame1, text = "Đăng nhập", font = ("", 15, "bold"), height = 40, width = 60,
                               fg_color = "#0085FF", cursor = "hand2",
                               corner_radius = 15, command = self.login)  # Button này dùng method login
        self.l_btn.grid(row = 3, column = 0, pady = 20, padx = 35)

        self.varcheck = IntVar()
        self.checkbtn = CTkCheckBox(self.frame1, variable = self.varcheck, onvalue = 1, offvalue = 0,
                                    text = "Sử dụng tài khoản quản trị")
        self.checkbtn.grid(row = 4, column = 0, sticky = "w", pady = 10, padx = 35)
         # Nhãn thông tin nhóm
        self.group_info_label = CTkLabel(self.frame1, text="Nhóm 1\n  GVHD : Trịnh Văn Bình\n", 
                                   text_color="black", font=("Helvetica", 16, "bold"))
        self.group_info_label.grid(row=5, column=0, pady=10)


    def print_email(self):
        print(self.var_email.get())
        print(self.var_password.get())

    # hàm đăng nhập
    def login(self):
        db_info = Database_str()  # Tạo đối tượng Database_str để lấy thông tin kết nối

        if self.username_entry.get() == "" or self.password_entry.get() == "":
            messagebox.showerror("Lỗi !!", "Vui lòng nhập đầy đủ thông tin")
        elif (self.varcheck.get() == 1):
            try:
                conn = mysql.connector.connect(
                    host=db_info.host,
                    user=db_info.user,
                    password=db_info.password,
                    database=db_info.database,
                    port=db_info.port
                )
                my_cursor = conn.cursor()
                my_cursor.execute("select * from admin where Account=%s and Password=%s", (
                    self.var_email.get(),
                    self.var_password.get()
                ))
                row = my_cursor.fetchone()
                if row == None:
                    messagebox.showerror("Lỗi", "Sai tên đăng nhập, mật khẩu hoặc quyền đăng nhập")
                else:
                    new_print(str(0))
                    self.reset()
                    messagebox.showinfo("Thông báo", "Bạn đã đăng nhập thành công với quyền Admin")
                    self.window.withdraw()
                    self.app = Face_Recognition_System(self)
                conn.commit()
                conn.close()
            except Exception as es:
                messagebox.showerror("Lỗi", f"Due To:{str(es)}", parent=self)
        else:
            try:
                conn = mysql.connector.connect(
                    host=db_info.host,
                    user=db_info.user,
                    password=db_info.password,
                    database=db_info.database,
                    port=db_info.port
                )
                my_cursor = conn.cursor()
                my_cursor.execute("select Teacher_id from teacher where Email=%s and Password=%s", (
                    self.var_email.get(),
                    self.var_password.get()
                ))
                row = my_cursor.fetchone()

                if row == None:
                    messagebox.showerror("Lỗi", "Sai tên đăng nhập hoặc mật khẩu")
                else:
                    new_print(str(row[0]))
                    self.reset()
                    self.window.withdraw()
                    self.new_window = Toplevel(self.window)
                    self.app = Face_Recognition_System(self)
                conn.commit()
                conn.close()
            except Exception as es:
                messagebox.showerror("Lỗi", f"Due To:{str(es)}", parent=self)


    # reset thông tin password_tài khoản
    def reset(self):
        self.var_email.set("")
        self.var_password.set("")
        self.varcheck.set(0)

    def show(self):
        """"""
        self.window.update()
        self.window.deiconify()


if __name__ == '__main__':
    window = CTk()  # tạo giao diện tkinter Tk() và gán nó vào biến window
    obj = LoginPage(window)
    window.mainloop()  # hiển thị giao diện và bắt đầu nhận các sự kiện để xử lý.
