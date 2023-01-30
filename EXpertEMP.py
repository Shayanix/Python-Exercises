import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import csv
import json
from datetime import datetime

class EmployeeManager:
    def __init__(self, filepath, storage_type='csv'):
        self.filepath = filepath
        self.storage_type = storage_type  # 'csv', 'txt', 'json'
        # initialize file with header or empty structure
        if self.storage_type == 'csv':
            try:
                with open(self.filepath, 'r', newline='', encoding='utf-8'):
                    pass
            except FileNotFoundError:
                with open(self.filepath, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Code', 'Name', 'Salary', 'CreatedAt', 'UpdatedAt'])
        elif self.storage_type == 'json':
            try:
                with open(self.filepath, 'r', encoding='utf-8'):
                    json.load(open(self.filepath, 'r', encoding='utf-8'))
            except (FileNotFoundError, json.JSONDecodeError):
                with open(self.filepath, 'w', encoding='utf-8') as f:
                    json.dump([], f, ensure_ascii=False, indent=2)
        elif self.storage_type == 'txt':
            try:
                with open(self.filepath, 'r', encoding='utf-8'):
                    pass
            except FileNotFoundError:
                with open(self.filepath, 'w', encoding='utf-8') as f:
                    f.write('Code,Name,Salary,CreatedAt,UpdatedAt\n')

    def _current_time(self):
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def get_all(self):
        if self.storage_type == 'csv':
            with open(self.filepath, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                return list(reader)
        elif self.storage_type == 'json':
            with open(self.filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:  # txt
            with open(self.filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            keys = lines[0].strip().split(',')
            data = []
            for line in lines[1:]:
                parts = line.strip().split(',')
                data.append({k: v for k, v in zip(keys, parts)})
            return data

    def exists(self, code):
        return any(emp['Code'] == code for emp in self.get_all())

    def add(self, code, name, salary):
        if self.exists(code):
            return False
        now = self._current_time()
        record = {'Code': code, 'Name': name, 'Salary': salary, 'CreatedAt': now, 'UpdatedAt': now}
        if self.storage_type == 'csv':
            with open(self.filepath, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(record.values())
        elif self.storage_type == 'json':
            data = self.get_all()
            data.append(record)
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        else:  # txt
            with open(self.filepath, 'a', encoding='utf-8') as f:
                f.write(','.join(record.values()) + '\n')
        return True

    def search(self, keyword):
        return [emp for emp in self.get_all()
                if keyword.lower() in emp['Code'].lower() or keyword.lower() in emp['Name'].lower()]

    def update(self, code, name, salary):
        updated = False
        data = self.get_all()
        now = self._current_time()
        for emp in data:
            if emp['Code'] == code:
                emp['Name'] = name or emp['Name']
                emp['Salary'] = salary or emp['Salary']
                emp['UpdatedAt'] = now
                updated = True
        if not updated:
            return False
        # write back
        if self.storage_type == 'csv' or self.storage_type == 'txt':
            with open(self.filepath, 'w', newline='', encoding='utf-8') as f:
                if self.storage_type == 'csv':
                    writer = csv.writer(f)
                    writer.writerow(['Code', 'Name', 'Salary', 'CreatedAt', 'UpdatedAt'])
                else:
                    f.write('Code,Name,Salary,CreatedAt,UpdatedAt\n')
                for emp in data:
                    f.write(','.join([emp['Code'], emp['Name'], emp['Salary'], emp['CreatedAt'], emp['UpdatedAt']]) + '\n')
        else:  # json
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        return True

    def delete(self, code):
        removed = False
        data = self.get_all()
        new_data = [emp for emp in data if emp['Code'] != code]
        removed = len(new_data) != len(data)
        # write back
        if self.storage_type == 'csv' or self.storage_type == 'txt':
            with open(self.filepath, 'w', newline='', encoding='utf-8') as f:
                if self.storage_type == 'csv':
                    writer = csv.writer(f)
                    writer.writerow(['Code', 'Name', 'Salary', 'CreatedAt', 'UpdatedAt'])
                else:
                    f.write('Code,Name,Salary,CreatedAt,UpdatedAt\n')
                for emp in new_data:
                    f.write(','.join([emp['Code'], emp['Name'], emp['Salary'], emp['CreatedAt'], emp['UpdatedAt']]) + '\n')
        else:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(new_data, f, ensure_ascii=False, indent=2)
        return removed

class EmployeeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("مدیریت کارکنان")
        self.root.geometry("800x550")
        self.manager = None

        # انتخاب نوع ذخیره‌سازی
        top_frame = tk.Frame(root, bg='#e0f7fa', pady=5)
        top_frame.pack(fill='x')
        tk.Label(top_frame, text="نوع فایل:", bg='#e0f7fa').pack(side='left', padx=5)
        self.storage_var = tk.StringVar(value='csv')
        for fmt in ['csv', 'txt', 'json']:
            tk.Radiobutton(top_frame, text=fmt.upper(), variable=self.storage_var,
                           value=fmt, bg='#e0f7fa').pack(side='left', padx=5)

        # فیلدهای ورودی
        frame = tk.Frame(root, bg='#e1f5fe', padx=10, pady=10)
        frame.pack(fill='x')
        tk.Label(frame, text="کد:", bg='#e1f5fe').grid(row=0, column=0, pady=5)
        self.code_entry = tk.Entry(frame)
        self.code_entry.grid(row=0, column=1, padx=5)
        tk.Label(frame, text="نام:", bg='#e1f5fe').grid(row=0, column=2)
        self.name_entry = tk.Entry(frame)
        self.name_entry.grid(row=0, column=3, padx=5)
        tk.Label(frame, text="حقوق:", bg='#e1f5fe').grid(row=0, column=4)
        self.salary_entry = tk.Entry(frame)
        self.salary_entry.grid(row=0, column=5, padx=5)

        # دکمه‌ها
        btn_frame = tk.Frame(root, bg='#b3e5fc', padx=10, pady=10)
        btn_frame.pack(fill='x')
        tk.Button(btn_frame, text="انتخاب فایل", command=self.select_file, bg='#0288d1', fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="افزودن", command=self.add, bg='#0277bd', fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="نمایش همه", command=self.show_all, bg='#01579b', fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="جستجو", command=self.search, bg='#014b72', fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="به‌روزرسانی", command=self.update, bg='#013440', fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="حذف", command=self.delete, bg='#b71c1c', fg='white').pack(side='left', padx=5)

        # جدول نمایش
        self.tree = ttk.Treeview(root, columns=('Code','Name','Salary','CreatedAt','UpdatedAt'), show='headings')
        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(fill='both', expand=True, padx=10, pady=10)

    def select_file(self):
        ext = self.storage_var.get()
        filetypes = [(f"{ext.upper()} files", f"*.{ext}")]
        path = filedialog.asksaveasfilename(defaultextension=f'.{ext}', filetypes=filetypes)
        if path:
            self.manager = EmployeeManager(path, storage_type=ext)
            messagebox.showinfo("فایل انتخاب شد", f"مسیر فایل:\n{path}")

    def refresh_tree(self, rows):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for emp in rows:
            self.tree.insert('', 'end', values=(emp['Code'], emp['Name'], emp['Salary'], emp['CreatedAt'], emp['UpdatedAt']))

    def add(self):
        if not self.manager: return
        code = self.code_entry.get().strip()
        name = self.name_entry.get().strip()
        salary = self.salary_entry.get().strip()
        if code and name and salary:
            if self.manager.add(code, name, salary):
                messagebox.showinfo("موفقیت", "کارمند اضافه شد.")
            else:
                messagebox.showerror("خطا", "کد تکراری است.")
            self.show_all()
        else:
            messagebox.showerror("خطا", "همه فیلدها را پر کنید.")

    def show_all(self):
        if not self.manager: return
        rows = self.manager.get_all()
        self.refresh_tree(rows)

    def search(self):
        if not self.manager: return
        key = self.code_entry.get().strip() or self.name_entry.get().strip()
        if not key:
            messagebox.showerror("خطا", "کد یا نام برای جستجو وارد کنید.")
            return
        rows = self.manager.search(key)
        self.refresh_tree(rows)

    def update(self):
        if not self.manager: return
        code = self.code_entry.get().strip()
        name = self.name_entry.get().strip()
        salary = self.salary_entry.get().strip()
        if not code:
            messagebox.showerror("خطا", "کد کارمند را وارد کنید.")
            return
        if self.manager.update(code, name, salary):
            messagebox.showinfo("موفقیت", "به‌روز شد.")
        else:
            messagebox.showerror("خطا", "کارمند پیدا نشد.")
        self.show_all()

    def delete(self):
        if not self.manager: return
        code = self.code_entry.get().strip()
        if not code:
            messagebox.showerror("خطا", "کد کارمند را وارد کنید.")
            return
        if self.manager.delete(code):
            messagebox.showinfo("موفقیت", "کارمند حذف شد.")
        else:
            messagebox.showerror("خطا", "کارمند پیدا نشد.")
        self.show_all()

if __name__ == '__main__':
    root = tk.Tk()
    app = EmployeeApp(root)
    root.mainloop()
