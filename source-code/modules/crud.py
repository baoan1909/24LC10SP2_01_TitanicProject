from tkinter import messagebox

def clear_form(entry_vars):
    for var in entry_vars.values():
        var.set("")

def update_table(tree, df, page=0, rows_per_page=50):
    tree.delete(*tree.get_children())
    start = page * rows_per_page
    end = start + rows_per_page
    page_data = df.iloc[start:end]
    for _, row in page_data.iterrows():
        tree.insert('', 'end', values=list(row))

def update_page_info(current_page_var, page_info_var, df, rows_per_page):
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

def add_row(df, cols, entry_vars, tree):
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
        passenger_id = int(tree.item(selected[0])['values'][0])
        idx = df[df['PassengerId'] == passenger_id].index[0]

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
        messagebox.showinfo("Thành công", "Cập nhật thành công!")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể cập nhật:\n{str(e)}")

def delete_row(df, tree, entry_vars):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chưa chọn dòng", "Vui lòng chọn dòng cần xoá.")
        return
    try:
        passenger_id = int(tree.item(selected[0])['values'][0])

        idx = df[df['PassengerId'] == passenger_id].index[0]

        df.drop(idx, inplace=True)
        df.reset_index(drop=True, inplace=True)

        update_table(tree, df)
        clear_form(entry_vars)
        messagebox.showinfo("Thành công", "Đã xoá hành khách.")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể xoá:\n{str(e)}")


def on_row_select(event, tree, cols, entry_vars):
    selected = tree.selection()
    if selected:
        values = tree.item(selected[0])['values']
        for col, val in zip(cols, values):
            entry_vars[col].set(val)



