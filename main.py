import re
import csv
import os
import logging

def logger(path):
    def __logger(old_function):
        # Создаем уникальный логгер для каждой функции
        logger = logging.getLogger(f"{old_function.__name__}_{path}")
        logger.setLevel(logging.INFO)

        # Создаем обработчик для записи логов в файл
        handler = logging.FileHandler(path, encoding='utf-8')
        handler.setLevel(logging.INFO)

        # Настраиваем форматирование
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        handler.setFormatter(formatter)

        # Добавляем обработчик к логгеру
        if not logger.handlers:
            logger.addHandler(handler)

        def new_function(*args, **kwargs):
            # Логируем имя функции и аргументы
            func_name = old_function.__name__
            logger.info(f"Функция '{func_name}' вызвана с args: {args} и kwargs: {kwargs}")

            # Вызываем оригинальную функцию и получаем результат
            result = old_function(*args, **kwargs)

            # Логируем результат
            logger.info(f"Функция '{func_name}' вернула: {result}")

            return result

        return new_function

    return __logger

@logger('log.log')
def process_contacts(contacts_list):
    phone_pattern = re.compile(
        r'(\+7|8)\s*\(*(\d{3})\)*\s*\-*(\d{3})\s*\-*(\d{2})\s*\-*(\d{2})')
    extension_pattern = re.compile(r'\s*\(*(доб.)\s*(\d+)\)*\s*')

    contacts_dict = {}
    for contact in contacts_list[1:]:
        # Объединяем ФИО в одно поле, чтобы потом разделить корректно
        full_name = ' '.join(contact[:3]).split()
        last_name, first_name, *surname = (full_name + [""])[:3]
        key = (last_name, first_name)

        # Форматируем номер телефона
        phone = contact[5]
        if phone:
            phone = phone_pattern.sub(r'+7(\2)\3-\4-\5', phone)
            phone = extension_pattern.sub(r' \1\2', phone)

        # Объединяем записи с одинаковыми именами и фамилиями
        if key not in contacts_dict:
            contacts_dict[key] = [last_name, first_name, surname[0], contact[3], contact[4], phone, contact[6]]
        else:
            for i in range(3, 7):
                if not contacts_dict[key][i]:
                    contacts_dict[key][i] = contact[i]

    return [contacts_list[0]] + list(contacts_dict.values())

@logger('log2.log')
def save_to_csv(file_name, contacts):
    with open(file_name, "w", newline='', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerows(contacts)


if __name__ == "__main__":
    with open("phonebook_raw.csv", encoding='utf8') as f:
        reader = csv.reader(f)
        contacts_list = list(reader)

    final_contacts = process_contacts(contacts_list)
    save_to_csv("phonebook.csv", final_contacts)