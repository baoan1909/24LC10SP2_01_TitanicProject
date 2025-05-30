import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import pandas as pd
from modules import crud

def manage_frame(app, df):
    # Khai báo biến dùng chung
    filtered_df = df.copy()
    current_page_var = ttk.IntVar(value=0)
    page_info_var = ttk.StringVar(value="Trang 1 / ?")
    rows_per_page = 50

    frame = ttk.Frame(app)

    # ==== Filter ====
    frame_filter = ttk.Frame(frame, padding=10)
    frame_filter.pack(fill=X)

    sex_var = ttk.StringVar(value="Tất cả")
    pclass_var = ttk.StringVar(value="Tất cả")
    search_var = ttk.StringVar()
    

    def do_filter():
        nonlocal filtered_df
        filtered_df = crud.filter_data(df, sex_var.get(), pclass_var.get(), search_var.get().strip().lower())
        current_page_var.set(0)
        crud.update_table(table, filtered_df, 0, rows_per_page)
        crud.update_page_info(current_page_var, page_info_var, filtered_df, rows_per_page)

    
    ttk.Label(frame_filter, text="Giới tính:").pack(side=LEFT)
    ttk.Combobox(frame_filter, textvariable=sex_var, values=["Tất cả", "male", "female"], width=10).pack(side=LEFT, padx=5)
    ttk.Label(frame_filter, text="Hạng vé:").pack(side=LEFT)
    ttk.Combobox(frame_filter, textvariable=pclass_var, values=["Tất cả", "1", "2", "3"], width=10).pack(side=LEFT, padx=5)
    ttk.Label(frame_filter, text="Tìm kiếm tên hành khách:").pack(side=LEFT)
    ttk.Entry(frame_filter, textvariable=search_var).pack(side=LEFT, padx=5)
    ttk.Button(frame_filter, text="Lọc dữ liệu", command=do_filter, bootstyle="primary").pack(side=LEFT, padx=10)

    # ==== Table ====
    frame_table = ttk.Frame(frame)
    frame_table.pack(fill=BOTH, expand=True, padx=10, pady=10)

    cols = list(df.columns)
    table = ttk.Treeview(frame_table, columns=cols, show="headings", bootstyle="info", yscrollcommand=True)

    for col in cols:
        table.heading(col, text=col)
        table.column(col, width=120, anchor='center')

    scroll_y = ttk.Scrollbar(frame_table, orient='vertical', command=table.yview)
    table.configure(yscrollcommand=scroll_y.set)
    table.pack(side=LEFT, fill=BOTH, expand=True)
    scroll_y.pack(side=RIGHT, fill=Y)

    crud.update_table(table, df, current_page_var.get(), rows_per_page)

    # ==== Pagination ====
    frame_pagination = ttk.Frame(frame)
    frame_pagination.pack(fill=X, padx=10, pady=5)
    go_to_page = ttk.IntVar()

    ttk.Label(frame_pagination, text="Đến trang:").pack(side=LEFT)
    ttk.Entry(frame_pagination, textvariable=go_to_page, width=5).pack(side=LEFT, padx=5)
    ttk.Button(frame_pagination, text="Đi", command=lambda: crud.go_to_page(filtered_df, go_to_page, current_page_var, rows_per_page, table, page_info_var), bootstyle="primary").pack(side=LEFT, padx=5)

    ttk.Button(frame_pagination, text="Trang sau ▶️", command=lambda: crud.next_page(filtered_df, current_page_var, rows_per_page, table, page_info_var), bootstyle="primary").pack(side=RIGHT, padx=5)
    ttk.Button(frame_pagination, text="◀️ Trang trước", command=lambda: crud.previous_page(filtered_df, current_page_var, rows_per_page, table, page_info_var), bootstyle="primary").pack(side=RIGHT, padx=5)
    ttk.Label(frame_pagination, textvariable=page_info_var).pack(side=RIGHT, padx=5)

    crud.update_page_info(current_page_var, page_info_var, df, rows_per_page)

    # ==== Form nhập ====
    frame_form = ttk.Labelframe(frame, text="Thông tin hành khách", padding=10)
    frame_form.pack(fill=X, padx=10, pady=5)

    entry_vars = {}
    for i, col in enumerate(cols):
        ttk.Label(frame_form, text=col).grid(row=i//4, column=(i%4)*2, sticky=E, padx=5, pady=5)
        var = ttk.StringVar()

        if col == 'Sex':
            widget = ttk.Combobox(frame_form, textvariable=var, values=["male", "female"], width=15)
        elif col == 'Survived':
            widget = ttk.Combobox(frame_form, textvariable=var, values=["0", "1"], width=15)
        elif col == 'Pclass':
            widget = ttk.Combobox(frame_form, textvariable=var, values=["1", "2", "3"], width=15)
        elif col == 'Embarked':
            widget = ttk.Combobox(frame_form, textvariable=var, values=["C", "Q", "S"], width=15)
        else:
            widget = ttk.Entry(frame_form, textvariable=var, width=17)

        widget.grid(row=i//4, column=(i%4)*2 + 1, padx=5, pady=5)
        entry_vars[col] = var

        if col == 'PassengerId':
            widget.configure(state='readonly')

    def refresh_filtered():
        nonlocal filtered_df
        filtered_df = df.copy()
        current_page_var.set(0)
        crud.update_page_info(current_page_var, page_info_var, filtered_df, rows_per_page)

    # ==== Buttons ====
    frame_btn = ttk.Frame(frame)
    frame_btn.pack(pady=10)

    ttk.Button(frame_btn, text="➕ Thêm",
        command=lambda: [crud.add_row(df, cols, entry_vars, table),
                        refresh_filtered()],
        bootstyle="success").pack(side=LEFT, padx=10)

    ttk.Button(frame_btn, text="✏️ Cập nhật",
        command=lambda: [crud.edit_row(df, cols, entry_vars, table),
                        refresh_filtered()],
        bootstyle="warning").pack(side=LEFT, padx=10)

    ttk.Button(frame_btn, text="❌ Xoá",
        command=lambda: [crud.delete_row(df, table, entry_vars),
                        refresh_filtered()],
        bootstyle="danger").pack(side=LEFT, padx=10)

    ttk.Button(frame_btn, text="🧹 Xoá form", command=lambda: crud.clear_form(entry_vars), bootstyle="secondary").pack(side=LEFT, padx=10)

    table.bind('<<TreeviewSelect>>', lambda event: crud.on_row_select(event, table, cols, entry_vars))

    return frame, table, entry_vars

def update_dataframe_in_manage(frame_manage, table, new_df):
    """
    Update the dataframe in manage frame after cleaning
    """
    crud.update_table(table, new_df)
