import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog


FILENAME = "shopping_list.json"


def load_list():
    if os.path.exists(FILENAME):
        try:
            with open (FILENAME, 'r', encoding='utf-8') as f:
                messagebox.showinfo("Загрузка","файл успешно загружен")
                return json.load(f)
        except FileExistsError:
            messagebox.showerror("ошибка!", "не получилось загрузить файл, поэтому создаем пустой список")
            return []
    else:
        messagebox.showinfo("Загрузка", "Файл не найден. Создаем пустой список")
        return []


def save_list(shopping_list):
    try:
        with open(FILENAME, 'w', encoding='utf-8') as file:
            json.dump(shopping_list, file, ensure_ascii=False, indent=4)
        messagebox.showinfo("успех!", "Список успешно сохранен")
    except Exception as error:
        messagebox.showerror("ошибка!", "ошибка при сохранении файла")


def show_list(shopping_list):
    if not shopping_list:
        messagebox.showinfo("Пустой список", "Список покупок пуст.")
        return False
    window = tk.Toplevel()
    window.title("Список покупок")
    label = tk.Label(window, text="Список покупок:")
    label.pack(pady=5)
    listbox = tk.Listbox(window, width=50)
    listbox.pack(padx=10, pady=5)
    for number, item in enumerate(shopping_list, start=1):
        listbox.insert(tk.END, f"{number}. {item['name']} (x{item['quantity']})")
    return True


def add_item(shopping_list):
    name = simpledialog.askstring("Добавить товар", "Введите название товара:")
    if not name:
        messagebox.showerror("Ошибка!", "Название товара не может быть пустым.")
        return
    while True:
        quantity_str = simpledialog.askstring("Количество", "Введите количество товара:")
        if quantity_str is None:
            return False
        try:
            quantity = int(quantity_str)
            if quantity <= 0:
                messagebox.showerror("Ошибка", "Количество должно быть больше нуля.")
                continue
            break
        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста, введите целое число.")
    shopping_list.append({"name": name, "quantity": quantity})
    messagebox.showinfo("Успех", f"Товар {name} в количестве {quantity} штук добавлен в список.")
  

def remove_item(shopping_list):
    if not shopping_list:
        messagebox.showinfo("Пустой список", "Список покупок пуст.")
        return False
    remove_window = tk.Toplevel()
    remove_window.title("Удалить товар")
    listbox = tk.Listbox(remove_window, width=50, height=10)
    for item in shopping_list:
        listbox.insert(tk.END, f"{item['name']} (x{item['quantity']})")
    listbox.pack(padx=10, pady=10)

    def delete_selected():
        selected_indices = listbox.curselection()
        if not selected_indices:
            messagebox.showerror("Ошибка!", "Пожалуйста, выберите товар для удаления.")
            return
        index = selected_indices[0]
        removed_item = shopping_list.pop(index)
        messagebox.showinfo("Удалено", f"Товар '{removed_item['name']}' удален.")
        remove_window.destroy()

    btn_delete = tk.Button(remove_window, text="Удалить выбранное", command=delete_selected)
    btn_delete.pack(pady=5)


def edit_item(shopping_list):
    if not shopping_list:
        messagebox.showinfo("Пустой список", "Список покупок пуст.")
        return
    edit_window = tk.Toplevel()
    edit_window.title("Редактировать товар")
    listbox = tk.Listbox(edit_window, width=50, height=10)
    for item in shopping_list:
        listbox.insert(tk.END, f"{item['name']} (x{item['quantity']})")
    listbox.pack(padx=10, pady=10)

    def edit_selected():
        selected_indices = listbox.curselection()
        if not selected_indices:
            messagebox.showerror("Ошибка!", "Пожалуйста, выберите товар для редактирования.")
            return
        index = selected_indices[0]
        item = shopping_list[index]
        new_name = simpledialog.askstring("Редактировать название", "Введите новое название товара:", initialvalue=item['name'])
        if new_name:
            item['name'] = new_name
        new_quantity_str = simpledialog.askstring("Редактировать количество", "Введите новое количество товара:", initialvalue=str(item['quantity']))
        if new_quantity_str:
            try:
                new_quantity = int(new_quantity_str)
                if new_quantity > 0:
                    item['quantity'] = new_quantity
                else:
                    messagebox.showerror("Ошибка!", "Количество должно быть положительным числом. Оставлено старое значение.")
            except ValueError:
                messagebox.showerror("Ошибка!", "Некорректное число. Количество оставлено без изменений.")
        listbox.delete(0, tk.END)
        for itm in shopping_list:
            listbox.insert(tk.END, f"{itm['name']} (x{itm['quantity']})")
        messagebox.showinfo("Успех!", "Товар успешно отредактирован.")

    btn_edit = tk.Button(edit_window, text="Редактировать выбранное", command=edit_selected)
    btn_edit.pack(pady=5)


def main():
    shopping_list = load_list()

    def save():
        save_list(shopping_list)

    def view():
        show_list(shopping_list)

    def add():
        add_item(shopping_list)

    def remove():
        remove_item(shopping_list)

    def edit():
        edit_item(shopping_list)

    root = tk.Tk()
    root.title("Меню покупок")

    btn_save = tk.Button(root, text="Сохранить список", command=save)
    btn_view = tk.Button(root, text="Просмотр списка", command=view)
    btn_add = tk.Button(root, text="Добавить товар", command=add)
    btn_remove = tk.Button(root, text="Удалить товар", command=remove)
    btn_edit = tk.Button(root, text="Редактировать товар", command=edit)
    btn_exit = tk.Button(root, text="Выход", command=root.quit)

    btn_save.pack(fill='x')
    btn_view.pack(fill='x')
    btn_add.pack(fill='x')
    btn_remove.pack(fill='x')
    btn_edit.pack(fill='x')
    btn_exit.pack(fill='x')

    root.mainloop()

if __name__ == "__main__":
    main()