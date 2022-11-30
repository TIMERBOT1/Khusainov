import Report
import table
a = input()
if a == "Статистика по вакнсиям":
    table.getetable()
elif a == "Вакансии":
    Report.get_report()
else:
    print("Неверный формат ввода")