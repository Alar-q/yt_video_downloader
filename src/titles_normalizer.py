import re


def normalize(title):

    # Преобразуем название файла в нормальный вид
    # Убираем символы, которые не разрешены в названиях файлов
    normalized_title = re.sub(r'[^\w\s-]', '', title).strip().lower()

    # Заменяем пробелы на дефисы
    normalized_title = re.sub(r'[\s]+', '_', normalized_title)

    return normalized_title


if __name__ == "__main__":
    title = normalize(title='Essence of linear algebra')
    print(title)
