# Student-Management-System
# Người tạo dự án
1. Hoàng Quốc Mạnh 
## Giới thiệu:
Student-Management-System là một hệ thống quản lý sinh viên hoàn chỉnh, cung cấp nhiều tính năng hiện đại giúp quản lý thông tin sinh viên, nhận diện khuôn mặt, chấm trắc nghiệm tự động và tích hợp AI để nâng cao trải nghiệm người dùng. Dự án này hỗ trợ nhiều tính năng như đăng nhập bảo mật, quản lý thông tin sinh viên, chấm điểm trắc nghiệm, và thay đổi mật khẩu.

## Tính năng chính

**1. Đăng nhập:**

- Người dùng (admin/giáo viên) có thể đăng nhập vào hệ thống thông qua tài khoản được cấp.
- Đảm bảo bảo mật qua mã hóa mật khẩu và giao thức bảo mật.
  
**2. Trang chủ:**

- Giao diện thân thiện, dễ sử dụng, hiển thị các thông tin cơ bản như tổng số sinh viên, lớp học, giáo viên, xuất file excel.
- Cung cấp các liên kết nhanh đến các chức năng như Quản lý Sinh viên, Chấm điểm, và Báo cáo.
  
**3. Quản lý Sinh viên:**

- Quản lý thông tin chi tiết về sinh viên như thông tin cá nhân, thông tin buổi học, điểm danh, thống kê.
- Chức năng thêm mới, chỉnh sửa và xóa thông tin sinh viên.
- Tìm kiếm và lọc danh sách sinh viên theo lớp, khóa học hoặc tên.

**4. Nhận diện khuôn mặt:**

- Tích hợp công nghệ nhận diện khuôn mặt để xác thực danh tính sinh viên.
- Sử dụng AI để đảm bảo độ chính xác và an toàn trong việc nhận diện sinh viên, đặc biệt trong các buổi điểm danh.
  
**5. Chấm điểm trắc nghiệm tự động:**

- Hệ thống hỗ trợ chấm điểm bài thi trắc nghiệm một cách tự động.
- Sinh viên có thể làm bài thi trực tuyến, và hệ thống sẽ chấm điểm ngay sau khi hoàn thành.
- Tích hợp AI để phân tích kết quả thi và đề xuất cải tiến học tập cho sinh viên.
    
**6. Tích hợp AI:**

- Hỗ trợ các chức năng thông minh như dự đoán kết quả học tập dựa trên dữ liệu quá khứ.
- Đưa ra các đề xuất cải thiện phương pháp học tập cho sinh viên dựa trên điểm số và tiến độ học tập.
  
**7. Đổi mật khẩu:**

- Người dùng có thể thay đổi mật khẩu thông qua giao diện đổi mật khẩu trong hệ thống.

## Hướng dẫn cài đặt
1. Clone repository: https://github.com/manhdzqatroioihi/Student-Management-System
2. Cài đặt các gói phụ thuộc: pip install pipreqs
                              pipreqs /path/to/your/project
3. Tạo cơ sở dữ liệu bằng cách chạy file face_recognizer (2).sql
4. Thay password SQL của bạn trong file database_str.py
```
class Database_str:
    def __init__(self):
        self.host='localhost'
        self.user='root'
        self.password='mat khau sql cua ban'
        self.database='manh'
        self.port='3306'
```
4. Chạy ứng dụng bằng cách chạy file LoginPage.py
# Công nghệ sử dụng
 - Thư viện giao diện người dùng (GUI)
    + tkinter: Thư viện này là bộ công cụ tiêu chuẩn của Python để tạo giao diện người dùng đồ họa. Nó cung cấp các widget như nút bấm, trường nhập liệu, bảng điều khiển, v.v.
    + ttk: Là phần mở rộng của tkinter, cung cấp các widget được làm đẹp hơn và giao diện hiện đại hơn so với các widget mặc định.
    + ImageTk: Đây là phần mở rộng của Pillow để tích hợp hình ảnh vào tkinter.
 - Python Built-in Libraries
   + os: Thư viện này cung cấp nhiều chức năng liên quan đến hệ điều hành như quản lý tập tin, thư mục, và môi trường hệ thống.
   + pickle: Thư viện này dùng để tuần tự hóa và giải tuần tự hóa các đối tượng Python. Nó rất hữu ích để lưu trữ và tải các đối tượng trong file.
   + datetime và time: Các thư viện này cung cấp các công cụ để làm việc với ngày và giờ, bao gồm cả việc định dạng ngày giờ và tính toán thời gian.
   + random: Thư viện này được sử dụng để tạo ra các số ngẫu nhiên, hoặc lựa chọn ngẫu nhiên từ một dãy dữ liệu.
 - Database: MySQL
 - Thư viện ngoài :
   + numpy: Thư viện mạnh mẽ dùng cho các tính toán khoa học và mảng đa chiều. Trong trường hợp này, có thể nó được sử dụng cho các phép tính liên quan đến dữ liệu hình ảnh hoặc dữ liệu số khác.
   + PIL (Python Imaging Library) và Pillow: PIL và Pillow là các thư viện dùng để xử lý hình ảnh, từ việc mở, thao tác, chỉnh sửa cho đến lưu trữ hình ảnh.
   + mysql.connector: Thư viện này cung cấp kết nối giữa Python và hệ quản trị cơ sở dữ liệu MySQL. Nó được dùng để tương tác với cơ sở dữ liệu như truy vấn, chèn dữ liệu, và quản lý bảng.
   + cv2 (OpenCV): Thư viện này dùng để xử lý hình ảnh và video. Nó rất phổ biến trong các ứng dụng thị giác máy tính và nhận diện khuôn mặt.
## Yêu cầu
 - Đã cài đặt Python
 - Đã cài đặt và chạy MySQL
 - Đã cài đặt Git
Copyrighted © hquocmanh0502 2024
