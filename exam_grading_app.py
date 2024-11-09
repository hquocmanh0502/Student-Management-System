import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import imutils
import cv2

class ExamGradingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chấm điểm bài thi")
        self.root.geometry("1350x700")
        self.root.config(bg="#f4f4f4")  # Màu nền cửa sổ

        # Tạo nhãn nền (background)
        self.background_image = Image.open(r"./ImageFaceDetect/bg1.png")  # Đường dẫn tới hình nền của bạn
        self.background_image = self.background_image.resize((1350, 700), Image.Resampling.LANCZOS)  # Thay đổi kích thước ảnh nền
        self.background_tk = ImageTk.PhotoImage(self.background_image)

        # Đặt nhãn để chứa hình nền
        background_label = tk.Label(self.root, image=self.background_tk)
        background_label.place(relwidth=1, relheight=1)  # Đặt nhãn nền để chiếm toàn bộ cửa sổ

        # Thêm tiêu đề
        title_label = tk.Label(self.root, text="Chấm điểm tự động", font=("Arial", 24), bg="white")  # Thay đổi màu nền nếu cần
        title_label.pack(pady=20)

        # Frame chính để chia thành 2 phần
        main_frame = tk.Frame(self.root, bg="#f4f4f4")
        main_frame.pack(pady=40, padx=40, expand=True, fill="both")

        # Frame bên trái để nhập đáp án
        left_frame = tk.Frame(main_frame, bg="#f4f4f4")
        left_frame.grid(row=0, column=0, padx=20, pady=10, sticky="n")

        # Nhãn nhập đáp án
        answer_label = tk.Label(left_frame, text="Xin mời nhập đáp án :", font=("Arial", 16), bg="#f4f4f4")
        answer_label.pack(pady=10)

        self.answer_entries = []
        self.num_questions = 5  # Số câu hỏi

        # Tạo nhãn và ô nhập cho mỗi câu hỏi
        for i in range(self.num_questions):
            question_label = tk.Label(left_frame, text=f"Câu {i + 1}:", font=("Arial", 12), bg="#f4f4f4")
            question_label.pack(anchor="w", padx=10)

            entry = tk.Entry(left_frame, width=10)
            entry.pack(pady=5)
            self.answer_entries.append(entry)

        # Nút chọn ảnh
        self.browse_image_button_image = Image.open(r"./ImageFaceDetect/bntChonAnh.png")
        self.browse_image_button_image = self.browse_image_button_image.resize((100, 37), Image.Resampling.LANCZOS)
        self.browse_image_button_tk = ImageTk.PhotoImage(self.browse_image_button_image)

        browse_button = tk.Button(left_frame, image=self.browse_image_button_tk, command=self.browse_image, borderwidth=0, cursor="hand2")
        browse_button.pack(pady=20)

        # Nút reset
        # Tải ảnh cho nút reset
        self.reset_button_image = Image.open(r"./ImageFaceDetect/register.png")  # Đường dẫn đến ảnh nút Reset
        self.reset_button_image = self.reset_button_image.resize((140, 50), Image.Resampling.LANCZOS)  # Thay đổi kích thước ảnh
        self.reset_button_tk = ImageTk.PhotoImage(self.reset_button_image)

        # Nút reset
        reset_button = tk.Button(left_frame, image=self.reset_button_tk, command=self.reset_entries, borderwidth=0, cursor="hand2")
        reset_button.pack(pady=5)


        # Frame bên phải để hiển thị kết quả
        right_frame = tk.Frame(main_frame, bg="#f4f4f4")
        right_frame.grid(row=0, column=1, padx=20, pady=10, sticky="n")

        result_label = tk.Label(right_frame, text="Kết quả :", font=("Arial", 16), bg="#f4f4f4")
        result_label.pack(pady=10,padx=500)

        self.result_label = tk.Label(right_frame, text="", font=("Arial", 14), bg="#f4f4f4", fg="red")
        self.result_label.pack(pady=10)

        # Nhãn để hiển thị hình ảnh kết quả
        self.result_image_label = tk.Label(right_frame)
        self.result_image_label.pack(pady=10,padx=500)

        # Thêm biến để lưu trữ nhãn điểm số và ảnh kết quả
        self.score_label = None
        self.img_label = None

    # Hàm chuyển đổi đáp án từ ký tự sang chỉ số
    def answer_to_index(self, answer):
        answer = answer.upper()  # Chuyển đáp án thành chữ hoa
        if answer == 'A':
            return 0
        elif answer == 'B':
            return 1
        elif answer == 'C':
            return 2
        elif answer == 'D':
            return 3
        elif answer == 'E':
            return 4
        return None  # Trả về None nếu đáp án không hợp lệ

    # Hàm chấm điểm bài thi và trả về ảnh kết quả
    def grade_exam(self, image_path, answer_key):
        # Tải ảnh, chuyển đổi sang ảnh xám, làm mờ và tìm các cạnh
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(blurred, 75, 200)

        # Tìm các đường viền trong bản đồ cạnh
        cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        docCnt = None

        # Đảm bảo rằng ít nhất một đường viền được tìm thấy
        if len(cnts) > 0:
            # Sắp xếp các đường viền theo kích thước
            cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

            # Lặp qua các đường viền đã sắp xếp
            for c in cnts:
                # Xấp xỉ đường viền
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.02 * peri, True)

                # Nếu đường viền có bốn điểm, có thể là tờ giấy
                if len(approx) == 4:
                    docCnt = approx
                    break

        # Áp dụng biến đổi phối cảnh cho ảnh và ảnh xám
        paper = four_point_transform(image, docCnt.reshape(4, 2))
        warped = four_point_transform(gray, docCnt.reshape(4, 2))

        # Nhị phân hóa ảnh bằng phương pháp Otsu
        thresh = cv2.threshold(warped, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

        # Tìm các đường viền trong ảnh đã ngưỡng
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        questionCnts = []

        # Lặp qua các đường viền
        for c in cnts:
            (x, y, w, h) = cv2.boundingRect(c)
            ar = w / float(h)

            # Gán nhãn cho đường viền là một câu hỏi nếu tỷ lệ phù hợp
            if w >= 20 and h >= 20 and ar >= 0.9 and ar <= 1.1:
                questionCnts.append(c)

        # Sắp xếp các đường viền câu hỏi từ trên xuống dưới
        questionCnts = contours.sort_contours(questionCnts, method="top-to-bottom")[0]
        correct = 0

        # Lặp qua các câu hỏi
        for (q, i) in enumerate(np.arange(0, len(questionCnts), 5)):
            cnts = contours.sort_contours(questionCnts[i:i + 5])[0]
            bubbled = None

            # Tìm đáp án được tô
            for (j, c) in enumerate(cnts):
                mask = np.zeros(thresh.shape, dtype="uint8")
                cv2.drawContours(mask, [c], -1, 255, -1)
                mask = cv2.bitwise_and(thresh, thresh, mask=mask)
                total = cv2.countNonZero(mask)

                if bubbled is None or total > bubbled[0]:
                    bubbled = (total, j)

            # Màu đường viền và đáp án đúng
            color = (0, 0, 255)
            k = answer_key[q]

            if k == bubbled[1]:
                color = (0, 255, 0)
                correct += 1

            cv2.drawContours(paper, [cnts[k]], -1, color, 3)

        score = (correct / len(answer_key)) * 100

        cv2.putText(paper, "{:.2f}%".format(score), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

        paper_rgb = cv2.cvtColor(paper, cv2.COLOR_BGR2RGB)
        result_img_pil = Image.fromarray(paper_rgb)

        return score, result_img_pil

    # Hàm để duyệt và chọn ảnh
    def browse_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            answer_key = {}
            for i in range(len(self.answer_entries)):
                answer = self.answer_entries[i].get()
                index = self.answer_to_index(answer)
                if index is None:
                    messagebox.showerror("Error", f"Đáp án cho câu {i + 1} không hợp lệ! Vui lòng nhập A, B, C, D hoặc E.")
                    return
                answer_key[i] = index

            score, result_image = self.grade_exam(file_path, answer_key)
            self.display_result(result_image, score)

    # Hàm để hiển thị kết quả
    def display_result(self, result_image_pil, score):
        self.result_label.config(text=f"Điểm: {score:.2f}%")

    # Define maximum width and height
        max_width = 500
        max_height = 700

    # Get original dimensions
        orig_width, orig_height = result_image_pil.size

    # Calculate the scaling factor
        scaling_factor = min(max_width / orig_width, max_height / orig_height, 1)

    # Calculate new dimensions
        new_width = int(orig_width * scaling_factor)
        new_height = int(orig_height * scaling_factor)

    # Resize the image to fit the designated area
        img_resized = result_image_pil.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Convert PIL image to ImageTk
        self.img_tk = ImageTk.PhotoImage(img_resized)

    # Display the resized image
        self.result_image_label.config(image=self.img_tk)
        self.result_image_label.image = self.img_tk  # Keep a reference to avoid garbage collection


    # Hàm reset các ô nhập
    def reset_entries(self):
        for entry in self.answer_entries:
            entry.delete(0, tk.END)  # Xóa nội dung các ô nhập
        self.result_label.config(text="")  # Xóa điểm
        self.result_image_label.config(image=None)  # Xóa hình ảnh kết quả
        self.img_tk = None  # Xóa tham chiếu hình ảnh để đảm bảo nó không hiển thị nữa

if __name__ == "__main__":
    root = tk.Tk()
    app = ExamGradingApp(root)
    root.mainloop()
