import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import pandas as pd
from modules import crud
from modules import visualize
from modules import clean
from manage import manage_frame
from tkinter import messagebox
import os

# === Giao diện chính ===
app = ttk.Window(themename="cosmo")
app.title("Quản lý dữ liệu Titanic")
app.geometry("1700x780")

# === Load dữ liệu ===
# Check if cleaned.csv exists and ask user preference
cleaned_file_exists = os.path.exists('dataset/titanic/cleaned.csv')

if cleaned_file_exists:
    # Ask user if they want to use cleaned data or original data
    use_cleaned = messagebox.askyesno(
        "Chọn dữ liệu", 
        "Phát hiện file cleaned.csv đã tồn tại.\n\nBạn có muốn sử dụng dữ liệu đã được clean không?\n\nChọn 'No' để load lại từ 3 file gốc."
    )
    
    if use_cleaned:
        df = clean.load_cleaned_data()
        print("Đã load dữ liệu từ cleaned.csv")
    else:
        print("Loading từ 3 file gốc...")
        train_df = pd.read_csv('dataset/titanic/train.csv')
        test_df = pd.read_csv('dataset/titanic/test.csv')
        gender_submission_df = pd.read_csv('dataset/titanic/gender_submission.csv')
        
        # Nối theo PassengerId để thêm cột Survived
        merged_df = test_df.merge(gender_submission_df, on="PassengerId", how="left")
        df = pd.concat([train_df, merged_df], ignore_index=True)
        print("Đã load và merge 3 file gốc")
else:
    # No cleaned file exists, load original files
    print("Không tìm thấy cleaned.csv. Loading từ 3 file gốc...")
    train_df = pd.read_csv('dataset/titanic/train.csv')
    test_df = pd.read_csv('dataset/titanic/test.csv')
    gender_submission_df = pd.read_csv('dataset/titanic/gender_submission.csv')
    
    # Nối theo PassengerId để thêm cột Survived
    merged_df = test_df.merge(gender_submission_df, on="PassengerId", how="left")
    df = pd.concat([train_df, merged_df], ignore_index=True)
    print("Đã load và merge 3 file gốc")

# Khung sidebar bên trái
frame_sidebar = ttk.Frame(app, padding=10, width=250)
frame_sidebar.pack(side=LEFT, fill=Y)
frame_sidebar.pack_propagate(False)

# Khung hiển thị nội dung chính
frame_main_content = ttk.Frame(app)
frame_main_content.pack(side=LEFT, fill=BOTH, expand=True)

# Label tiêu đề
ttk.Label(frame_sidebar, text="Chức năng", font=("Arial", 12, "bold")).pack(pady=10)

# === Tạo frame Quản lý hành khách ===
frame_manage_passenger, table, entry_vars = manage_frame(frame_main_content, df)
frame_manage_passenger.pack(fill=BOTH, expand=True)  # Hiển thị mặc định

# Hàm ẩn tất cả frame trong nội dung chính
def hide_all_frames():
    for child in frame_main_content.winfo_children():
        child.pack_forget()

# Hàm reload dữ liệu sau khi clean
def reload_data():
    global df, frame_manage_passenger, table, entry_vars
    new_df = clean.load_cleaned_data()
    if new_df is not None:
        df = new_df
        # Tạo lại frame quản lý với dữ liệu mới
        hide_all_frames()
        frame_manage_passenger, table, entry_vars = manage_frame(frame_main_content, df)
        frame_manage_passenger.pack(fill=BOTH, expand=True)
        crud.update_table(table, df)

# --- Nút Quản lý hành khách ---
def show_manage_passenger():
    hide_all_frames()
    frame_manage_passenger.pack(fill=BOTH, expand=True)
    crud.update_table(table, df)
    crud.clear_form(entry_vars)

ttk.Button(
    frame_sidebar,
    text="👤 Quản lý hành khách",
    command=show_manage_passenger,
    bootstyle="primary"
).pack(pady=5, fill=X)

# --- Nút Clean dữ liệu với tùy chọn ---
def clean_data_options():
    choice = messagebox.askyesnocancel(
        "Tùy chọn Clean", 
        "Chọn cách thức clean dữ liệu:\n\n" +
        "• YES: Clean dữ liệu hiện tại (bao gồm thay đổi của bạn)\n" +
        "• NO: Clean từ 3 file gốc (bỏ qua thay đổi)\n" +
        "• Cancel: Hủy bỏ"
    )
    
    if choice is None:  # Cancel
        return
    
    try:
        messagebox.showinfo("Đang xử lý", "Đang thực hiện cleaning dữ liệu...")
        
        if choice:  # YES - Clean current data
            clean.merge_and_clean_data(current_df=df)
            messagebox.showinfo("Thành công", 
                "Đã clean dữ liệu hiện tại (bao gồm thay đổi) và lưu vào cleaned.csv!\n" +
                "Dữ liệu đã được tự động reload.")
        else:  # NO - Clean from original files
            clean.merge_and_clean_data(current_df=None)
            messagebox.showinfo("Thành công", 
                "Đã clean từ 3 file gốc và lưu vào cleaned.csv!\n" +
                "Dữ liệu đã được tự động reload.")
        
        reload_data()
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể clean dữ liệu:\n{str(e)}")

ttk.Button(
    frame_sidebar,
    text="🧹 Clean dữ liệu",
    command=clean_data_options,
    bootstyle="warning"
).pack(pady=5, fill=X)

# --- Nút Biểu đồ ---
def toggle_chart_options():
    if chart_frame.winfo_ismapped():
        chart_frame.pack_forget()
    else:
        chart_frame.pack(after=btn_chart, pady=5, fill=X)

btn_chart = ttk.Button(frame_sidebar, text="📊 Biểu đồ ▼", command=toggle_chart_options, bootstyle="info")
btn_chart.pack(pady=5, fill=X)

# --- Khung các lựa chọn biểu đồ ---
chart_frame = ttk.Frame(frame_sidebar)

def show_chart():
    hide_all_frames()
    chart_frame_container = ttk.Frame(frame_main_content)
    chart_frame_container.place(relwidth=1, relheight=1)

ttk.Button(chart_frame, text="Phân bố tuổi với hạng vé (boxplot)", command=lambda: show_chart(visualize.boxplot_show_age_pclass_chart(df))).pack(fill=X, pady=2)
ttk.Button(chart_frame, text="Tỉ lệ sống - không sống (pie)", command=lambda: show_chart(visualize.pie_show_survived_rate_chart(df))).pack(fill=X, pady=2)
ttk.Button(chart_frame, text="Sống sót theo các đặc trưng (subplot)", command=lambda: show_chart(visualize.subplot_show_survival_chart(df))).pack(fill=X, pady=2)
ttk.Button(chart_frame, text="Tỉ lệ sống theo đặc trưng tuổi (hist)", command=lambda: show_chart(visualize.hist_show_age_chart(df))).pack(fill=X, pady=2)
ttk.Button(chart_frame, text="Tỉ lệ sống theo danh xưng (countplot)", command=lambda: show_chart(visualize.count_plot_show_title_chart(df))).pack(fill=X, pady=2)

# --- Nút Xuất CSV ---
def export_csv():
    try:
        df.to_csv('dataset/titanic/exported_data.csv', index=False)
        messagebox.showinfo("Thành công", "Đã xuất dữ liệu ra exported_data.csv!")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể xuất CSV:\n{str(e)}")

ttk.Button(frame_sidebar, text="📤 Xuất CSV", command=export_csv, bootstyle="success").pack(pady=5, fill=X)

# === Hiển thị giao diện ===
app.mainloop()
