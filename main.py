import Report
import table
a = input()
if a == "Статистика вакансий":
    table.getetable()
elif a == "Вакансии":
    Report.get_report()
else:
    print("Неверный формат ввода")