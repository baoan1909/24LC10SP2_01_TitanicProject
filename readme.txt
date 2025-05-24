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
   - Clean dữ liệu: 2 tùy chọn cleaning với dialog lựa chọn
   - Biểu đồ: Hiển thị các biểu đồ phân tích dữ liệu
   - Xuất CSV: Xuất dữ liệu hiện tại ra file CSV

4. Cấu trúc dữ liệu:
   - cleaned.csv: File dữ liệu đã được làm sạch
   - Nếu chưa có cleaned.csv, ứng dụng sẽ tự động load từ 3 file gốc

5. Chức năng Clean dữ liệu (có 2 tùy chọn):
   - **Tùy chọn YES**: Clean dữ liệu hiện tại (bao gồm thay đổi của bạn)
     → Các dòng thêm/sửa/xóa sẽ được giữ lại trong cleaned.csv
   - **Tùy chọn NO**: Clean từ 3 file gốc (bỏ qua thay đổi)
     → Reset về dữ liệu gốc và thực hiện cleaning

6. Luồng làm việc:
   a) Thêm/sửa/xóa dữ liệu trong giao diện
   b) Nhấn "🧹 Clean dữ liệu" → chọn "YES" để giữ thay đổi
   c) Hoặc chọn "NO" nếu muốn reset về dữ liệu gốc

7. Lưu ý quan trọng:
   - Thay đổi trong giao diện chỉ lưu trong memory
   - Phải nhấn "Clean với YES" để lưu thay đổi vào cleaned.csv
   - "Clean với NO" sẽ MẤT HẾT thay đổi và reset về gốc