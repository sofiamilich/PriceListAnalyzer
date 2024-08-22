# PriceAnaliz

## Обзор проекта

`PriceAnaliz` — это инструмент для анализа прайс-листов, который загружает данные из множества CSV файлов, содержащих информацию о товарах, ценах и весе. Программа позволяет искать товары по тексту сразу во всех файлах, в названии которых есть слово "price", сортировать результаты по цене за килограмм, выдать имя файла, в котором нашел товар, и экспортировать данные в HTML файл.
По запросу можно добавить вывод в exel.

## Почему это важно?

Этот инструмент позволяет быстро и эффективно искать данные о товарах из различных источников, что особенно полезно для анализа цен и весов товаров, сравнения предложений от разных поставщиков.

## Установка

1. Убедитесь, что у вас установлен Python 3.6 или выше.

2. Клонируйте репозиторий или загрузите файлы проекта:

    ```sh
    git clone <URL-вашего-репозитория>
    cd <папка-проекта>
    ```

3. Импортируйте необходимые библиотеки:

    ```sh
    import os
    import csv
    ```

## Использование

1. Поместите все файлы прайс-листов в папку с проектом. Замените путь на данные файлы, изменив в коде директорию `file_path`. Убедитесь, что название файлов содержит слово "price" и они имеют формат CSV с разделителем `,`.

2. Запустите программу.

3. Введите наименование продукта для поиска в консоли. Программа выведет результаты поиска в виде таблицы, отсортированной по цене за килограмм.

4. Для выхода из программы введите `exit`.

## Примеры использования

Введите текст для поиска:

    ```
    Введите текст для поиска (или 'exit' для выхода): кальмар
    ```

Программа выведет список товаров, содержащих "кальмар" в названии, отсортированный по цене за килограмм:

    ```
    №    Наименование               Цена      Вес       Файл         Цена за кг.
    1    кальмар тушка               3420     3        price_3.csv  1140.00
    2    кальмар тушка               4756     4        price_0.csv  1189.00
    ```

## Экспорт в HTML

После выполнения поиска программа экспортирует результаты в HTML файл `output.html`. Этот файл содержит таблицу с результатами поиска.

## Внесение вклада

Если вы хотите внести свой вклад в проект, пожалуйста, создайте запрос на извлечение (pull request) с описанием изменений. Обязательно добавьте тесты и убедитесь, что все существующие тесты проходят успешно.

## Лицензия

Этот проект лицензируется под MIT License. См. файл [LICENSE](LICENSE) для подробностей.

## Контакты

Если у вас есть вопросы или предложения или пожелания для дополнения функциональности, пожалуйста, свяжитесь с [sofyamilich@gmail.com].
