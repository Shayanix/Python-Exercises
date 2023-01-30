
import csv
import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime

DATA_FILE = "inventory.csv"
SALES_LOG = "sales.csv"

# --- Class for managing the shop ---
class Shop:
    def __init__(self, filename=DATA_FILE):
        self.filename = filename
        self.products = self.load_inventory()

    def load_inventory(self):
        try:
            with open(self.filename, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                return list(reader)
        except FileNotFoundError:
            return []

    def save_inventory(self):
        with open(self.filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['name', 'buy_price', 'sell_price', 'stock'])
            writer.writeheader()
            for product in self.products:
                writer.writerow(product)

    def add_product(self, name, buy_price, sell_price, stock):
        if any(p['name'] == name for p in self.products):
            raise ValueError("محصولی با این نام قبلاً اضافه شده است.")
        self.products.append({
            'name': name,
            'buy_price': str(buy_price),
            'sell_price': str(sell_price),
            'stock': str(stock)
        })
        self.save_inventory()

    def sell_product(self, name, quantity):
        for product in self.products:
            if product['name'] == name:
                current_stock = int(product['stock'])
                if current_stock < quantity:
                    raise ValueError("موجودی کافی نیست.")
                product['stock'] = str(current_stock - quantity)
                self.save_inventory()
                self.log_sale(name, int(product['sell_price']), quantity)
                return
        raise ValueError("محصول یافت نشد.")

    def log_sale(self, name, price, quantity):
        with open(SALES_LOG, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([datetime.now().strftime('%Y-%m-%d'), name, price, quantity])

    def search_product(self, name):
        return [p for p in self.products if name.lower() in p['name'].lower()]

    def generate_report(self, start_date=None, end_date=None):
        try:
            with open(SALES_LOG, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                sales = list(reader)
        except FileNotFoundError:
            return "هیچ فروشی ثبت نشده است."

        report = {}
        for row in sales:
            date, name, price, qty = row
            if start_date and date < start_date:
                continue
            if end_date and date > end_date:
                continue
            qty = int(qty)
            price = int(price)
            if name not in report:
                report[name] = {'qty': 0, 'total': 0}
            report[name]['qty'] += qty
            report[name]['total'] += price * qty

        if not report:
            return "هیچ فروشی در این بازه ثبت نشده است."

        result = ""
        for name, data in report.items():
            result += f"{name}: {data['qty']} عدد، مجموع فروش: {data['total']} تومان\n"
        return result

# --- CLI Interface ---
def run_cli(shop):
    while True:
        print("\n---- سیستم مدیریت فروشگاه ----")
        print("1. افزودن کالا")
        print("2. فروش کالا")
        print("3. جستجوی کالا")
        print("4. گزارش فروش")
        print("5. خروج")

        choice = input("انتخاب شما: ")

        try:
            if choice == '1':
                name = input("نام کالا: ")
                buy = int(input("قیمت خرید: "))
                sell = int(input("قیمت فروش: "))
                stock = int(input("موجودی اولیه: "))
                shop.add_product(name, buy, sell, stock)
                print("✅ کالا اضافه شد.")
            elif choice == '2':
                name = input("نام کالا: ")
                qty = int(input("تعداد فروش: "))
                shop.sell_product(name, qty)
                print("✅ فروش ثبت شد.")
            elif choice == '3':
                name = input("نام کالا برای جستجو: ")
                results = shop.search_product(name)
                for p in results:
                    print(p)
            elif choice == '4':
                start = input("تاریخ شروع (YYYY-MM-DD) یا Enter: ")
                end = input("تاریخ پایان (YYYY-MM-DD) یا Enter: ")
                report = shop.generate_report(start or None, end or None)
                print(report)
            elif choice == '5':
                break
            else:
                print("❌ انتخاب نامعتبر.")
        except Exception as e:
            print(f"⚠️ خطا: {e}")

# --- Tkinter GUI Interface ---
def run_gui(shop):
    root = tk.Tk()
    root.title("سیستم مدیریت فروشگاه")
    root.geometry("400x400")
    root.resizable(False, False)

    def add_product():
        form = tk.Toplevel(root)
        form.geometry("300x200")
        form.resizable(False, False)
        form.title("افزودن کالا")

        tk.Label(form, text="نام کالا").grid(row=0, column=0)
        tk.Label(form, text="قیمت خرید").grid(row=1, column=0)
        tk.Label(form, text="قیمت فروش").grid(row=2, column=0)
        tk.Label(form, text="موجودی").grid(row=3, column=0)

        name_entry = tk.Entry(form)
        buy_entry = tk.Entry(form)
        sell_entry = tk.Entry(form)
        stock_entry = tk.Entry(form)

        name_entry.grid(row=0, column=1)
        buy_entry.grid(row=1, column=1)
        sell_entry.grid(row=2, column=1)
        stock_entry.grid(row=3, column=1)

        def submit():
            try:
                name = name_entry.get()
                buy = int(buy_entry.get())
                sell = int(sell_entry.get())
                stock = int(stock_entry.get())
                shop.add_product(name, buy, sell, stock)
                messagebox.showinfo("موفق", "کالا اضافه شد.")
                name_entry.delete(0, tk.END)
                buy_entry.delete(0, tk.END)
                sell_entry.delete(0, tk.END)
                stock_entry.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("خطا", str(e))

        tk.Button(form, text="ثبت", command=submit).grid(row=4, column=0, columnspan=2)

    def sell_product():
        form = tk.Toplevel(root)
        form.geometry("300x200")
        form.resizable(False, False)
        form.title("فروش کالا")

        available_products = [p['name'] for p in shop.products if int(p['stock']) > 0]

        if not available_products:
            messagebox.showinfo("عدم موجودی", "هیچ کالایی برای فروش وجود ندارد.")
            form.destroy()
            return

        tk.Label(form, text="انتخاب کالا").grid(row=0, column=0)
        tk.Label(form, text="تعداد فروش").grid(row=1, column=0)

        product_var = tk.StringVar()
        product_var.set(available_products[0])

        product_menu = tk.OptionMenu(form, product_var, *available_products)
        qty_entry = tk.Entry(form)

        product_menu.grid(row=0, column=1)
        qty_entry.grid(row=1, column=1)

        def submit():
            try:
                name = product_var.get()
                qty = int(qty_entry.get())
                shop.sell_product(name, qty)
                messagebox.showinfo("موفق", f"{qty} عدد از {name} فروخته شد.")
                qty_entry.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("خطا", str(e))

        tk.Button(form, text="ثبت", command=submit).grid(row=2, column=0, columnspan=2)

    def search_product():
        name = simpledialog.askstring("جستجو", "نام کالا:")
        results = shop.search_product(name)
        result_text = "\n".join([f"{p['name']} | قیمت فروش: {p['sell_price']} | موجودی: {p['stock']}" for p in results])
        messagebox.showinfo("نتیجه جستجو", result_text or "موردی یافت نشد.")

    def report_by_date():
        form = tk.Toplevel(root)
        form.geometry("300x200")
        form.resizable(False, False)
        form.title("گزارش فروش با تاریخ")

        tk.Label(form, text="تاریخ شروع (YYYY-MM-DD)").grid(row=0, column=0)
        tk.Label(form, text="تاریخ پایان (YYYY-MM-DD)").grid(row=1, column=0)

        start_entry = tk.Entry(form)
        end_entry = tk.Entry(form)

        start_entry.grid(row=0, column=1)
        end_entry.grid(row=1, column=1)

        def submit():
            start = start_entry.get()
            end = end_entry.get()
            result = shop.generate_report(start or None, end or None)
            messagebox.showinfo("گزارش فروش", result)

        tk.Button(form, text="نمایش گزارش", command=submit).grid(row=2, column=0, columnspan=2)

    def report_all():
        result = shop.generate_report()
        messagebox.showinfo("گزارش کل فروش", result)
        
    def show_inventory():
        inv_window = tk.Toplevel(root)
        inv_window.title("لیست موجودی فروشگاه")
        inv_window.geometry("600x400")
        inv_window.resizable(False, False)

        text = tk.Text(inv_window)
        text.pack(expand=True, fill='both')

        if not shop.products:
            text.insert('end', "هیچ کالایی موجود نیست.")
        else:
            for p in shop.products:
                line = f"{p['name']} | قیمت خرید: {p['buy_price']} | قیمت فروش: {p['sell_price']} | موجودی: {p['stock']}\n"
                text.insert('end', line)
        text.config(state='disabled')


    tk.Button(root, text="افزودن کالا", width=30, command=add_product).pack(pady=5)
    tk.Button(root, text="فروش کالا", width=30, command=sell_product).pack(pady=5)
    tk.Button(root, text="جستجوی کالا", width=30, command=search_product).pack(pady=5)
    tk.Button(root, text="گزارش فروش (همه)", width=30, command=report_all).pack(pady=5)
    tk.Button(root, text="گزارش فروش با تاریخ", width=30, command=report_by_date).pack(pady=5)
    tk.Button(root, text="موجودی فروشگاه", width=30, command=show_inventory).pack(pady=5)
    tk.Button(root, text="خروج", width=30, command=root.destroy).pack(pady=10)

    root.mainloop()

# --- Start ---
if __name__ == "__main__":
    shop = Shop()

    print("1. رابط متنی")
    print("2. رابط گرافیکی Tkinter")
    interface = input("نوع رابط را انتخاب کنید (1 یا 2): ")

    if interface == '1':
        run_cli(shop)
    elif interface == '2':
        run_gui(shop)
    else:
        print("❌ انتخاب نامعتبر.")
