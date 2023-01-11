import pprint

import requests

DOMAIN = 'https://api.hh.ru/'

url_vacancies = f'{DOMAIN}vacancies'

params = {
    'text': 'Python developer',
    # страница
    'page': 1
}

result = requests.get(url_vacancies, params=params).json()


# всего вакансий
vacancies = result['found']


# добавляем зп в лист
salary_list = []
for a, b in result.items():
    if isinstance(b, list):
        for c in b:
            for d, e in c.items():
                if isinstance(e, dict):
                    if d == 'salary':
                        for f, g in e.items():
                            if f == 'from' and e['currency'] == 'RUR' and isinstance(g, int):
                                salary_list.append(g)
                            else:
                                pass
my_sum = 0
for i in salary_list:
    my_sum += i


# my_sum - средняя зп
my_sum = my_sum / len(salary_list)


# словарь с требованиями
requirements = {'pytest': 0, 'Django': 0, 'Flask': 0, 'HTTP': 0, 'numpy': 0, 'MySql': 0}


# считаем требования в вакансиях
for a, b in result.items():
    if isinstance(b, list):
        for c in b:
            for d, e in c.items():
                if isinstance(e, dict):
                    if d == 'snippet':
                        for f, g in e.items():
                            if f == 'requirement':
                                for h, j in requirements.items():
                                    if h in g:
                                        requirements[h] += 1
                            else:
                                pass


# сохраняем данные в файл
f = open('Данные по вакансиям', 'w')

f.write(f'Данные по вакансиям:\nНайдено вакансий: {vacancies}\n'
        f'Требования в вакансиях с первой страницы hh: {requirements}\n'
        f'Средняя зп на первой странице: {my_sum}')

f.close()
