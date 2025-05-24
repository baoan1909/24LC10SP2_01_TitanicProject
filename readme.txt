----- Thông tin đề tài --------------------- 
STT:  
Tên đề tài: Quản lý dữ liệu Titanic với chức năng Clean
Lớp học phần: 24LC10SP2_01
Năm học: HKx/2024-20xx 

----- Thông tin nhóm ----------------------- 
1. Họ tên sinh viên trưởng nhóm (mã số sinh viên trưởng nhóm) – SĐT – Email cá nhân 
2. Họ tên sinh viên 2 (mã số sinh viên 2) 
3. Họ tên sinh viên 3 (mã số sinh viên 3) 
4. Họ tên sinh viên 4 (mã số sinh viên 4) 
5. Họ tên sinh viên 5 (mã số sinh viên 5) 

----- Hướng dẫn sử dụng ứng dụng -----------

1. Cài đặt thư viện:
   pip install -r requirements.txt

2. Chạy ứng dụng:
   python source-code/main.py

3. Các chức năng chính:
   - Quản lý hành khách: Xem, thêm, sửa, xóa thông tin hành khách
   - Clean dữ liệu: Hợp nhất và làm sạch dữ liệu từ train.csv, test.csv, gender_submission.csv
   - Biểu đồ: Hiển thị các biểu đồ phân tích dữ liệu
   - Xuất CSV: Xuất dữ liệu hiện tại ra file CSV

4. Cấu trúc dữ liệu:
   - cleaned.csv: File dữ liệu đã được làm sạch
   - Nếu chưa có cleaned.csv, ứng dụng sẽ tự động load từ 3 file gốc

5. Chức năng Clean dữ liệu:
   - Hợp nhất train.csv, test.csv và gender_submission.csv
   - Xử lý missing values cho Age, Fare, Cabin, Embarked
   - Loại bỏ duplicate records
   - Xuất kết quả ra cleaned.csv và tự động reload trong ứng dụng