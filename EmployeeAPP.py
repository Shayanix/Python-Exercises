import tkinter as tk
from tkinter import filedialog, messagebox

class EmployeeManager:
    def __init__(self, filepath):
        self.filepath = filepath

    def exists(self, code):
        for line in self.get_all_employees():
            if line.strip().split(',')[0] == code:
                return True
        return False

    def add_employee(self, code, name, salary):
        if self.exists(code):
            return False
        with open(self.filepath, 'a', encoding='utf-8') as f:
            f.write(f"{code},{name},{salary}\n")
        return True

    def get_all_employees(self):
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                return f.readlines()
        except FileNotFoundError:
            return []

    def search_employee(self, keyword):
        results = []
        for line in self.get_all_employees():
            if keyword in line:
                results.append(line)
        return results

    def update_employee(self, code, new_name, new_salary):
        lines = self.get_all_employees()
        updated = False
        with open(self.filepath, 'w', encoding='utf-8') as f:
            for line in lines:
                parts = line.strip().split(',')
                if parts[0] == code:
                    f.write(f"{code},{new_name},{new_salary}\n")
                    updated = True
                else:
                    f.write(line)
        return updated

class EmployeeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("مدیریت کارکنان")
        self.manager = None

        self.code_entry = self._make_entry("کد کارمند", 0)
        self.name_entry = self._make_entry("نام خانوادگی", 1)
        self.salary_entry = self._make_entry("حقوق", 2)

        self.output = tk.Text(root, height=10, width=60)
        self.output.grid(row=6, column=0, columnspan=3, padx=5, pady=5)

        tk.Button(root, text="انتخاب فایل", command=self.select_file).grid(row=3, column=0)
        tk.Button(root, text="افزودن", command=self.add).grid(row=3, column=1)
        tk.Button(root, text="نمایش همه", command=self.show_all).grid(row=4, column=0)
        tk.Button(root, text="جستجو", command=self.search).grid(row=4, column=1)
        tk.Button(root, text="به‌روزرسانی", command=self.update).grid(row=5, column=0)

    def _make_entry(self, label, row):
        tk.Label(self.root, text=label).grid(row=row, column=0)
        entry = tk.Entry(self.root)
        entry.grid(row=row, column=1)
        return entry

    def select_file(self):
        path = filedialog.asksaveasfilename(defaultextension=".txt")
        if path:
            self.manager = EmployeeManager(path)
            messagebox.showinfo("فایل انتخاب شد", f"مسیر فایل:\n{path}")

    def add(self):
        if not self.manager:
            return
        code = self.code_entry.get().strip()
        name = self.name_entry.get().strip()
        salary = self.salary_entry.get().strip()
        if code and name and salary:
            success = self.manager.add_employee(code, name, salary)
            if success:
                self.output.insert(tk.END, "✅ کارمند با موفقیت اضافه شد.\n")
            else:
                self.output.insert(tk.END, "❌ این کد کارمند قبلاً ثبت شده است.\n")
        else:
            messagebox.showerror("خطا", "همه فیلدها را پر کنید.")

    def show_all(self):
        if not self.manager:
            return
        self.output.delete(1.0, tk.END)
        lines = self.manager.get_all_employees()
        if lines:
            self.output.insert(tk.END, "📋 لیست کارکنان:\n")
            for line in lines:
                parts = line.strip().split(',')
                if len(parts) == 3:
                    self.output.insert(tk.END, f"کد: {parts[0]} | نام خانوادگی: {parts[1]} | حقوق: {parts[2]}\n")
        else:
            self.output.insert(tk.END, "هیچ اطلاعاتی موجود نیست.\n")

    def search(self):
        if not self.manager:
            return
        keyword = self.code_entry.get().strip() or self.name_entry.get().strip()
        if not keyword:
            messagebox.showerror("خطا", "کد یا نام را برای جستجو وارد کنید.")
            return
        self.output.delete(1.0, tk.END)
        results = self.manager.search_employee(keyword)
        if results:
            self.output.insert(tk.END, "🔍 نتایج جستجو:\n")
            for res in results:
                parts = res.strip().split(',')
                self.output.insert(tk.END, f"کد: {parts[0]} | نام: {parts[1]} | حقوق: {parts[2]}\n")
        else:
            self.output.insert(tk.END, "❌ نتیجه‌ای یافت نشد.\n")

    def update(self):
        if not self.manager:
            return
        code = self.code_entry.get().strip()
        name = self.name_entry.get().strip()
        salary = self.salary_entry.get().strip()
        if not code:
            messagebox.showerror("خطا", "کد کارمند را وارد کنید.")
            return
        updated = self.manager.update_employee(code, name, salary)
        if updated:
            self.output.insert(tk.END, "✅ اطلاعات به‌روزرسانی شد.\n")
        else:
            self.output.insert(tk.END, "❌ کارمند با این کد پیدا نشد.\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeApp(root)
    root.mainloop()
