import requests

DOMAIN = 'https://api.hh.ru/'
url_vacancies = f'{DOMAIN}vacancies'

params = {
    'text': 'Python developer',
    'page': 1
}

result = requests.get(url_vacancies, params=params).json()

# Всего вакансий
vacancies = result['found']

# Собираем зарплаты "от" в рублях
salary_list = []
for vacancy in result.get('items', []):
    salary = vacancy.get('salary')
    if salary and salary.get('currency') == 'RUR' and isinstance(salary.get('from'), int):
        salary_list.append(salary['from'])

# Средняя зарплата, если есть данные
if salary_list:
    avg_salary = sum(salary_list) / len(salary_list)
else:
    avg_salary = 0

# Словарь требований
requirements = {'pytest': 0, 'Django': 0, 'Flask': 0, 'HTTP': 0, 'numpy': 0, 'MySql': 0}

# Считаем вхождения требований в snippet.requirement
for vacancy in result.get('items', []):
    snippet = vacancy.get('snippet', {})
    requirement_text = snippet.get('requirement', '').lower()  # приводим к нижнему регистру
    for req in requirements.keys():
        if req.lower() in requirement_text:
            requirements[req] += 1

# Сохраняем данные в файл
with open('Данные по вакансиям.txt', 'w', encoding='utf-8') as f:
    f.write(f'Данные по вакансиям:\nНайдено вакансий: {vacancies}\n'
            f'Требования в вакансиях с первой страницы hh: {requirements}\n'
            f'Средняя зп на первой странице: {avg_salary:.2f}')
