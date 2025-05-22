from tkinter import messagebox

def clear_form(entry_vars):
    for var in entry_vars.values():
        var.set("")

def update_table(tree, df, page=0, rows_per_page=50):
    """Hiển thị dữ liệu theo trang."""
    tree.delete(*tree.get_children())
    start = page * rows_per_page
    end = start + rows_per_page
    page_data = df.iloc[start:end]
    for _, row in page_data.iterrows():
        tree.insert('', 'end', values=list(row))

def update_page_info(current_page_var, page_info_var, df, rows_per_page):
    """Cập nhật chuỗi Trang x / y"""
    total_pages = (len(df) - 1) // rows_per_page + 1
    current = current_page_var.get() + 1
    page_info_var.set(f"Trang {current} / {total_pages}")

def previous_page(df, current_page_var, rows_per_page, table, page_info_var):
    if current_page_var.get() > 0:
        current_page_var.set(current_page_var.get() - 1)
        update_table(table, df, current_page_var.get(), rows_per_page)
        update_page_info(current_page_var, page_info_var, df, rows_per_page)

def next_page(df, current_page_var, rows_per_page, table, page_info_var):
    total_pages = (len(df) - 1) // rows_per_page
    if current_page_var.get() < total_pages:
        current_page_var.set(current_page_var.get() + 1)
        update_table(table, df, current_page_var.get(), rows_per_page)
        update_page_info(current_page_var, page_info_var, df, rows_per_page)

def filter_data(df, sex_value, pclass_value):
    """Trả về DataFrame đã lọc"""
    filtered = df.copy()
    if sex_value != "Tất cả":
        filtered = filtered[filtered['Sex'] == sex_value]
    if pclass_value != "Tất cả":
        filtered = filtered[filtered['Pclass'] == int(pclass_value)]
    return filtered

def add_row(df, cols, entry_vars, tree):
    try:
        # Lấy dữ liệu từ form, bỏ qua PassengerId
        new_data = {col: entry_vars[col].get() for col in cols if col != 'PassengerId'}

        # Tự động sinh PassengerId mới
        new_id = int(df['PassengerId'].max()) + 1 if not df.empty else 1
        new_data['PassengerId'] = new_id

        # Chuyển kiểu dữ liệu phù hợp
        new_data['Survived'] = int(new_data['Survived'])
        new_data['Pclass'] = int(new_data['Pclass'])
        new_data['Age'] = float(new_data['Age'])
        new_data['SibSp'] = int(new_data['SibSp'])
        new_data['Parch'] = int(new_data['Parch'])
        new_data['Fare'] = float(new_data['Fare'])

        df.loc[len(df)] = new_data
        update_table(tree, df)
        clear_form(entry_vars)

        messagebox.showinfo("Thành công", "Thêm hành khách thành công!")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Dữ liệu không hợp lệ:\n{str(e)}")

def edit_row(df, cols, entry_vars, tree):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chưa chọn dòng", "Vui lòng chọn dòng cần sửa.")
        return
    try:
        idx = tree.index(selected[0])
        for col in cols:
            val = entry_vars[col].get()
            if col in ['PassengerId', 'Pclass', 'SibSp', 'Parch', 'Survived']:
                df.at[idx, col] = int(val)
            elif col in ['Age', 'Fare']:
                df.at[idx, col] = float(val)
            else:
                df.at[idx, col] = val
        update_table(tree, df)
        clear_form(entry_vars)
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể cập nhật:\n{str(e)}")

def delete_row(df, tree, entry_vars):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chưa chọn dòng", "Vui lòng chọn dòng cần xoá.")
        return
    idx = tree.index(selected[0])
    df.drop(df.index[idx], inplace=True)
    df.reset_index(drop=True, inplace=True)
    update_table(tree, df)
    clear_form(entry_vars)

def on_row_select(event, tree, cols, entry_vars):
    selected = tree.selection()
    if selected:
        values = tree.item(selected[0])['values']
        for col, val in zip(cols, values):
            entry_vars[col].set(val)
