import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox


class CreditSystemApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Кредитный Помощник")
        self.root.geometry("900x700")
        self.root.configure(background='#2c3e50')

        self.create_database()
        self.create_main_screen()

    def create_database(self):
        conn = sqlite3.connect('credit_system.db')
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            email TEXT,
            phone TEXT
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            full_name TEXT NOT NULL,
            credit_sum REAL NOT NULL,
            credit_term INTEGER NOT NULL,
            status TEXT DEFAULT 'На рассмотрении',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES clients(id)
        )
        ''')

        # Добавляем примерные данные клиентов
        clients = [
            ("client1", "password1", "Иван Иванов", "ivan@example.com", "1234567890"),
            ("client2", "password2", "Петр Петров", "petr@example.com", "0987654321"),
            ("client3", "password3", "Ольга Сидорова", "olga@example.com", "5551234567"),
            ("client4", "password4", "Алексей Алексеев", "alexey@example.com", "6660987654"),
            ("client5", "password5", "Елена Егорова", "elena@example.com", "7775551234"),
            ("client6", "password6", "Анастасия Смирнова", "anastasia@example.com", "8881234567"),
            ("client7", "password7", "Дмитрий Кузнецов", "dmitry@example.com", "9997654321"),
        ]

        cursor.executemany(
            "INSERT OR IGNORE INTO clients (username, password, full_name, email, phone) VALUES (?, ?, ?, ?, ?)",
            clients
        )

        # Добавляем примерные заявки
        applications = [
            (1, "Иван Иванов", 100000, 12, "На рассмотрении"),
            (2, "Петр Петров", 50000, 6, "На рассмотрении"),
            (3, "Ольга Сидорова", 150000, 24, "Одобрено"),
            (4, "Алексей Алексеев", 200000, 36, "Не одобрено"),
            (5, "Елена Егорова", 250000, 18, "На рассмотрении"),
            (6, "Анастасия Смирнова", 300000, 24, "На рассмотрении"),
            (7, "Дмитрий Кузнецов", 120000, 12, "Не одобрено"),
        ]

        cursor.executemany(
            "INSERT INTO applications (client_id, full_name, credit_sum, credit_term, status) VALUES (?, ?, ?, ?, ?)",
            applications
        )

        conn.commit()
        conn.close()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_main_screen(self):
        self.clear_screen()

        container = tk.Frame(self.root, bg='#2c3e50', padx=30, pady=30)
        container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        title_label = tk.Label(
            container,
            text="Кредитный Помощник",
            font=("Helvetica", 28, "bold"),
            bg='#2c3e50',
            fg='white'
        )
        title_label.pack(pady=(0, 30))

        button_style = {
            "width": 35,
            "padx": 10,
            "pady": 5,
        }

        client_button = tk.Button(
            container,
            text="Вход для клиента",
            command=self.show_client_login,
            **button_style,
            bg='blue',
            fg='white'
        )
        client_button.pack(pady=10)

        admin_button = tk.Button(
            container,
            text="Вход для администратора",
            command=self.show_admin_login,
            **button_style,
            bg='red',
            fg='white'
        )
        admin_button.pack(pady=10)

        register_button = tk.Button(
            container,
            text="Регистрация",
            command=self.show_registration,
            **button_style,
            bg='green',
            fg='white'
        )
        register_button.pack(pady=10)

    def show_client_login(self):
        self.clear_screen()

        container = tk.Frame(self.root, bg='#2c3e50', padx=30, pady=30)
        container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        title = tk.Label(container, text="Вход для клиента", font=("Helvetica", 24, "bold"), bg='#2c3e50', fg='white')
        title.pack(pady=20)

        username_label = tk.Label(container, text="Логин:", bg='#2c3e50', fg='white')
        username_label.pack()
        username_entry = tk.Entry(container, width=40)
        username_entry.pack(pady=5)

        password_label = tk.Label(container, text="Пароль:", bg='#2c3e50', fg='white')
        password_label.pack()
        password_entry = tk.Entry(container, show="*", width=40)
        password_entry.pack(pady=5)

        button_frame = tk.Frame(container, bg='#2c3e50')
        button_frame.pack(pady=20)

        login_button = tk.Button(
            button_frame,
            text="Войти",
            command=lambda: self.client_login(username_entry.get(), password_entry.get()),
            width=15,
            padx=5,
            pady=5,
            font=("Helvetica", 10),
            bg='blue',
            fg='white'
        )
        login_button.pack(side=tk.LEFT, padx=10)

        back_button = tk.Button(
            button_frame,
            text="Назад",
            command=self.create_main_screen,
            width=15,
            padx=5,
            pady=5,
            font=("Helvetica", 10),
            bg='grey',
            fg='white'
        )
        back_button.pack(side=tk.LEFT)

    def client_login(self, username, password):
        conn = sqlite3.connect('credit_system.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients WHERE username = ? AND password = ?", (username, password))
        client = cursor.fetchone()
        conn.close()

        if client:
            self.show_client_dashboard(client)
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль")

    def show_client_dashboard(self, client):
        self.clear_screen()

        welcome_label = tk.Label(
            self.root,
            text=f"Добро пожаловать, {client[3]}!",
            font=("Helvetica", 24, "bold"),
            bg='#2c3e50',
            fg='white'
        )
        welcome_label.pack(pady=20)

        dashboard_frame = tk.Frame(self.root, bg='#2c3e50')
        dashboard_frame.pack(expand=True)

        new_application_button = tk.Button(
            dashboard_frame,
            text="Новая заявка на кредит",
            command=lambda: self.show_credit_application(client),
            width=30,
            padx=10,
            pady=5,
            font=("Helvetica", 12),
            bg='green',
            fg='white'
        )
        new_application_button.pack(pady=(10, 5))

        view_applications_button = tk.Button(
            dashboard_frame,
            text="Мои заявки",
            command=lambda: self.show_client_applications(client),
            width=30,
            padx=10,
            pady=5,
            font=("Helvetica", 12),
            bg='blue',
            fg='white'
        )
        view_applications_button.pack(pady=(5, 5))

        logout_button = tk.Button(
            dashboard_frame,
            text="Выйти",
            command=self.create_main_screen,
            width=30,
            padx=10,
            pady=5,
            font=("Helvetica", 12),
            bg='red',
            fg='white'
        )
        logout_button.pack(pady=(5, 10))

    def show_credit_application(self, client):
        self.clear_screen()

        title = tk.Label(
            self.root,
            text="Новая кредитная заявка",
            font=("Helvetica", 24, "bold"),
            bg='#2c3e50',
            fg='white'
        )
        title.pack(pady=20)

        form_frame = tk.Frame(self.root, bg='#2c3e50')
        form_frame.pack(expand=True)

        fields = [
            ("Сумма кредита", "credit_sum"),
            ("Срок кредита (месяцев)", "credit_term")
        ]

        entries = {}
        for label_text, entry_name in fields:
            label = tk.Label(form_frame, text=label_text, bg='#2c3e50', fg='white')
            label.pack()
            entry = tk.Entry(form_frame, width=30)
            entry.pack(pady=5)
            entries[entry_name] = entry

        button_frame = tk.Frame(form_frame, bg='#2c3e50')
        button_frame.pack(pady=10)

        submit_button = tk.Button(
            button_frame,
            text="Отправить заявку",
            command=lambda: self.submit_credit_application(client, entries),
            width=15,
            padx=5,
            pady=5,
            font=("Helvetica", 10),
            bg='green',
            fg='white'
        )
        submit_button.pack(side=tk.LEFT, padx=5)

        back_button = tk.Button(
            button_frame,
            text="Назад",
            command=lambda: self.show_client_dashboard(client),
            width=15,
            padx=5,
            pady=5,
            font=("Helvetica", 10),
            bg='grey',
            fg='white'
        )
        back_button.pack(side=tk.LEFT, padx=5)

    def submit_credit_application(self, client, entries):
        try:
            credit_sum = float(entries['credit_sum'].get())
            credit_term = int(entries['credit_term'].get())

            conn = sqlite3.connect('credit_system.db')
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO applications 
                (client_id, full_name, credit_sum, credit_term) 
                VALUES (?, ?, ?, ?)
            ''', (client[0], client[3], credit_sum, credit_term))

            conn.commit()
            conn.close()

            messagebox.showinfo("Успех", "Заявка успешно отправлена!")
            self.show_client_dashboard(client)

        except ValueError:
            messagebox.showerror("Ошибка", "Некорректный ввод данных")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def show_admin_login(self):
        self.clear_screen()

        container = tk.Frame(self.root, bg='#2c3e50', padx=30, pady=30)
        container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        title = tk.Label(
            container,
            text="Вход Администратора",
            font=("Helvetica", 24, "bold"),
            bg='#2c3e50',
            fg='white'
        )
        title.pack(pady=20)

        username_label = tk.Label(container, text="Логин:", bg='#2c3e50', fg='white')
        username_label.pack()
        username_entry = tk.Entry(container, width=40)
        username_entry.pack(pady=5)

        password_label = tk.Label(container, text="Пароль:", bg='#2c3e50', fg='white')
        password_label.pack()
        password_entry = tk.Entry(container, show="*", width=40)
        password_entry.pack(pady=5)

        button_frame = tk.Frame(container, bg='#2c3e50')
        button_frame.pack(pady=20)

        login_button = tk.Button(
            button_frame,
            text="Войти",
            command=lambda: self.admin_login(username_entry.get(), password_entry.get()),
            width=15,
            padx=5,
            pady=5,
            font=("Helvetica", 10),
            bg='red',
            fg='white'
        )
        login_button.pack(side=tk.LEFT, padx=10)

        back_button = tk.Button(
            button_frame,
            text="Назад",
            command=self.create_main_screen,
            width=15,
            padx=5,
            pady=5,
            font=("Helvetica", 10),
            bg='grey',
            fg='white'
        )
        back_button.pack(side=tk.LEFT)

    def admin_login(self, username, password):
        if username == "admin" and password == "CreditAdmin2023!":
            messagebox.showinfo("Успех", "Вы вошли как администратор.")
            self.show_admin_dashboard()
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль")

    def show_admin_dashboard(self):
        self.clear_screen()

        title = tk.Label(
            self.root,
            text="Панель Администратора",
            font=("Helvetica", 24, "bold"),
            bg='#2c3e50',
            fg='white'
        )
        title.pack(pady=20)

        dashboard_frame = tk.Frame(self.root, bg='#2c3e50')
        dashboard_frame.pack(expand=True)

        search_label = tk.Label(dashboard_frame, text="Поиск по ФИО:", bg='#2c3e50', fg='white')
        search_label.pack(pady=(10, 5))

        search_entry = tk.Entry(dashboard_frame, width=50)
        search_entry.pack(pady=5)

        search_button = tk.Button(
            dashboard_frame,
            text="Поиск",
            command=lambda: self.search_applications(search_entry.get()),
            width=15,
            padx=5,
            pady=5,
            font=("Helvetica", 10),
            bg='blue',
            fg='white'
        )
        search_button.pack(pady=(5, 10))

        view_applications_button = tk.Button(
            dashboard_frame,
            text="Просмотр всех заявок",
            command=self.view_all_applications,
            width=30,
            padx=10,
            pady=5,
            font=("Helvetica", 12),
            bg='blue',
            fg='white'
        )
        view_applications_button.pack(pady=(10, 5))

        logout_button = tk.Button(
            dashboard_frame,
            text="Выйти",
            command=self.create_main_screen,
            width=30,
            padx=10,
            pady=5,
            font=("Helvetica", 12),
            bg='red',
            fg='white'
        )
        logout_button.pack(pady=(5, 10))

    def view_all_applications(self):
        conn = sqlite3.connect('credit_system.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM applications")
        applications = cursor.fetchall()
        conn.close()

        if applications:
            applications_window = tk.Toplevel(self.root)
            applications_window.title("Все заявки")
            applications_window.geometry("800x400")

            frame = tk.Frame(applications_window)
            frame.pack(fill=tk.BOTH, expand=True)

            scrollbar = tk.Scrollbar(frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            tree = ttk.Treeview(frame, columns=("ID", "ФИО", "Сумма кредита", "Срок кредита", "Статус"),
                                show="headings", yscrollcommand=scrollbar.set)
            scrollbar.config(command=tree.yview)

            tree.heading("ID", text="ID")
            tree.heading("ФИО", text="ФИО")
            tree.heading("Сумма кредита", text="Сумма кредита")
            tree.heading("Срок кредита", text="Срок кредита")
            tree.heading("Статус", text="Статус")

            for app in applications:
                tree.insert("", tk.END, values=app[1:])

            tree.pack(expand=True, fill=tk.BOTH)

            button_frame = tk.Frame(applications_window)
            button_frame.pack(pady=10)

            status_label = tk.Label(button_frame, text="Статус:", bg='white')
            status_label.pack(side=tk.LEFT, padx=(0, 5))

            status_var = tk.StringVar(value='На рассмотрении')
            status_options = ['На рассмотрении', 'Одобрено', 'Не одобрено']
            status_menu = ttk.Combobox(button_frame, textvariable=status_var, values=status_options, state='readonly')
            status_menu.pack(side=tk.LEFT, padx=(0, 5))

            update_button = tk.Button(
                button_frame,
                text="Изменить статус",
                command=lambda: self.update_status(tree, status_var.get()),
                bg='yellow',
                fg='black'
            )
            update_button.pack(side=tk.LEFT)

            back_button = tk.Button(
                button_frame,
                text="Назад",
                command=applications_window.destroy,
                bg='grey',
                fg='white'
            )
            back_button.pack(side=tk.LEFT, padx=(5, 0))

        else:
            messagebox.showinfo("Информация", "Нет заявок для отображения.")

    def update_status(self, tree, new_status):
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Предупреждение", "Пожалуйста, выберите заявку.")
            return

        item_id = tree.item(selected_item, 'values')[0]  # Получаем ID заявки
        conn = sqlite3.connect('credit_system.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE applications SET status = ? WHERE id = ?", (new_status, item_id))
        conn.commit()
        conn.close()

        messagebox.showinfo("Успех", "Статус заявки изменен!")
        self.view_all_applications()

    def search_applications(self, query):
        conn = sqlite3.connect('credit_system.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM applications WHERE full_name LIKE ?", ('%' + query + '%',))
        applications = cursor.fetchall()
        conn.close()

        if applications:
            applications_window = tk.Toplevel(self.root)
            applications_window.title("Результаты поиска")
            applications_window.geometry("800x400")

            frame = tk.Frame(applications_window)
            frame.pack(fill=tk.BOTH, expand=True)

            scrollbar = tk.Scrollbar(frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            tree = ttk.Treeview(frame, columns=("ID", "ФИО", "Сумма кредита", "Срок кредита", "Статус"),
                                show="headings", yscrollcommand=scrollbar.set)
            scrollbar.config(command=tree.yview)

            tree.heading("ID", text="ID")
            tree.heading("ФИО", text="ФИО")
            tree.heading("Сумма кредита", text="Сумма кредита")
            tree.heading("Срок кредита", text="Срок кредита")
            tree.heading("Статус", text="Статус")

            for app in applications:
                tree.insert("", tk.END, values=app[1:])

            tree.pack(expand=True, fill=tk.BOTH)

            button_frame = tk.Frame(applications_window)
            button_frame.pack(pady=10)

            back_button = tk.Button(
                button_frame,
                text="Назад",
                command=applications_window.destroy,
                bg='grey',
                fg='white'
            )
            back_button.pack(side=tk.LEFT)

        else:
            messagebox.showinfo("Информация", "Не найдено заявок по вашему запросу.")

    def show_registration(self):
        self.clear_screen()

        container = tk.Frame(self.root, bg='#2c3e50', padx=30, pady=30)
        container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        title = tk.Label(
            container,
            text="Регистрация",
            font=("Helvetica", 24, "bold"),
            bg='#2c3e50',
            fg='white'
        )
        title.pack(pady=20)

        registration_frame = tk.Frame(container, bg='#2c3e50')
        registration_frame.pack(expand=True)

        username_label = tk.Label(registration_frame, text="Логин:", bg='#2c3e50', fg='white')
        username_label.pack()
        username_entry = tk.Entry(registration_frame, width=30)
        username_entry.pack(pady=5)

        password_label = tk.Label(registration_frame, text="Пароль:", bg='#2c3e50', fg='white')
        password_label.pack()
        password_entry = tk.Entry(registration_frame, show="*", width=30)
        password_entry.pack(pady=5)

        full_name_label = tk.Label(registration_frame, text="ФИО:", bg='#2c3e50', fg='white')
        full_name_label.pack()
        full_name_entry = tk.Entry(registration_frame, width=30)
        full_name_entry.pack(pady=5)

        email_label = tk.Label(registration_frame, text="Email:", bg='#2c3e50', fg='white')
        email_label.pack()
        email_entry = tk.Entry(registration_frame, width=30)
        email_entry.pack(pady=5)

        phone_label = tk.Label(registration_frame, text="Телефон:", bg='#2c3e50', fg='white')
        phone_label.pack()
        phone_entry = tk.Entry(registration_frame, width=30)
        phone_entry.pack(pady=5)

        button_frame = tk.Frame(registration_frame, bg='#2c3e50')
        button_frame.pack(pady=10)

        register_button = tk.Button(
            button_frame,
            text="Зарегистрироваться",
            command=lambda: self.register_client(username_entry.get(), password_entry.get(),
                                                 full_name_entry.get(), email_entry.get(),
                                                 phone_entry.get()),
            width=15,
            padx=5,
            pady=5,
            font=("Helvetica", 10),
            bg='green',
            fg='white'
        )
        register_button.pack(side=tk.LEFT, padx=5)

        back_button = tk.Button(
            button_frame,
            text="Назад",
            command=self.create_main_screen,
            width=15,
            padx=5,
            pady=5,
            font=("Helvetica", 10),
            bg='grey',
            fg='white'
        )
        back_button.pack(side=tk.LEFT, padx=5)

    def register_client(self, username, password, full_name, email, phone):
        conn = sqlite3.connect('credit_system.db')
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO clients (username, password, full_name, email, phone) VALUES (?, ?, ?, ?, ?)",
                           (username, password, full_name, email, phone))
            conn.commit()
            messagebox.showinfo("Успех", "Регистрация прошла успешно!")
            self.create_main_screen()
        except sqlite3.IntegrityError:
            messagebox.showerror("Ошибка", "Логин уже занят. Пожалуйста, выберите другой логин.")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
        finally:
            conn.close()

    def show_client_applications(self, client):
        self.clear_screen()

        conn = sqlite3.connect('credit_system.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM applications WHERE client_id = ?", (client[0],))
        applications = cursor.fetchall()
        conn.close()

        if applications:
            frame = tk.Frame(self.root, bg='#2c3e50')
            frame.pack(fill=tk.BOTH, expand=True)

            scrollbar = tk.Scrollbar(frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            tree = ttk.Treeview(frame, columns=("ID", "ФИО", "Сумма кредита", "Срок кредита", "Статус"),
                                show="headings", yscrollcommand=scrollbar.set)
            scrollbar.config(command=tree.yview)

            tree.heading("ID", text="ID")
            tree.heading("ФИО", text="ФИО")
            tree.heading("Сумма кредита", text="Сумма кредита")
            tree.heading("Срок кредита", text="Срок кредита")
            tree.heading("Статус", text="Статус")
            for app in applications:
                tree.insert("", tk.END, values=app[1:])
            tree.pack(expand=True, fill=tk.BOTH)

            button_frame = tk.Frame(self.root, bg='#2c3e50')
            button_frame.pack(pady=10)

            back_button = tk.Button(
                button_frame,
                text="Назад",
                command=lambda: self.show_client_dashboard(client),
                width=15,
                padx=5,
                pady=5,
                font=("Helvetica", 10),
                bg='grey',
                fg='white'
            )
            back_button.pack(side=tk.LEFT)

        else:
            messagebox.showinfo("Информация", "У вас нет заявок.")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = CreditSystemApp()
    app.run()