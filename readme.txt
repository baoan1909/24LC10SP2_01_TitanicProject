# 🚢 TITANIC DATA MANAGEMENT PROJECT

## 📋 Thông tin đề tài
**STT:** [Điền số thứ tự]  
**Tên đề tài:** Quản lý và Phân tích Dữ liệu Titanic với Chức năng Clean  
**Lớp học phần:** 24LC10SP2_01  
**Năm học:** HK1/2024-2025  

## 👥 Thông tin nhóm
1. **Trưởng nhóm:** [Họ tên] ([MSSV]) – [SĐT] – [Email]
2. **Thành viên 2:** [Họ tên] ([MSSV])
3. **Thành viên 3:** [Họ tên] ([MSSV])
4. **Thành viên 4:** [Họ tên] ([MSSV])
5. **Thành viên 5:** [Họ tên] ([MSSV])

## 🎯 Mô tả dự án
Ứng dụng quản lý và phân tích dữ liệu hành khách tàu Titanic với giao diện đồ họa hiện đại, 
cung cấp các chức năng CRUD (Create, Read, Update, Delete), làm sạch dữ liệu, và trực quan hóa 
thông qua các biểu đồ phân tích.

## ✨ Tính năng chính

### 🔧 Quản lý dữ liệu
- **Xem danh sách hành khách**: Hiển thị bảng dữ liệu với phân trang
- **Thêm hành khách mới**: Form nhập liệu với validation
- **Sửa thông tin**: Chỉnh sửa dữ liệu hành khách hiện có
- **Xóa hành khách**: Xóa các bản ghi không cần thiết

### 🧹 Làm sạch dữ liệu
- **2 chế độ cleaning**:
  - **YES**: Làm sạch dữ liệu hiện tại (bao gồm các thay đổi)
  - **NO**: Làm sạch từ dữ liệu gốc (reset về ban đầu)
- **Xử lý missing values**: Tự động điền giá trị thiếu
- **Chuẩn hóa định dạng**: Đồng nhất kiểu dữ liệu

### 📊 Trực quan hóa dữ liệu
- **Pie Chart**: Tỷ lệ sống sót vs gặp nạn
- **Subplot**: Phân tích sống sót theo nhiều đặc trưng
- **Count Plot**: Sống sót theo kích thước gia đình
- **Histogram**: Phân bố độ tuổi và tỷ lệ sống sót
- **Box Plot**: Phân tích theo giới tính, độ tuổi, hạng vé

### 📤 Xuất dữ liệu
- **Export CSV**: Xuất dữ liệu hiện tại ra file CSV
- **Lưu tự động**: Tự động lưu dữ liệu sau khi cleaning

## 🛠️ Cài đặt và Chạy ứng dụng

### Yêu cầu hệ thống
- Python 3.8 trở lên
- Windows/macOS/Linux

### Bước 1: Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### Bước 2: Chạy ứng dụng
```bash
python source-code/main.py
```

## 📁 Cấu trúc thư mục
```
24LC10SP2_01_TitanicProject/
├── dataset/titanic/           # Dữ liệu Titanic
│   ├── train.csv             # Dữ liệu training
│   ├── test.csv              # Dữ liệu testing
│   ├── gender_submission.csv # Dự đoán giới tính
│   ├── cleaned.csv           # Dữ liệu đã làm sạch
│   └── exported_data.csv     # Dữ liệu xuất ra
├── source-code/              # Mã nguồn chính
│   ├── main.py              # File chính chạy ứng dụng
│   ├── cleaning.py          # Module làm sạch dữ liệu
│   ├── manage.py            # Module quản lý giao diện
│   └── modules/             # Các module con
│       ├── crud.py          # Chức năng CRUD
│       ├── clean.py         # Logic làm sạch dữ liệu
│       └── visualize.py     # Trực quan hóa dữ liệu
├── libs/                     # Thư viện bổ sung
├── refs/                     # Tài liệu tham khảo
├── reports/                  # Báo cáo dự án
├── requirements.txt          # Dependencies
└── readme.txt               # File hướng dẫn này
```

## 🔄 Quy trình làm việc

### Làm việc với dữ liệu mới
1. **Khởi động ứng dụng**: Chọn nguồn dữ liệu (cleaned.csv hoặc files gốc)
2. **Quản lý dữ liệu**: Thêm/sửa/xóa thông tin hành khách
3. **Lưu thay đổi**: Sử dụng chức năng "Clean với YES"
4. **Phân tích**: Xem các biểu đồ trực quan
5. **Xuất kết quả**: Export ra file CSV

### Reset về dữ liệu gốc
1. **Chọn "Clean dữ liệu"**
2. **Chọn "NO"**: Reset về 3 file gốc ban đầu
3. **Xác nhận**: Dữ liệu sẽ được làm sạch từ đầu

## ⚠️ Lưu ý quan trọng

### Về lưu trữ dữ liệu
- **Thay đổi trong giao diện chỉ lưu tạm trong memory**
- **Phải dùng "Clean với YES" để lưu vĩnh viễn vào cleaned.csv**
- **"Clean với NO" sẽ MẤT HẾT các thay đổi và reset về gốc**

### Về hiệu năng
- Ứng dụng tối ưu cho dataset có kích thước vừa phải (< 10MB)
- Các biểu đồ có thể mất vài giây để load với dữ liệu lớn

### Về tương thích
- Tested trên Python 3.8-3.11
- GUI hoạt động tốt trên màn hình ≥ 1366x768

## 🔧 Dependencies chính
- **pandas**: Xử lý và phân tích dữ liệu
- **numpy**: Tính toán số học
- **matplotlib**: Vẽ biểu đồ cơ bản
- **seaborn**: Biểu đồ thống kê nâng cao
- **ttkbootstrap**: Giao diện đồ họa hiện đại
- **missingno**: Phân tích missing values

## 🐛 Troubleshooting

### Lỗi không tìm thấy file
- Đảm bảo chạy từ thư mục gốc của project
- Kiểm tra đường dẫn tới files CSV trong dataset/titanic/

### Lỗi import module
- Chạy lại: `pip install -r requirements.txt`
- Kiểm tra version Python (≥ 3.8)

### Lỗi hiển thị biểu đồ
- Cài đặt thêm: `pip install tkinter` (nếu cần)
- Kiểm tra resolution màn hình
