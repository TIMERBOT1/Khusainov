from var_dump import var_dump
import re
import csv
from datetime import datetime
from prettytable import PrettyTable, ALL
from time import time

class DataSet:
    """Класс для распаковки csv
        Attributes:
            file_name (string): Название распаковываемого csv-файла
            vacancies_objects (list): Данные из csv-файла
    """
    def __init__(self, file_name):
        """Инициализирует объект DataSet
                Args:
                    file_name (string): имя csv-файла
        """
        self.file_name = file_name
        self.vacancies_objects = DataSet.сsv_reader(file_name)

    def сsv_reader(file_name):
        """
            Извлекает данные из csv-файла и складывает их в список
                Args: file_name(string): название csv-файла
                :return: list: список с данными из csv-файла
        """
        file_csv = open(file_name, encoding='utf_8_sig')
        reader_csv = csv.reader(file_csv)
        listData = []
        for x in reader_csv:
            listData.append(x)
        if len(listData) == 0:
            print('Пустой файл')
            exit(0)
        if len(listData) == 1:
            print("Нет данных")
            exit(0)
        columns = listData[0]
        data = listData[1:]
        class_data = []
        for x in data:
            if len(columns) == len(x) and not x.__contains__(''):
                h = Vacancy(x)
                class_data.append(h)
        return class_data


class Salary:
    """
        Класс для представления зарплаты

        Attributes:
            salary(int): средняя зарплата в рублях
            salary_currency(string): Валюта оклада
    """
    def __init__(self, salary_from, salary_to, salary_gross, salary_currency):
        """
            Инициализирует объект Salary, производит конвертацию зарплаты в указанную валюту
                :param salary_from (str or int or float): Нижняя граница вилки оклада
                :param salary_to (str or int or float): Верхняя граница вилки оклада
                :param salary_currency (str): Валюта оклада
        """
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.salary_gross = salary_gross
        self.salary_currency = salary_currency

    def conv_to_rub(self):
        """Конвертирует зарплату в рубли
        :return зарплата в рублях
        """
        return (int(float(self.salary_to)) + int(float(self.salary_from))) * currency_to_rub[self.salary_currency]


class Vacancy:
    """
        Класс для представления вакансии

        Attributes:
            name(str): название вакансии
            salary(Salary): Зарплата
            area_name(str): Регион
            published_at(int): Дата публикации
        """
    def __init__(self, vacanlist):
        """
                Инициализирует объект Vacancy
                :param vacanlist: список с данными по вакансии
        """
        self.name = vacanlist[0]
        self.description = vacanlist[1]
        self.key_skills = vacanlist[2].split('\n')
        self.experience_id = vacanlist[3]
        self.premium = vacanlist[4]
        self.employer_name = vacanlist[5]
        self.salary = Salary(vacanlist[6], vacanlist[7], vacanlist[8], vacanlist[9])
        self.area_name = vacanlist[10]
        self.published_at = vacanlist[11]


field_names = ["№", "Название", "Описание", "Навыки", "Опыт работы", "Премиум-вакансия", "Компания", "Оклад",
               "Название региона", "Дата публикации вакансии"]
translate_dict = {'name': 'Название', 'description': 'Описание', 'key_skills': 'Навыки', 'experience_id': 'Опыт работы',
                  'premium': 'Премиум-вакансия', 'employer_name': 'Компания', 'salary': 'Оклад',
                  'area_name': 'Название региона', 'published_at': 'Дата публикации вакансии'}
translate_dict_tr = dict(zip(translate_dict.values(), translate_dict.keys()))
exp_dict = {"noExperience": "Нет опыта", "between1And3": "От 1 года до 3 лет", "between3And6": "От 3 до 6 лет",
            "moreThan6": "Более 6 лет"}
exp_dict_ = {"noExperience": 0, "between1And3": 1, "between3And6": 3, "moreThan6": 6}
cur_dict = {"AZN": "Манаты", "BYR": "Белорусские рубли", "EUR": "Евро", "GEL": "Грузинский лари",
            "KGS": "Киргизский сом", "KZT": "Тенге", "RUR": "Рубли", "UAH": "Гривны", "USD": "Доллары",
            "UZS": "Узбекский сум"}
currency_to_rub = {"AZN": 35.68, "BYR": 23.91, "EUR": 59.90, "GEL": 21.74, "KGS": 0.76, "KZT": 0.13, "RUR": 1,
                   "UAH": 1.64, "USD": 60.66, "UZS": 0.0055}
yes_No = {'true': 'Да', 'false': 'Нет'}
gross = {'false': 'С вычетом налогов', 'true': 'Без вычета налогов'}


class InputConnect:
    """
       Класс для формирования статистических данных
       Attributes:
           params(list): список с названием файла и вакансии
           filename(string)
           name(string):
    """
    def __init__(self):
        """
                Инициализирует объект InputConnect
        """
        self.params = InputConnect.get_params(self)
        self.filename = self.params[0]
        self.filt_argument = self.params[1]
        self.sort_arg = self.params[2]
        self.rev = self.params[3]
        self.rows = self.params[4]
        self.fields = self.params[5]

    def get_params(self):
        """
                Считывает данные с клавиатуры для формирования статистики
                :return: список с данными введёнными с клавиатуры
        """
        filename = input('Введите название файла: ')
        filt_argument = input('Введите параметр фильтрации: ')
        sort_arg = input('Введите параметр сортировки: ')
        rev = input('Обратный порядок сортировки (Да / Нет): ')
        rows_count = input("Введите диапазон вывода: ")
        fields = input("Введите требуемые столбцы: ").split(', ')
        if not (filt_argument.__contains__(': ')) and filt_argument != '':
            print('Формат ввода некорректен')
            exit(0)
        if not field_names.__contains__(sort_arg) and sort_arg != '':
            print('Параметр сортировки некорректен')
            exit(0)
        if not (rev == 'Да' or rev == 'Нет' or rev == ''):
            print('Порядок сортировки задан некорректно')
            exit(0)
        if not field_names.__contains__(filt_argument.split(': ')[0]) and filt_argument != '' and \
                filt_argument.split(': ')[0] != 'Идентификатор валюты оклада':
            print('Параметр поиска некорректен')
            exit(0)
        return [filename, filt_argument, sort_arg, rev, rows_count, fields]

    def filtration(self, a):
        """
        Фильтрует данные
        :param a:
        :return: отфильтрованный словарь с данными
        """
        final_list = []
        vacancies = a.vacancies_objects
        if self.filt_argument == '':
            return vacancies
        filt_pol = self.filt_argument.split(': ')[0]
        filt_arg = self.filt_argument.split(': ')[1]
        for i in vacancies:
            k = i.__dict__
            sk = filt_arg.split(', ')
            if filt_pol == 'Навыки':
                flag = False
                for i1 in sk:
                    if not k['key_skills'].__contains__(i1):
                        flag = True
                        break
                if flag: continue
                final_list.append(i)

            if filt_pol == 'Идентификатор валюты оклада':
                if filt_arg == cur_dict[i.salary.salary_currency]:
                    final_list.append(i)
                continue
            if filt_pol == 'Оклад' and int(i.salary.salary_from) <= int(filt_arg) <= int(i.salary.salary_to):
                final_list.append(i)
            if filt_pol == 'Опыт работы' and exp_dict[i.experience_id] == filt_arg:
                final_list.append(i)
            if filt_pol == 'Премиум-вакансия' and yes_No[i.premium.lower()] == filt_arg:
                final_list.append(i)
            if filt_pol == "Дата публикации вакансии" and filt_arg == datetime.strptime(i.published_at,
                                                                                        '%Y-%m-%dT%H:%M:%S+0300').strftime(
                    '%d.%m.%Y'):
                final_list.append(i)
            if filt_arg == k[translate_dict_tr[filt_pol]]:
                final_list.append(i)
        if len(final_list) == 0:
            print('Ничего не найдено')
            exit(0)
        return final_list

    def sort(self, list):
        """
        Сортирует данные
        :param list:
        :return: отсортированный список
        """
        if self.sort_arg == '':
            return list
        rever = True if self.rev == 'Да' else False
        arg = lambda x: x.__dict__[translate_dict_tr[self.sort_arg]]
        salar = lambda x: Salary.conv_to_rub(x.salary)
        skills = lambda x: len(x.key_skills)
        datet = lambda x: (datetime.strptime(x.published_at, '%Y-%m-%dT%H:%M:%S+0300')).strftime('%d.%m.%Y %H:%M:%S')
        exp = lambda x: exp_dict_[x.experience_id]
        arg = salar if self.sort_arg == 'Оклад' else arg
        arg = skills if self.sort_arg == 'Навыки' else arg
        arg = exp if self.sort_arg == 'Опыт работы' else arg
        arg = datet if self.sort_arg == 'Дата публикации вакансии' else arg
        list.sort(key=arg, reverse=rever)
        return list

    def print_table(self, list):
        """Представляет данные в виде таблички

        Attributes:
            list: данные для таблички
        """

        def cleaner(j):
            j = re.sub(r"\<[^>]*\>", "", j)
            j = re.sub(r'\s+', ' ', j)
            j = j.strip()
            return j

        def limiter(stro):
            return stro if len(stro) <= 100 else f'{stro[0:100]}...'

        def separator(g):
            g = cleaner(str(g))
            g = g[::-1]
            c = 0
            k = ''
            h = ''
            for i in g:
                c = c + 1
                h = f'{h}{i}'
                if c % 3 == 0 or c == len(g):
                    k = f'{k} {h}'
                    h = ''
            k = k[::-1]
            return k

        def inter(i):
            return str(int(float(i)))

        start, end = 0, len(list)
        rows_count = self.rows.split(' ')
        if len(rows_count) == 2:
            start = int(rows_count[0]) - 1
            end = int(rows_count[1]) - 1
        if len(rows_count) == 1 and rows_count[0] != '':
            start = int(rows_count[0]) - 1
        table_list = PrettyTable()
        table_list.field_names = field_names
        table_list.max_width = 20
        table_list.align = "l"
        table_list.hrules = ALL
        j = 1
        if self.fields[0] == '':
            fields = field_names
        else:
            fields = ['№'] + self.fields
        for i in list:
            table_list.add_row([j, cleaner(i.name), limiter(cleaner(i.description)), limiter('\n'.join(i.key_skills)),
                                exp_dict[i.experience_id], yes_No[i.premium.lower()], i.employer_name,
                                f'{separator(inter(i.salary.salary_from))}- {separator(inter(i.salary.salary_to))}({cur_dict[i.salary.salary_currency]}) ({gross[i.salary.salary_gross.lower()]})',
                                i.area_name,
                                datetime.strptime(i.published_at, '%Y-%m-%dT%H:%M:%S+0300').strftime('%d.%m.%Y')])
            j = j + 1
        table_list = table_list.get_string(fields=fields, start=start, end=end)
        print(table_list)

def getetable():
    """
    Формирует табличку из данных
    :return:
    """
    m = InputConnect()
    a = DataSet(m.filename)
    p = InputConnect.filtration(m, a)
    p = InputConnect.sort(m, p)
    InputConnect.print_table(m, p)

