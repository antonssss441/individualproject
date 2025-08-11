import json
import os


FILENAME = "shopping_list.json"


def load_list():
    if os.path.exists(FILENAME):
        try:
            with open (FILENAME, 'r', encoding='utf-8') as f:
                print("файл успешно загружен")
                return json.load(f)
        except FileExistsError:
            print("не получилось загрузить файл, поэтому создаем пустой список")
            return []
    else:
        print("Файл не найден. Создаем пустой список")
        return []


def save_list(shopping_list):
    try:
        with open(FILENAME, 'w', encoding='utf-8') as file:
            json.dump(shopping_list, file, ensure_ascii=False, indent=4)
    except Exception as error:
        print("ошибка при сохранении файла")


def show_list(shopping_list):
    if not shopping_list:
        print("список пуст")
        return False
    else:
        print("список покупок:")
        for number, item in enumerate(shopping_list, start=1):
            print(f"{number}. {item['name']} (x{item['quantity']})")
        return True
    

def add_item(shopping_list):
    name = input("Введите название товара: ")
    if not name:
        print("ошибка в названии товара")
        return
    while True:
        try:
            quantity = int(input("Введите количество: "))
            if quantity <= 0:
                print("Количество товаров должно быть больше нуля")
                continue
            break
        except ValueError:
            print('это не целое число')
    shopping_list.append({"name": name, "quantity": quantity})
    print(f"товар {name} в количестве {quantity} штук добавлен в ваш список")
  

def remove_item(shopping_list):
    if not shopping_list:
        print("список пуст")
        return False
    else:
        print("список покупок:")
        for number, item in enumerate(shopping_list, start=1):
            print(f"{number}. {item['name']} (x{item['quantity']})")
        try:
            index = int(input("Введите номер товара для удаления: ")) - 1
            if index <= -1 or index >= len(shopping_list):
                print("неккоректный номер")
                return False
            else:
                remove = shopping_list.pop(index)
                print(f"товар {remove["name"]} удален")
                return True
        except ValueError:
            print("номер товара должен быть целым числом")
            return False


def edit_item(shopping_list):
    if not shopping_list:
        print("список пуст")
    else:
        print("список покупок:")
        for number, item in enumerate(shopping_list, start=1):
            print(f"{number}. {item['name']} (x{item['quantity']})")
        try:
            index = int(input("Введите номер товара для редактирования: ")) - 1
            if index <= -1 or index >= len(shopping_list):
                print("неккоректный номер")
            else:
                print(f"Название товара: {item['name']}")
                print(f"Количество товара: {item['quantity']}")
                new_name = input("Введите новое название (или нажмите Enter, чтобы оставить старое): ")
                new_quantity = input("Введите новое количество (или нажмите Enter, чтобы оставить старое): ")
                if new_name:
                    item['name'] = new_name
                if new_quantity:
                    try:
                        if int(new_quantity) > 0:
                            item['quantity'] = int(new_quantity)
                        else:
                            print("Некорректное количество, оставлено старое значение.")
                    except ValueError:
                        print("Некорректное количество, оставлено старое значение.")
        except ValueError:
            print("номер товара должен быть целым числом")
            return False


def main():
    shopping_list = load_list()
    while True:
        menu = int(input("""Меню:
        1. сохранить список
        2. просмотр списка
        3. добавить товар
        4. удалить товар
        5. редактировать товар
        6. Выход
"""))
        if menu == 1:
            save_list(shopping_list)
        elif menu == 2:
            show_list(shopping_list)
        elif menu == 3:
            add_item(shopping_list)
        elif menu == 4:
            remove_item(shopping_list)
        elif menu == 5:
            edit_item(shopping_list)
        else:
            break
        

if __name__ == "__main__":
    main()