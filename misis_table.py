import requests
from bs4 import BeautifulSoup

def load_page(url):
    page = requests.get(url)
    return page

specialty = int(input("Выберите специальность: ПИ - 1, ИВТ - 2\n"))
if (specialty == 1):
    url = "https://misis.ru/applicants/admission/progress/magistracy/list-of-applicants/list/?id=MAG-BUDJ-O-090403-000004839-ITKN-NITU_MISIS"
elif (specialty == 2):
    url = "https://misis.ru/applicants/admission/progress/magistracy/list-of-applicants/list/?id=MAG-BUDJ-O-090401-000004828-ITKN-NITU_MISIS"
else:
    print("Такой специальности нет, просто напиши цифру из предложенных.")
    exit()

page = load_page(url=url)

soup = BeautifulSoup(page.text, "html.parser")

table_rows_raw = soup.find_all("tr")[1:]

table_rows = []
# id, общая сумма баллов, оригинал, ВП
for row in table_rows_raw:
    row_data = row.find_all("td")
    row_tuple = (int(str(row_data[3])[4:-5]),
                 True if str(row_data[7])[4:-5] == "+" else False,
                 True if str(row_data[9])[4:-5] == "+" else False)
    table_rows.append(row_tuple)

# Фильтруем кортежи, оставляя только те, где подан оригинал и высший приоритет
filtered_rows = [row for row in table_rows if row[1] == True and row[2] == True]

# Сортируем по баллам в нисходящем порядке
sorted_data = sorted(filtered_rows, key=lambda x: x[0], reverse=True)

sorted_data = [(id + 1, row) for id, row in enumerate(sorted_data)]

print("\nТаблица для", "ПИ" if specialty == 1 else "ИВТ")
print("Место, (Баллы, Ориг, ВП)\n----------------")
print(*sorted_data, sep="\n")
