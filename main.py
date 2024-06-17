import csv
import tkinter as tk
from tkinter import ttk
import os
from tkinter import simpledialog, messagebox


class PhonebookApp:
    def __init__(self, root):
        self.root = root
        root.geometry('580x450')
        self.root.title("Телефонная книга alpha ver. 0.01")

        icon = tk.PhotoImage(file='icon.png')
        root.iconphoto(True, icon)

        self.contacts = self.read_csv("result.csv")
        self.sort_contacts()

        # Создаем верхнее меню
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        # Создаем кнопку "Инструкция"
        self.menu.add_command(label="Инструкция", command=self.open_instruction_file)

        self.selected_contact_id = None

        self.create_widgets()

        # Настройка стиля Treeview для изменения размера шрифта
        style = ttk.Style()
        style.configure("Treeview", font=("Helvetica", 13))

    def create_widgets(self):
        self.contact_list = ttk.Treeview(self.root, columns=("Name/Number",))
        self.contact_list.heading("#0", text="")
        self.contact_list.heading("Name/Number", text="Имя/Номер телефона")

        self.contact_list.column("#0", stretch=tk.NO, minwidth=0, width=0)
        self.contact_list.column("Name/Number", stretch=tk.YES, minwidth=100, width=285)

        self.contact_list.bind("<Double-1>", self.update_contact_info)
        self.contact_list.grid(row=0, column=0, padx=10, pady=10, sticky=tk.NSEW)

        # Добавляем ползунок прокрутки
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.contact_list.yview)
        # scrollbar.grid(row=0, column=1, sticky='nse')
        scrollbar.place(x=300, y=5, height=250)

        self.contact_list.configure(yscrollcommand=scrollbar.set)

        self.load_contacts()

        search_label = tk.Label(self.root, text="Поиск:")
        search_label.grid(row=1, column=0, padx=10, pady=(0, 5), sticky=tk.W)

        self.search_entry = tk.Entry(self.root)
        self.search_entry.grid(row=1, column=0, padx=(50, 10), pady=(0, 5), sticky=tk.EW)
        self.search_entry.bind("<KeyRelease>", self.search_contacts)

        call_button = tk.Button(self.root, text="Позвонить", command=self.call_contact)
        call_button.grid(row=2, column=0, padx=10, pady=5, sticky=tk.EW)

        edit_button = tk.Button(self.root, text="Редактировать", command=self.edit_contact)
        edit_button.grid(row=3, column=0, padx=10, pady=5, sticky=tk.EW)

        new_button = tk.Button(self.root, text="Создать новый", command=self.create_contact)
        new_button.grid(row=4, column=0, padx=10, pady=5, sticky=tk.EW)

        delete_button = tk.Button(self.root, text="Удалить", command=self.delete_contact)
        delete_button.grid(row=5, column=0, padx=10, pady=5, sticky=tk.EW)

        # Добавляем текстовые поля для отображения имени, номера телефона, пола, даты рождения и комментария
        self.name_label = tk.Label(self.root, text="Имя:")
        self.name_label.place(x=335, y=10, width=40, height=10)
        self.name_label.config(padx=10, pady=5)

        self.name_entry = tk.Text(self.root, wrap="word", height=3)
        self.name_entry.configure(state="disabled")
        self.name_entry.place(x=375, y=10, width=200, height=50)

        self.phone_label = tk.Label(self.root, text="Телефон:")
        self.phone_label.place(x=315, y=70, width=50, height=10)
        self.phone_label.config(padx=10, pady=5)

        self.phone_entry = tk.Text(self.root, wrap="word", height=3)
        self.phone_entry.configure(state="disabled")
        self.phone_entry.place(x=375, y=70, width=200, height=20)

        self.gender_label = tk.Label(self.root, text="Пол:")
        self.gender_label.place(x=325, y=110, width=50, height=10)

        self.gender_entry = tk.Entry(self.root, state="readonly")
        self.gender_entry.place(x=375, y=110, width=200, height=20)

        self.dob_label = tk.Label(self.root, text="Дата\nрождения:")
        self.dob_label.place(x=310, y=135, width=57, height=27)

        self.dob_entry = tk.Entry(self.root, state="readonly")
        self.dob_entry.place(x=375, y=140, width=200, height=20)

        self.comment_label = tk.Label(self.root, text="Комментарий:")
        self.comment_label.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)

        self.comment_entry = tk.Text(self.root, state="disabled", wrap="word")
        self.comment_entry.place(x=320, y=310, width=250, height=100)
        self.comment_entry.config(padx=10, pady=5)

    def open_instruction_file(self):
        # Открываем текстовый файл инструкции
        os.startfile("instruction.txt", 'open')

    def read_csv(self, filename):
        contacts = []
        with open(filename, "r", encoding="windows-1251") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                contact = {
                    'id': row['id'],
                    'names': row['names'],
                    'phone_number': row['phone_number'],
                    'sex': row['sex'],
                    'dob': row['dob'],
                    'comments': row['comments']
                }
                contacts.append(contact)
        return contacts

    def load_contacts(self):
        self.contact_list.delete(*self.contact_list.get_children())
        for contact in self.contacts:
            name_number = f"{contact['names']} ({contact['phone_number']})"
            self.contact_list.insert("", "end", iid=contact['id'], text="", values=(name_number,))

    def update_contact_info(self, event):
        selected_item = self.contact_list.focus()
        if selected_item:
            self.selected_contact_id = selected_item
            filtered_contacts = self.contact_list.get_children()
            selected_contact = next((contact for contact in self.contacts if contact['id'] == self.selected_contact_id),
                                    None)
            if selected_contact:
                self.name_entry.config(state='normal')
                self.name_entry.delete('1.0', tk.END)
                self.name_entry.insert(tk.INSERT, selected_contact['names'])
                self.name_entry.config(state='disabled')

                self.phone_entry.config(state='normal')
                self.phone_entry.delete('1.0', tk.END)  # Используем индексы в формате "line.column" для tk.Text
                self.phone_entry.insert(tk.INSERT, selected_contact['phone_number'])
                self.phone_entry.config(state='disabled')

                self.gender_entry.config(state='normal')
                self.gender_entry.delete(0, tk.END)  # Используем числовые индексы для tk.Entry
                self.gender_entry.insert(0, selected_contact['sex'])
                self.gender_entry.config(state='readonly')

                self.dob_entry.config(state='normal')
                self.dob_entry.delete(0, tk.END)  # Используем числовые индексы для tk.Entry
                self.dob_entry.insert(0, selected_contact['dob'])
                self.dob_entry.config(state='readonly')

                self.comment_entry.config(state='normal')
                self.comment_entry.delete('1.0', tk.END)
                self.comment_entry.insert(tk.END, selected_contact['comments'])
                self.comment_entry.config(state='disabled')
        else:
            self.clear_contact_info()

    def clear_contact_info(self):
        self.name_entry.config(state='normal')
        self.name_entry.delete(0, tk.END)
        self.name_entry.config(state='readonly')

        self.phone_entry.config(state='normal')
        self.phone_entry.delete(0, tk.END)
        self.phone_entry.config(state='readonly')

        self.gender_entry.config(state='normal')
        self.gender_entry.delete(0, tk.END)
        self.gender_entry.config(state='readonly')

        self.dob_entry.config(state='normal')
        self.dob_entry.delete(0, tk.END)
        self.dob_entry.config(state='readonly')

        self.comment_entry.config(state='normal')
        self.comment_entry.delete('1.0', tk.END)
        self.comment_entry.config(state='disabled')

    def get_gender_text(self, gender):
        if gender == "f":
            return "Семья"
        elif gender == "m":
            return "Мужчина"
        elif gender == "w":
            return "Женщина"
        elif gender == "" or len(gender) > 8:
            return "Неизвестно"
        else:
            return gender

    def search_contacts(self, event):
        search_term = self.search_entry.get().lower()
        filtered_contacts = [contact for contact in self.contacts if
                             search_term in contact['names'].lower() or search_term in contact['phone_number'].lower()]
        self.load_filtered_contacts(filtered_contacts)

    def load_filtered_contacts(self, filtered_contacts):
        self.contact_list.delete(*self.contact_list.get_children())
        for contact in filtered_contacts:
            name_number = f"{contact['names']} ({contact['phone_number']})"
            self.contact_list.insert("", "end", iid=contact['id'], text="", values=(name_number,))

    def call_contact(self):
        selected_item = self.contact_list.focus()
        if selected_item:
            selected_contact = next((c for c in self.contacts if c['id'] == selected_item), None)
            if selected_contact:
                phone_number = selected_contact.get("phone_number", "")
                if phone_number:
                    self.root.clipboard_clear()
                    self.root.clipboard_append(phone_number)
                    messagebox.showinfo("Позвонить", f"Номер телефона {phone_number} скопирован в буфер обмена.")
                else:
                    messagebox.showerror("Ошибка", "Для выбранного контакта не указан номер телефона.")
        else:
            messagebox.showerror("Ошибка", "Выберите контакт из списка.")

    def edit_contact(self):
        selected_item = self.contact_list.focus()
        if selected_item:
            self.selected_contact_id = selected_item
            selected_contact = next((c for c in self.contacts if c['id'] == self.selected_contact_id), None)
            if selected_contact:
                dialog = tk.Toplevel(self.root)
                dialog.title("Редактирование контакта")

                tk.Label(dialog, text="Имя:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
                name_entry = tk.Entry(dialog)
                name_entry.insert(0, selected_contact.get("names", ""))
                name_entry.grid(row=0, column=1, padx=10, pady=5, sticky=tk.EW)

                tk.Label(dialog, text="Номер телефона:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
                phone_entry = tk.Entry(dialog)
                phone_entry.insert(0, selected_contact.get("phone_number", ""))
                phone_entry.grid(row=1, column=1, padx=10, pady=5, sticky=tk.EW)

                tk.Label(dialog, text="Дата рождения:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
                dob_entry = tk.Entry(dialog)
                dob_entry.insert(0, selected_contact.get("dob", ""))
                dob_entry.grid(row=2, column=1, padx=10, pady=5, sticky=tk.EW)

                tk.Label(dialog, text="Пол:").grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
                gender_var = tk.StringVar(dialog)
                gender_var.set(selected_contact.get("sex", ""))
                gender_menu = tk.OptionMenu(dialog, gender_var, "Мужской", "Женский")
                gender_menu.grid(row=3, column=1, padx=10, pady=5, sticky=tk.EW)

                tk.Label(dialog, text="Комментарий:").grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
                comment_entry = tk.Text(dialog, wrap="word", height=5)
                comment_entry.insert("1.0", selected_contact.get("comments", ""))
                comment_entry.grid(row=4, column=1, padx=10, pady=5, sticky=tk.EW)

                def save_edited_contact():
                    names = name_entry.get()
                    phone_number = phone_entry.get()
                    dob = dob_entry.get()
                    sex = gender_var.get()
                    comment = comment_entry.get("1.0", tk.END).strip()

                    if names and phone_number:
                        selected_contact["names"] = names
                        selected_contact["phone_number"] = phone_number
                        selected_contact["dob"] = dob
                        selected_contact["sex"] = sex
                        selected_contact["comments"] = comment

                        self.write_csv("result.csv", self.contacts)
                        self.load_contacts()
                        dialog.destroy()
                    else:
                        messagebox.showerror("Ошибка", "Введите имя и номер телефона контакта.")

                tk.Button(dialog, text="Сохранить", command=save_edited_contact).grid(row=5, column=0, columnspan=2,
                                                                                      padx=10, pady=10)

    def write_csv(self, filename, contacts):
        current_dir = os.getcwd()
        file_path = os.path.join(current_dir, filename)
        with open(file_path, "w", newline="", encoding="windows-1251") as csvfile:
            fieldnames = ["id", "names", "phone_number", "dob", "sex", "comments"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=";")
            writer.writeheader()
            for contact in contacts:
                writer.writerow(contact)

    def create_contact(self):
        # Отображаем диалоговое окно для ввода информации о новом контакте
        dialog = tk.Toplevel(self.root)
        dialog.title("Создание нового контакта")

        # Создаем метки и поля для ввода информации
        tk.Label(dialog, text="Имя:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        name_entry = tk.Entry(dialog)
        name_entry.grid(row=0, column=1, padx=10, pady=5, sticky=tk.EW)

        tk.Label(dialog, text="Номер телефона:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        phone_entry = tk.Entry(dialog)
        phone_entry.grid(row=1, column=1, padx=10, pady=5, sticky=tk.EW)

        # Добавляем поля для других данных
        tk.Label(dialog, text="Возраст:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        age_entry = tk.Entry(dialog)
        age_entry.grid(row=2, column=1, padx=10, pady=5, sticky=tk.EW)

        tk.Label(dialog, text="Пол:").grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
        gender_var = tk.StringVar(dialog)
        gender_var.set("Мужской")
        gender_menu = tk.OptionMenu(dialog, gender_var, "Мужской", "Женский", "Семья")
        gender_menu.grid(row=3, column=1, padx=10, pady=5, sticky=tk.EW)

        tk.Label(dialog, text="Комментарий:").grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
        comment_entry = tk.Text(dialog, wrap="word", height=5)
        comment_entry.grid(row=4, column=1, padx=10, pady=5, sticky=tk.EW)

        # Функция для сохранения контакта
        def save_contact():
            name = name_entry.get()
            phone = phone_entry.get()
            age = age_entry.get()
            gender = gender_var.get()
            comment = comment_entry.get("1.0", tk.END).strip()

            # Проверяем, что введены имя и номер телефона
            if name and phone:
                # Добавляем новый контакт в список контактов
                new_contact = {"name": name, "phone_number": phone, "age": age, "sex": gender, "comments": comment}
                self.contacts.append(new_contact)

                # Добавляем новый контакт в файл CSV
                with open("result.csv", "a", newline="", encoding="windows-1251") as csvfile:
                    fieldnames = ["names", "phone_number", "age", "sex", "comments"]
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')

                    # Если файл пустой, записываем заголовки
                    if csvfile.tell() == 0:
                        writer.writeheader()

                    # Записываем данные нового контакта
                    writer.writerow(
                        {"names": name, "phone_number": phone, "age": age, "sex": gender, "comments": comment})

                # Закрываем диалоговое окно
                dialog.destroy()
                # Обновляем список контактов в приложении
                self.load_contacts()
            else:
                # Выводим сообщение об ошибке, если не введены имя или номер телефона
                tk.messagebox.showerror("Ошибка", "Введите имя и номер телефона контакта.")

        # Создаем кнопку для сохранения контакта
        tk.Button(dialog, text="Сохранить", command=save_contact).grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def delete_contact(self):
        item = self.contact_list.selection()[0]
        contact_name = self.contact_list.item(item, "values")[0]
        selected_contact = next((contact for contact in self.contacts if
                                 contact.get("names", "") == contact_name or contact["phone_number"] == contact_name),
                                None)
        if selected_contact:
            print("Deleting contact ID:", selected_contact["id"])
            self.contact_list.delete(item)

    def sort_contacts(self):
        self.contacts.sort(key=lambda x: (x.get("names", ""), x["phone_number"]))


if __name__ == "__main__":
    root = tk.Tk()
    app = PhonebookApp(root)
    root.mainloop()