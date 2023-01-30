# filepath: c:\Users\Shayan\Desktop\Python\shopapp.py

import sqlite3
import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

# Class representing a product in the shop
class Shop:
    def __init__(self, manager, id, name, purchase_price, selling_price, inventory):
        self.manager = manager  # Reference to ShopManager for database operations
        self.id = id
        self.name = name
        self.purchase_price = purchase_price
        self.selling_price = selling_price
        self.inventory = inventory

    def add_inventory(self, amount):
        """Increase inventory by the specified amount."""
        if amount < 0:
            raise ValueError("Amount to add cannot be negative")
        self.manager.add_inventory(self.id, amount)
        self.inventory += amount

    def sell(self, quantity):
        """Sell the specified quantity, updating inventory."""
        if quantity < 0:
            raise ValueError("Quantity to sell cannot be negative")
        if self.inventory < quantity:
            raise ValueError("Not enough inventory to sell")
        self.manager.sell(self.id, quantity)
        self.inventory -= quantity

# Class managing the shop's database and operations
class ShopManager:
    def __init__(self, db_name='shop.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        """Create products and sales tables if they don't exist."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                purchase_price REAL NOT NULL,
                selling_price REAL NOT NULL,
                inventory INTEGER NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
        self.conn.commit()

    def add_product(self, name, purchase_price, selling_price, inventory):
        """Add a new product to the database."""
        if purchase_price < 0 or selling_price < 0 or inventory < 0:
            raise ValueError("Prices and inventory must be non-negative")
        self.cursor.execute('''
            INSERT INTO products (name, purchase_price, selling_price, inventory)
            VALUES (?, ?, ?, ?)
        ''', (name, purchase_price, selling_price, inventory))
        self.conn.commit()
        product_id = self.cursor.lastrowid
        return Shop(self, product_id, name, purchase_price, selling_price, inventory)

    def add_inventory(self, product_id, amount):
        """Increase inventory for a product."""
        self.cursor.execute('SELECT id FROM products WHERE id = ?', (product_id,))
        if not self.cursor.fetchone():
            raise ValueError("Product not found")
        self.cursor.execute('''
            UPDATE products SET inventory = inventory + ? WHERE id = ?
        ''', (amount, product_id))
        self.conn.commit()

    def sell(self, product_id, quantity):
        """Record a sale and update inventory."""
        self.cursor.execute('SELECT inventory FROM products WHERE id = ?', (product_id,))
        result = self.cursor.fetchone()
        if not result:
            raise ValueError("Product not found")
        if result[0] < quantity:
            raise ValueError("Not enough inventory")
        self.cursor.execute('UPDATE products SET inventory = inventory - ? WHERE id = ?', 
                           (quantity, product_id))
        timestamp = datetime.datetime.now().isoformat()
        self.cursor.execute('INSERT INTO sales (product_id, quantity, timestamp) VALUES (?, ?, ?)',
                           (product_id, quantity, timestamp))
        self.conn.commit()

    def search_products(self, name):
        """Search for products by name."""
        self.cursor.execute('''
            SELECT id, name, purchase_price, selling_price, inventory
            FROM products WHERE name LIKE ?
        ''', ('%' + name + '%',))
        return [Shop(self, *row) for row in self.cursor.fetchall()]

    def generate_sales_report(self, start_date, end_date):
        """Generate a sales report for a specific period."""
        self.cursor.execute('''
            SELECT p.id, p.name, SUM(s.quantity), SUM(s.quantity * p.selling_price)
            FROM sales s JOIN products p ON s.product_id = p.id
            WHERE s.timestamp >= ? AND s.timestamp <= ?
            GROUP BY p.id, p.name
        ''', (start_date, end_date + ' 23:59:59'))
        results = self.cursor.fetchall()
        total_quantity = sum(row[2] for row in results)
        total_revenue = sum(row[3] for row in results)
        return results, total_quantity, total_revenue

    def __del__(self):
        """Close the database connection when the object is destroyed."""
        self.conn.close()

# Text-based User Interface
def text_ui(manager):
    while True:
        print("\n*** سیستم مدیریت فروشگاه ***")
        print("1. اضافه کردن کالای جدید")
        print("2. افزودن به موجودی")
        print("3. فروش کالا")
        print("4. جستجوی کالاها")
        print("5. گزارش فروش")
        print("6. خروج")
        choice = input("گزینه را انتخاب کنید: ")
        try:
            if choice == '1':
                name = input("نام کالا: ")
                purchase_price = float(input("قیمت خرید: "))
                selling_price = float(input("قیمت فروش: "))
                inventory = int(input("موجودی اولیه: "))
                manager.add_product(name, purchase_price, selling_price, inventory)
                print("کالا با موفقیت اضافه شد.")
            elif choice == '2':
                product_id = int(input("شناسه کالا: "))
                amount = int(input("مقدار اضافه شده: "))
                manager.add_inventory(product_id, amount)
                print("موجودی به‌روزرسانی شد.")
            elif choice == '3':
                product_id = int(input("شناسه کالا: "))
                quantity = int(input("تعداد فروخته شده: "))
                manager.sell(product_id, quantity)
                print("فروش ثبت شد.")
            elif choice == '4':
                name = input("نام کالا برای جستجو: ")
                products = manager.search_products(name)
                for p in products:
                    print(f"شناسه: {p.id}, نام: {p.name}, موجودی: {p.inventory}")
            elif choice == '5':
                start_date = input("تاریخ شروع (YYYY-MM-DD): ")
                end_date = input("تاریخ پایان (YYYY-MM-DD): ")
                results, total_qty, total_rev = manager.generate_sales_report(start_date, end_date)
                for row in results:
                    print(f"شناسه: {row[0]}, نام: {row[1]}, تعداد: {row[2]}, درآمد: {row[3]}")
                print(f"مجموع تعداد: {total_qty}, مجموع درآمد: {total_rev}")
            elif choice == '6':
                print("خروج از برنامه.")
                break
            else:
                print("گزینه نامعتبر!")
        except ValueError as e:
            print(f"خطا: {e}")
        except Exception as e:
            print(f"خطای غیرمنتظره: {e}")

# Tkinter Graphical User Interface
class ShopApp:
    def __init__(self, root, manager):
        self.root = root
        self.manager = manager
        self.root.title("سیستم مدیریت فروشگاه")
        self.root.geometry("400x300")
        
        # Main menu buttons
        tk.Button(root, text="اضافه کردن کالا", command=self.add_product).pack(pady=5)
        tk.Button(root, text="افزودن به موجودی", command=self.add_inventory).pack(pady=5)
        tk.Button(root, text="فروش کالا", command=self.sell_product).pack(pady=5)
        tk.Button(root, text="جستجوی کالاها", command=self.search_products).pack(pady=5)
        tk.Button(root, text="گزارش فروش", command=self.generate_report).pack(pady=5)

    def add_product(self):
        name = simpledialog.askstring("ورودی", "نام کالا:")
        if name:
            try:
                purchase_price = simpledialog.askfloat("ورودی", "قیمت خرید:")
                selling_price = simpledialog.askfloat("ورودی", "قیمت فروش:")
                inventory = simpledialog.askinteger("ورودی", "موجودی اولیه:")
                if all(x is not None for x in [purchase_price, selling_price, inventory]):
                    self.manager.add_product(name, purchase_price, selling_price, inventory)
                    messagebox.showinfo("موفقیت", "کالا با موفقیت اضافه شد.")
            except ValueError as e:
                messagebox.showerror("خطا", str(e))

    def add_inventory(self):
        product_id = simpledialog.askinteger("ورودی", "شناسه کالا:")
        if product_id:
            try:
                amount = simpledialog.askinteger("ورودی", "مقدار اضافه شده:")
                if amount is not None:
                    self.manager.add_inventory(product_id, amount)
                    messagebox.showinfo("موفقیت", "موجودی به‌روزرسانی شد.")
            except ValueError as e:
                messagebox.showerror("خطا", str(e))

    def sell_product(self):
        product_id = simpledialog.askinteger("ورودی", "شناسه کالا:")
        if product_id:
            try:
                quantity = simpledialog.askinteger("ورودی", "تعداد فروخته شده:")
                if quantity is not None:
                    self.manager.sell(product_id, quantity)
                    messagebox.showinfo("موفقیت", "فروش ثبت شد.")
            except ValueError as e:
                messagebox.showerror("خطا", str(e))

    def search_products(self):
        name = simpledialog.askstring("ورودی", "نام کالا برای جستجو:")
        if name:
            products = self.manager.search_products(name)
            search_win = tk.Toplevel(self.root)
            search_win.title("نتایج جستجو")
            tree = ttk.Treeview(search_win, columns=("ID", "Name", "Inventory"), show="headings")
            tree.heading("ID", text="شناسه")
            tree.heading("Name", text="نام")
            tree.heading("Inventory", text="موجودی")
            for p in products:
                tree.insert("", "end", values=(p.id, p.name, p.inventory))
            tree.pack(expand=True, fill="both")

    def generate_report(self):
        start_date = simpledialog.askstring("ورودی", "تاریخ شروع (YYYY-MM-DD):")
        end_date = simpledialog.askstring("ورودی", "تاریخ پایان (YYYY-MM-DD):")
        if start_date and end_date:
            try:
                results, total_qty, total_rev = self.manager.generate_sales_report(start_date, end_date)
                report_win = tk.Toplevel(self.root)
                report_win.title("گزارش فروش")
                text = tk.Text(report_win, height=15, width=50)
                for row in results:
                    text.insert("end", f"شناسه: {row[0]}, نام: {row[1]}, تعداد: {row[2]}, درآمد: {row[3]}\n")
                text.insert("end", f"\nمجموع تعداد: {total_qty}\nمجموع درآمد: {total_rev}")
                text.pack()
            except ValueError as e:
                messagebox.showerror("خطا", str(e))

# Main execution
if __name__ == "__main__":
    manager = ShopManager()
    print("برای رابط متنی عدد 1 و برای رابط گرافیکی عدد 2 را وارد کنید:")
    ui_choice = input("انتخاب شما: ")
    if ui_choice == '1':
        text_ui(manager)
    elif ui_choice == '2':
        root = tk.Tk()
        app = ShopApp(root, manager)
        root.mainloop()
    else:
        print("گزینه نامعتبر! برنامه بسته می‌شود.")