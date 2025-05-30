from tkinter import messagebox

# entry_vars một từ điển chứa dữ liệu nhập vào từ Entry
# table là bảng dữ liệu liệu Treeview
# df dữ liệu Dataframe
# page số trang, rows_per_page số dòng trên một trang
# current_page_var Số trang thay đổi
# page_info_var thông tin về số trang hiện tại và tổng số trang
# goto_page_var số trang muốn đến
# sex_value, pclass_value giá trị của bộ lọc


# Dọn dẹp ô nhập dữ liệu
def clear_form(entry_vars):
    for var in entry_vars.values():
        var.set("")

# Cập nhật dữ liệu bảng
def update_table(table, df, page=0, rows_per_page=50):
    table.delete(*table.get_children())
    start = page * rows_per_page
    end = start + rows_per_page
    page_data = df.iloc[start:end]
    for _, row in page_data.iterrows():
        table.insert('', 'end', values=list(row))

# Cập nhật hiển thị số trang
def update_page_info(current_page_var, page_info_var, df, rows_per_page):
    total_pages = (len(df) - 1) // rows_per_page + 1
    current = current_page_var.get() + 1
    page_info_var.set(f"Trang {current} / {total_pages}")

# Lùi trang
def previous_page(df, current_page_var, rows_per_page, table, page_info_var):
    if current_page_var.get() > 0:
        current_page_var.set(current_page_var.get() - 1)
        update_table(table, df, current_page_var.get(), rows_per_page)
        update_page_info(current_page_var, page_info_var, df, rows_per_page)

# Trang tiếp theo
def next_page(df, current_page_var, rows_per_page, table, page_info_var):
    total_pages = (len(df) - 1) // rows_per_page
    if current_page_var.get() < total_pages:
        current_page_var.set(current_page_var.get() + 1)
        update_table(table, df, current_page_var.get(), rows_per_page)
        update_page_info(current_page_var, page_info_var, df, rows_per_page)

# Điền số trang muốn đến và đi đến trang đó
def go_to_page(df, goto_page_var, current_page_var, rows_per_page, table, page_info_var):
    try:
        page_number = int(goto_page_var.get()) - 1  # vì trang hiển thị bắt đầu từ 1
        total_pages = (len(df) - 1) // rows_per_page

        if 0 <= page_number <= total_pages:
            current_page_var.set(page_number)
            update_table(table, df, page_number, rows_per_page)
            update_page_info(current_page_var, page_info_var, df, rows_per_page)
        else:
            messagebox.showwarning("Cảnh báo", f"Số trang phải từ 1 đến {total_pages + 1}")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Số trang không hợp lệ:\n{str(e)}")

# Lọc Dữ liệu
def filter_data(df, sex_value, pclass_value, keyword):
    filtered = df.copy()
    if sex_value != "Tất cả":
        filtered = filtered[filtered['Sex'] == sex_value]
    if pclass_value != "Tất cả":
        filtered = filtered[filtered['Pclass'] == int(pclass_value)]
    if keyword == "":
        filtered = filtered
    else:
        if keyword.isdigit():
            filtered = filtered[filtered["PassengerId"] == int(keyword)]
        else:
            filtered = filtered[filtered["Name"].str.lower().str.contains(keyword, na=False)]
    return filtered

# Thêm mới dữ liệu
def add_row(df, cols, entry_vars, table):
    try:
        new_data = {col: entry_vars[col].get() for col in cols if col != 'PassengerId'}

        new_id = int(df['PassengerId'].max()) + 1 if not df.empty else 1
        new_data['PassengerId'] = new_id

        new_data['Survived'] = int(new_data['Survived'])
        new_data['Pclass'] = int(new_data['Pclass'])
        new_data['Age'] = float(new_data['Age'])
        new_data['SibSp'] = int(new_data['SibSp'])
        new_data['Parch'] = int(new_data['Parch'])
        new_data['Fare'] = float(new_data['Fare'])

        df.loc[len(df)] = new_data
        update_table(table, df)
        clear_form(entry_vars)

        messagebox.showinfo("Thành công", "Thêm hành khách thành công!")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Dữ liệu không hợp lệ:\n{str(e)}")

# cập nhật dữ liệu
def edit_row(df, cols, entry_vars, table):
    selected = table.selection()
    if not selected:
        messagebox.showwarning("Chưa chọn dòng", "Vui lòng chọn dòng cần sửa.")
        return
    try:
        passenger_id = int(table.item(selected[0])['values'][0])
        idx = df[df['PassengerId'] == passenger_id].index[0]

        for col in cols:
            val = entry_vars[col].get()
            if col in ['PassengerId', 'Pclass', 'SibSp', 'Parch', 'Survived']:
                df.at[idx, col] = int(val)
            elif col in ['Age', 'Fare']:
                df.at[idx, col] = float(val)
            else:
                df.at[idx, col] = val

        update_table(table, df)
        clear_form(entry_vars)
        messagebox.showinfo("Thành công", "Cập nhật thành công!")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể cập nhật:\n{str(e)}")

# xóa một bản ghi
def delete_row(df, table, entry_vars):
    selected = table.selection()
    if not selected:
        messagebox.showwarning("Chưa chọn dòng", "Vui lòng chọn dòng cần xoá.")
        return
    
     # Hỏi xác nhận
    confirm = messagebox.askyesno("Xác nhận xoá", "Bạn có chắc chắn muốn xoá dòng đã chọn không?")
    if not confirm:
        return

    try:
        passenger_id = int(table.item(selected[0])['values'][0])

        idx = df[df['PassengerId'] == passenger_id].index[0]

        df.drop(idx, inplace=True)
        df.reset_index(drop=True, inplace=True)

        update_table(table, df)
        clear_form(entry_vars)
        messagebox.showinfo("Thành công", "Đã xoá hành khách.")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể xoá:\n{str(e)}")

# chọn một bản ghi
def on_row_select(event,table, cols, entry_vars):
    selected = table.selection()
    if selected:
        values = table.item(selected[0])['values']
        for col, val in zip(cols, values):
            entry_vars[col].set(val)



