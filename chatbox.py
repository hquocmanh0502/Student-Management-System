import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import customtkinter as ctk
import openai
import google.generativeai as genai

# Thay thế bằng khóa API của bạn
genai.configure(api_key = "AIzaSyBnwyOW6KfZlMPPQ-IQFbDSOiDTo4N82KI")
model = genai.GenerativeModel('gemini-1.5-flash-latest')


class ChatBoxWindow(ctk.CTk):
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.title("AI ChatBox")
        self.geometry("800x600")
        self.resizable(True, True)  # Đặt kích thước tuyệt đối cho cửa sổ
        # Set up the main frame
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(pady = 20, padx = 20, fill = "both", expand = True)

        # Text widget to display conversation
        self.text_area = ctk.CTkTextbox(self.frame, wrap = "word")
        self.text_area.pack(pady = 10, padx = 10, fill = "both", expand = True)
        self.text_area.configure(state = "disabled")

        # Frame to hold the user input and buttons
        self.input_frame = ctk.CTkFrame(self.frame)
        self.input_frame.pack(pady = 10, padx = 10, fill = "x")

        # Entry widget for user input
        self.user_input = ctk.CTkEntry(self.input_frame, placeholder_text = 'Nhập vào điều bạn cần hỏi')
        self.user_input.pack(side = "left", pady = 10, padx = (10, 5), fill = "x", expand = True)
        self.user_input.bind("<Return>", self.send_message)

        # Send button
        self.send_button = ctk.CTkButton(self.input_frame, text = "Send", command = self.send_message)
        self.send_button.pack(side = "left", pady = 10, padx = 5)

        # Add a button to open file chooser
        self.file_button = ctk.CTkButton(self.input_frame, text = "Chọn ảnh", command = self.choose_image,
                                         width = 100)
        self.file_button.pack(side = "left", pady = 10, padx = (5, 5))

        # Add a button to delete image
        self.delete_button = ctk.CTkButton(self.input_frame, text = "Xoá ảnh", command = self.delete_image,
                                           width = 100)
        self.delete_button.pack(side = "left", pady = 10, padx = (5, 10))

        # Frame to hold the image
        self.image_frame = tk.Frame(self.frame, width = 150, height = 150, bg = "gray")
        self.image_frame.pack(pady = 10)
        self.image_frame.pack_propagate(True)  # Prevent frame from resizing to fit the image

        # Label to display the selected image
        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack(expand = True)

        self.img = None

    def choose_image(self):
        file_path = filedialog.askopenfilename(filetypes = [("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")])
        if file_path:
            self.img = Image.open(file_path)
            self.display_image(self.img, file_path)

    def display_image(self, img, file_path):
        self.display_message("System", f"Image loaded: {file_path}")

        # Resize image to fit in label
        img.thumbnail((150, 150))
        img_tk = ImageTk.PhotoImage(img)

        self.image_label.configure(image = img_tk)
        self.image_label.image = img_tk  # Keep a reference to avoid garbage collection

    def delete_image(self):
        self.img = None
        self.image_label.configure(image = None)
        self.image_label.image = None
        self.display_message("System", "Image deleted")

    def send_message(self, event = None):
        user_message = self.user_input.get()
        if user_message.strip():
            self.display_message("User", user_message)
            self.user_input.delete(0, tk.END)
            response = self.get_gpt_response(user_message)
            self.display_message("AI", response)

    def display_message(self, sender, message):
        self.text_area.configure(state = "normal")
        self.text_area.insert(tk.END, f"{sender}: {message}\n")
        self.text_area.configure(state = "disabled")
        self.text_area.see(tk.END)

    def get_gpt_response(self, user_message):
        try:
            if self.img is None:
                reponse = model.generate_content(user_message)
                return reponse.text
            else:
                response = model.generate_content([user_message, self.img])
                self.img = None
                return response.text
        except Exception as e:
            return f"Error: {e}"


if __name__ == "__main__":
    app = ChatBoxWindow()
    app.mainloop()
