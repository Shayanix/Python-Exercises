import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class Employee:
    def __init__(self, code, last_name, salary):
        self.code = code
        self.last_name = last_name
        self.salary = salary

    def to_string(self):
        return f"{self.code},{self.last_name},{self.salary}"

class EmployeeFileManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.employees = []

    def load_data(self):
        self.employees.clear()
        if not os.path.exists(self.file_path):
            return
        with open(self.file_path, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) == 3:
                    code, last_name, salary = parts
                    self.employees.append(Employee(code, last_name, salary))

    def save_data(self):
        with open(self.file_path, 'w', encoding='utf-8') as file:
            for emp in self.employees:
                file.write(emp.to_string() + '\n')

    def display(self):
        return [emp.to_string() for emp in self.employees]

    def update(self, code, last_name, salary):
        found = False
        for emp in self.employees:
            if emp.code == code:
                emp.last_name = last_name
                emp.salary = salary
                found = True
                break
        if not found:
            # اگر کارمند پیدا نشد، افزودن جدید
            self.employees.append(Employee(code, last_name, salary))
        self.save_data()

    def search(self, search_term, search_by='code'):
        results = []
        for emp in self.employees:
            if search_by == 'code' and emp.code == search_term:
                results.append(emp)
            elif search_by == 'last_name' and emp.last_name == search_term:
                results.append(emp)
        return results

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("مدیریت کارکنان")
        self.file_manager = None

        # قسمت انتخاب مسیر فایل
        self.frame_top = tk.Frame(root)
        self.frame_top.pack(pady=10)

        self.btn_browse = tk.Button(self.frame_top, text="انتخاب مسیر فایل", command=self.browse_file)
        self.btn_browse.pack(side=tk.LEFT)

        self.lbl_path = tk.Label(self.frame_top, text="مسیر فایل انتخاب نشده")
        self.lbl_path.pack(side=tk.LEFT, padx=10)

        # قسمت عملیات
        self.frame_ops = tk.Frame(root)
        self.frame_ops.pack(pady=10)

        # ورودی‌های اطلاعات کارمند
        tk.Label(self.frame_ops, text="کد کارمند:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_code = tk.Entry(self.frame_ops)
        self.entry_code.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.frame_ops, text="نام خانوادگی:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_last_name = tk.Entry(self.frame_ops)
        self.entry_last_name.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.frame_ops, text="حقوق:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_salary = tk.Entry(self.frame_ops)
        self.entry_salary.grid(row=2, column=1, padx=5, pady=5)

        # دکمه‌های عملیات
        self.btn_update = tk.Button(self.frame_ops, text="به‌روزرسانی/افزودن", command=self.update_employee)
        self.btn_update.grid(row=3, column=0, padx=5, pady=5)

        self.btn_display = tk.Button(self.frame_ops, text="نمایش محتویات", command=self.display_employees)
        self.btn_display.grid(row=3, column=1, padx=5, pady=5)

        # قسمت جستجو
        self.frame_search = tk.Frame(root)
        self.frame_search.pack(pady=10)

        self.search_var = tk.StringVar()
        self.search_by_var = tk.StringVar(value='code')

        tk.Radiobutton(self.frame_search, text='کد کارمند', variable=self.search_by_var, value='code').pack(side=tk.LEFT)
        tk.Radiobutton(self.frame_search, text='نام خانوادگی', variable=self.search_by_var, value='last_name').pack(side=tk.LEFT)

        self.entry_search = tk.Entry(self.frame_search)
        self.entry_search.pack(side=tk.LEFT, padx=5)

        self.btn_search = tk.Button(self.frame_search, text="جستجو", command=self.search_employee)
        self.btn_search.pack(side=tk.LEFT, padx=5)

        # قسمت نمایش نتایج
        self.tree = ttk.Treeview(root, columns=('کد', 'نام خانوادگی', 'حقوق'), show='headings')
        self.tree.heading('کد', text='کد کارمند')
        self.tree.heading('نام خانوادگی', text='نام خانوادگی')
        self.tree.heading('حقوق', text='حقوق دریافتی')
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

    def browse_file(self):
        path = filedialog.askopenfilename()
        if path:
            self.lbl_path.config(text=path)
            self.file_manager = EmployeeFileManager(path)
            self.file_manager.load_data()
            self.display_employees()

    def display_employees(self):
        if self.file_manager:
            # پاک کردن آیتم‌های قبلی
            for item in self.tree.get_children():
                self.tree.delete(item)
            # افزودن داده‌ها
            for emp_str in self.file_manager.display():
                code, last_name, salary = emp_str.split(',')
                self.tree.insert('', 'end', values=(code, last_name, salary))
        else:
            messagebox.showwarning("خطا", "لطفاً ابتدا مسیر فایل را انتخاب کنید.")

    def update_employee(self):
        if self.file_manager:
            code = self.entry_code.get().strip()
            last_name = self.entry_last_name.get().strip()
            salary = self.entry_salary.get().strip()

            if not code or not last_name or not salary:
                messagebox.showwarning("خطا", "تمام فیلدها باید پر شوند.")
                return

            self.file_manager.update(code, last_name, salary)
            self.display_employees()
        else:
            messagebox.showwarning("خطا", "لطفاً ابتدا مسیر فایل را انتخاب کنید.")

    def search_employee(self):
        if self.file_manager:
            search_term = self.entry_search.get().strip()
            if not search_term:
                messagebox.showwarning("خطا", "لطفاً متن جستجو را وارد کنید.")
                return
            results = self.file_manager.search(search_term, self.search_by_var.get())

            # پاک کردن آیتم‌های قبلی
            for item in self.tree.get_children():
                self.tree.delete(item)

            if results:
                for emp in results:
                    self.tree.insert('', 'end', values=(emp.code, emp.last_name, emp.salary))
            else:
                messagebox.showinfo("نتیجه", "موردی یافت نشد.")
        else:
            messagebox.showwarning("خطا", "لطفاً ابتدا مسیر فایل را انتخاب کنید.")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
