import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import csv

class EmployeeManager:
    def __init__(self, filepath):
        self.filepath = filepath
        # ensure file exists
        try:
            with open(self.filepath, 'r', newline='', encoding='utf-8'):
                pass
        except FileNotFoundError:
            with open(self.filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Code', 'Name', 'Salary'])

    def get_all(self):
        with open(self.filepath, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)

    def exists(self, code):
        for emp in self.get_all():
            if emp['Code'] == code:
                return True
        return False

    def add(self, code, name, salary):
        if self.exists(code):
            return False
        with open(self.filepath, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([code, name, salary])
        return True

    def search(self, keyword):
        return [emp for emp in self.get_all() if keyword.lower() in emp['Code'].lower() or keyword.lower() in emp['Name'].lower()]

    def update(self, code, name, salary):
        updated = False
        employees = self.get_all()
        with open(self.filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Code', 'Name', 'Salary'])
            for emp in employees:
                if emp['Code'] == code:
                    writer.writerow([code, name, salary])
                    updated = True
                else:
                    writer.writerow([emp['Code'], emp['Name'], emp['Salary']])
        return updated

    def delete(self, code):
        removed = False
        employees = self.get_all()
        with open(self.filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Code', 'Name', 'Salary'])
            for emp in employees:
                if emp['Code'] == code:
                    removed = True
                    continue
                writer.writerow([emp['Code'], emp['Name'], emp['Salary']])
        return removed

class EmployeeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("مدیریت کارکنان CSV")
        self.root.geometry("700x500")
        self.manager = None
        self.style = ttk.Style(root)
        self.style.theme_use('clam')
        self.style.configure('Treeview',
            background='#f0f0f0',
            foreground='#000000',
            rowheight=25,
            fieldbackground='#f0f0f0')
        self.style.map('Treeview', background=[('selected', '#347083')], foreground=[('selected', 'white')])

        # ورودی‌ها
        frame = tk.Frame(root, bg='#e1f5fe', padx=10, pady=10)
        frame.pack(fill='x')
        tk.Label(frame, text="کد کارمند:", bg='#e1f5fe').grid(row=0, column=0, padx=5, pady=5)
        self.code_entry = tk.Entry(frame)
        self.code_entry.grid(row=0, column=1, padx=5)
        tk.Label(frame, text="نام:", bg='#e1f5fe').grid(row=0, column=2, padx=5)
        self.name_entry = tk.Entry(frame)
        self.name_entry.grid(row=0, column=3, padx=5)
        tk.Label(frame, text="حقوق:", bg='#e1f5fe').grid(row=0, column=4, padx=5)
        self.salary_entry = tk.Entry(frame)
        self.salary_entry.grid(row=0, column=5, padx=5)

        # دکمه‌ها
        btn_frame = tk.Frame(root, bg='#b3e5fc', padx=10, pady=10)
        btn_frame.pack(fill='x')
        tk.Button(btn_frame, text="انتخاب فایل", command=self.select_file, bg='#039be5', fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="افزودن", command=self.add, bg='#0288d1', fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="نمایش همه", command=self.show_all, bg='#0277bd', fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="جستجو", command=self.search, bg='#01579b', fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="به‌روزرسانی", command=self.update, bg='#006064', fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="حذف", command=self.delete, bg='#d32f2f', fg='white').pack(side='left', padx=5)

        # نمایش جدول
        self.tree = ttk.Treeview(root, columns=('Code','Name','Salary'), show='headings')
        self.tree.heading('Code', text='کد')
        self.tree.heading('Name', text='نام')
        self.tree.heading('Salary', text='حقوق')
        self.tree.pack(fill='both', expand=True, padx=10, pady=10)

    def select_file(self):
        path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV files','*.csv')])
        if path:
            self.manager = EmployeeManager(path)
            messagebox.showinfo("فایل انتخاب شد", f"مسیر فایل:{path}")

    def refresh_tree(self, rows):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for emp in rows:
            self.tree.insert('', 'end', values=(emp['Code'], emp['Name'], emp['Salary']))

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