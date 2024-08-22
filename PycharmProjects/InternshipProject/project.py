import os
# import json
import csv
# import re


class PriceMachine():


# Создадим конструктор класса, список, который будет принимать данные,
# загружаемые из файлов и переменную для хранения макс. длины названий тов-в:

    def __init__(self):
        self.data = []
        self.result = ''
        self.name_length = 0
        self.last_search_results = []


# Создадим метод, который будет загружать данные из всех файлов с прайсами в
#  директории file_path в словарь:
    def load_prices(self, file_path='C:/Users/User/pythonProject6/PycharmProjects/InternshipProject'):
        '''
            Сканирует указанный каталог. Ищет файлы со словом price в названии.
            В файле ищет столбцы с названием товара, ценой и весом.
            Допустимые названия для столбца с товаром:
                товар
                название
                наименование
                продукт

            Допустимые названия для столбца с ценой:
                розница
                цена

            Допустимые названия для столбца с весом (в кг.)
                вес
                масса
                фасовка
        '''
        # Проверим ли не пустой:
        if not file_path:
            raise ValueError("Путь к каталогу не должен быть пустым.")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Каталог не найден: {file_path}")

        files = [f for f in os.listdir(file_path) if 'price' in f.lower()]
        if not files:
            print("Файлы с прайсами не найдены.")
            return
        # здесь список получает все файлы, где встречается слово price в названии.
        # Далее обработаем все найденные файлы (открываем с использованием with, что
        # обеспечит автоматическое закрытие файла после завершения работы с ним):
        for file_name in files:
            with open(os.path.join(file_path, file_name), newline='', encoding='utf-8') as csvfile:
                # прочтем найденные файлы, разделитель укажем, как ;
                reader = csv.reader(csvfile, delimiter=',')
                # считаем первую строку, где названия столбцов, найдем индекс названия продукта,
                # индекс столбца с ценой и весом:
                headers = next(reader)
                product_idx, price_idx, weight_idx = self._search_product_price_weight(headers)
                # Проверим, нашлись ли они, если нашлись, переберем для извлечения данных каждую строку:
                if product_idx is not None and price_idx is not None and weight_idx is not None:
                    for row in reader:
                        # извлечем найденные названия по индексу:
                        try:
                            product = row[product_idx]
                            price = float(row[price_idx])
                            weight = float(row[weight_idx])
                            price_per_kg = price / weight
                            # Добавим в словарь найденные данные:
                            self.data.append({
                                'product': product,
                                'price': price,
                                'weight': weight,
                                'file': file_name,
                                'price_per_kg': price_per_kg
                            })
                        except ValueError as e:
                            print(f"Ошибка при обработке строки: {row} в файле {file_name}. Ошибка: {e}")
        print(f"Загружено {len(self.data)} товаров из файлов: {files}")


    # Напишем метод, который будет искать индексы столбцов в заголовках(название, цену, вес):
    def _search_product_price_weight(self, headers):
        '''
            Возвращает номера столбцов
        '''
        # Создадим переменные со списком возможных названий:
        product_aliases = ['название', 'продукт', 'товар', 'наименование']
        price_aliases = ['цена', 'розница']
        weight_aliases = ['фасовка', 'масса', 'вес']

        #
        # Найдем название столбца в заголовке, если найдено, вернем его индекс или None:
        product_idx = next((i for i, h in enumerate(headers) if h.lower() in product_aliases), None)
        price_idx = next((i for i, h in enumerate(headers) if h.lower() in price_aliases), None)
        weight_idx = next((i for i, h in enumerate(headers) if h.lower() in weight_aliases), None)

        return product_idx, price_idx, weight_idx


    # Создадим метод для экспорта данных в html. fname - имя файла по умолчанию.
    def export_to_html(self, data, fname='output.html'):
        if not data:
            print("Нет данных для экспорта.")
            return


        # Формируем строку с html-кодом, которая будет содержать таблицу с данными:
        result = '''
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">  <!-- Добавляем тег meta для кодировки -->
                <title>Позиции продуктов</title>
            </head>
            <body>
                <table border="1">
                    <tr>
                        <th>Номер</th>
                        <th>Название</th>
                        <th>Цена</th>
                        <th>Фасовка</th>
                        <th>Файл</th>
                        <th>Цена за кг.</th>
                    </tr>
            '''

        # Цикл, который переберет каждый элемент в data. Добавим enumerate для формирования
        # порядкового номера (порядковый номер зададим с 1, а не с 0, т.к. индексы с 0):
        # for i, item in enumerate(self.data, start=1):
        for i, item in enumerate(data, start=1):
            # для каждого элемента добавим строки с данными (наименование, цена, вес и тд)
            # i вставляет порядковый номер в ячейку, остальные - данные:
            result += f'''
                            <tr>

                                <td>{i}</td>
                                <td>{item['product']}</td>
                                <td>{item['price']}</td>
                                <td>{item['weight']}</td>
                                <td>{item['file']}</td>
                                <td>{item['price_per_kg']:.2f}</td>
                            </tr>
                        '''
        # result завершит таблицу и закроет тело и тд:
        result += '''
                        </table>
                    </body>
                    </html>
                    '''

        # откроем файл в режиме записи, запишем его:
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(result)


    # Пропишем метод для поиска товаров по тексту. resalt  примет все элементы data с текстом
    # (в нижнем регистре),который нужно найти:
    def find_text(self, text):
        result = [item for item in self.data if text.lower() in item['product'].lower()]
        self.last_search_results = sorted(result, key=lambda x: x['price_per_kg'])  # Сохранение результатов поиска
        return self.last_search_results
        # Отсортируем по цене за кг:
        # return sorted(result, key=lambda x: x['price_per_kg'])


# если файл будет запущен, а не импортирован как модуль в др программе, выполняется данный код:

if __name__ == "__main__":
#     pm = PriceMachine()
    pm = PriceMachine()
# folder_path = 'C:/Users/User/pythonProject6/PycharmProjects'
#     print(pm.load_prices())
    pm.load_prices()

# Цикл, который открыт, пока пользователь не выйдет:
    while True:
        # пропишем переменную, сохраняющую введенный пользователем текст, если выход написан - окончим цикл:
        search_text = input("Введите текст для поиска (или 'exit' для выхода): ")
        if search_text.lower() == 'exit':
            print("Работа завершена.")
            break

        # вызовем метод, который ищет товары по тексту, передадим ему введенный пользователем текст:
        results = pm.find_text(search_text)

        # если список не пустой и найдены товары подходящие, выведем заголовок и информацию о каждом товаре
        # (а так же выровняем колонки и зададим ширину):
        if results:
            print(f"{'№':<5} {'Наименование':<30} {'Цена':<10} {'Вес':<10} {'Файл':<15} {'Цена за кг.':<10}")

        # пройдемся по списку, добавляя порядковый номер, зададим вывод с 1 (чтобы список не начинался с 0).
        # Выведем данные о каждом найденном товаре - его порядковый номер, вес, название файла и цену за кг
        # (точность - 2 знака после,):
            for i, item in enumerate(results, start=1):
                print(f"{i:<5} {item['product']:<30} {item['price']:<10} {item['weight']:<10} {item['file']:<15} "
                      f"{item['price_per_kg']:<10.2f}")
            # Экспорт результатов поиска
            pm.export_to_html(results)
            print("Данные экспортированы в output.html")
        else:
            print("Товары не найдены.")

# print('the end')
# print(pm.export_to_html())
# print("Данные экспортированы в output.html")
    # Если есть последние результаты поиска, экспортируем их
    if pm.last_search_results:
        pm.export_to_html(pm.last_search_results)
    else:
        print("Нет данных для экспорта.")

    print("the end")
