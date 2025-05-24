import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import pandas as pd
from modules import crud
from modules import visualize
from manage import manage_frame

# === Load dữ liệu gốc ===
train_df = pd.read_csv('dataset/titanic/train.csv')
test_df = pd.read_csv('dataset/titanic/test.csv')
gender_submission_df = pd.read_csv('dataset/titanic/gender_submission.csv')

# Nối theo PassengerId để thêm cột Survived
merged_df = test_df.merge(gender_submission_df, on="PassengerId", how="left")
merged_df.to_csv("dataset/titanic/test_with_survived.csv", index=False)

df = pd.concat([train_df, merged_df], ignore_index=True)

# === Giao diện chính ===
app = ttk.Window(themename="cosmo")
app.title("Quản lý dữ liệu Titanic")
app.geometry("1700x780")

# Khung sidebar bên trái
frame_sidebar = ttk.Frame(app, padding=10, width=220)
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
ttk.Button(chart_frame, text="Sống sót qua các đặc trưng (subplot)", command=lambda: show_chart(visualize.subplot_show_survival_chart(df))).pack(fill=X, pady=2)
ttk.Button(chart_frame, text="Tỉ lệ sống qua đặc trưng tuổi (hist)", command=lambda: show_chart(visualize.hist_show_age_chart(df))).pack(fill=X, pady=2)

# --- Các nút khác ---
ttk.Button(frame_sidebar, text="💾 Xuất CSV", bootstyle="success").pack(pady=5, fill=X)

# === Hiển thị giao diện ===
app.mainloop()
