import operator
from abc import ABC, abstractmethod

import json
from datetime import datetime
from operator import itemgetter
from vacancy import Vacancy


def write_file(filename):
    pass


# def save_to_json(vacancy, filename):
#     vacs = []
#     for item in vacancy:
#         vacs.append(item.__dict__)
#     with open(filename, 'w', encoding='UTF-8') as f:
#         f.write(json.dumps(vacs, indent=2, ensure_ascii=False))
#     print(f'\nЗаписано {len(vacs)} вакансий в файл {filename}\n')


def hh_for_dict(hh_vacancies):
    hh_vacancies_dict = []
    for vacancy in hh_vacancies:
        hh_vacancy = Vacancy(vacancy['name'],
                             vacancy['salary']['from'],
                             vacancy['salary']['to'],
                             vacancy['alternate_url'],
                             vacancy['snippet']['requirement'],
                             vacancy['snippet']['responsibility'],
                             vacancy["published_at"])
        hh_vacancies_dict.append(hh_vacancy)
    return hh_vacancies_dict


def sj_for_dict(superjob_vacancies):
    sj_vacancies_dict = []
    for vacancy in superjob_vacancies:
        sj_vacancy = Vacancy(vacancy['profession'],
                             vacancy['payment_from'],
                             vacancy['payment_to'],
                             vacancy['link'],
                             vacancy['candidat'],
                             None,
                             vacancy["date_published"])
        sj_vacancies_dict.append(sj_vacancy)
    return sj_vacancies_dict


def sorted_data(list_vacancies):
    """
    Сортируем по дате список вакансий.
    """
    for item in list_vacancies:
        if 'superjob.ru' in item['url']:
            item['published_at'] = datetime.fromtimestamp(item['published_at'])
            item['published_at'] = item['published_at'].strftime('%d-%m-%Y %H:%M:%S')
            item['published_at'] = datetime.strptime(item['published_at'], '%d-%m-%Y %H:%M:%S')
        else:
            item['published_at'] = datetime.fromisoformat(item['published_at'])
            item['published_at'] = item['published_at'].strftime('%d-%m-%Y %H:%M:%S')
            item['published_at'] = datetime.strptime(item['published_at'], '%d-%m-%Y %H:%M:%S')
    sorted_list = sorted(list_vacancies, key=operator.itemgetter('published_at'), reverse=True)
    for item in sorted_list:
        item['published_at'] = item['published_at'].strftime('%d-%m-%Y %H:%M:%S')
    return sorted_list


def instance_vacancy_sorted(data):
    """
    Создаем список экземпляров класса, полученные после всех сортировок и фильтров.
    """
    vacancy_list = []
    for item in data:
        vacancy = Vacancy(item["name"],
                          item["salary_from"],
                          item["salary_to"],
                          item["url"],
                          item["info"],
                          item["responsibility"],
                          item["published_at"])
        vacancy_list.append(vacancy)
    return vacancy_list


def top_n_vacancies(list_vacancies, n):
    """
    Выводим top N вакансий.
    """
    list_top = []
    counter = 1
    for item in list_vacancies:
        print(item)
        list_top.append(item)
        counter += 1
        if counter > n:
            break
    return list_top


class APIIteraction(ABC):
    """
    Абстрактный класс, который обязывает реализовать методы для добавления вакансий в файл,
    получения данных из файла по указанным критериям и удаления информации о вакансиях.
    """

    @abstractmethod
    def add_vacancy(self, vacancy, filename):
        pass

    def add_vacancies(self, vacancy, vacancy2, filename):
        pass

    def get_vacancies_by_response(self, response, filename):
        pass

    def get_vacancies_by_salary(self, salary, filename):
        pass

    def delete_vacancy(self, vacancy_del, filename):
        pass

    def sort_vacancy(self, list_vacancies, filename_to):
        pass

    def read_file(self, filename):
        with open(filename, 'r', encoding='UTF-8') as f:
            data = json.load(f)
        return data

    def save_json(self, list_vacancy, file_name):
        pass


class SaveToJSON(APIIteraction):
    """
    Класс для сохранения информации о вакансиях в JSON-файл.
    """

    def add_vacancy(self, vacancy, filename):
        new_list = []
        for item in vacancy:
            new_list.append(item.__dict__)
        with open(filename, 'w', encoding='UTF-8') as f:
            f.write(json.dumps(new_list, indent=2, ensure_ascii=False))
        print(f'\nЗаписано {len(new_list)} вакансий в файл {filename}')

    def add_vacancies(self, vacancy, vacancy2, filename):
        new_list = []
        for item in vacancy:
            new_list.append(item.__dict__)
        for item in vacancy2:
            new_list.append(item.__dict__)
        with open(filename, 'w', encoding='UTF-8') as f:
            f.write(json.dumps(new_list, indent=2, ensure_ascii=False))
        print(f'\nЗаписано {len(new_list)} вакансий.\n')

    def save_json(self, list_vacancy, file_name):
        new_list = []
        for item in list_vacancy:
            new_list.append(item.__dict__)
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(json.dumps(new_list, indent=4, ensure_ascii=False))
        print('\nВсе вакансии по вашему запросу сохранены в JSON-файл.')


class LoadFileJSON(APIIteraction):
    """
    Класс для загрузки информации о вакансиях из JSON-файл.
    """

    def add_vacancy(self, vacancy, filename):
        pass

    def get_vacancies_by_salary(self, salary, filename):
        with open(filename, 'r', encoding='UTF-8') as f:
            data = json.load(f)
        new_list = []
        for item in data:
            if item['salary_from'] is None:
                continue
            if salary <= item['salary_from']:
                new_list.append(Vacancy(**item))
        return new_list


class DeleteFileJSON(APIIteraction):
    """
    Класс для удаления определенной вакансии из JSON-файл.
    """

    def add_vacancy(self, vacancy, filename):
        with open(filename, 'w', encoding='UTF-8') as f:
            f.write(json.dumps(vacancy, indent=2, ensure_ascii=False))
        print(f'\nЗаписано {len(vacancy)} вакансий в файл {filename} без лишней вакансии')

    def delete_vacancy(self, vacancy_del_url, filename):
        vacancies = []
        for vacancy in self.read_file('data/suitable_vacancies.json'):
            if vacancy['url'] != vacancy_del_url:
                vacancies.append(vacancy)
        self.add_vacancy(vacancies, filename)


class RespondFileJSON(APIIteraction):

    def add_vacancy(self, vacancy, filename):
        with open(filename, 'w', encoding='UTF-8') as f:
            f.write(json.dumps(vacancy, indent=2, ensure_ascii=False))
        print(f'\nЗаписано {len(vacancy)} вакансий в файл {filename} соответствующих запросу')

    def get_vacancies_by_response(self, response, filename):
        vacancies = []
        for vacancy in self.read_file('data/suitable_vacancies.json'):
            if response in str(vacancy['info']) or response in str(vacancy['name']):
                vacancies.append(vacancy)
        self.add_vacancy(vacancies, filename)


class SortFileJSON(APIIteraction):
    def add_vacancy(self, vacancy, filename):
        new_list = []
        for item in list_vacancy:
            new_list.append(item.__dict__)
        with open(filename, 'w', encoding='UTF-8') as f:
            f.write(json.dumps(new_list, indent=2, ensure_ascii=False))
        print(f'\nЗаписано {len(new_list)} вакансий в файл {filename} соответствующих запросу')

    def sorted_data(list_vacancies):
        """
        Сортируем по дате список вакансий.
        """
        for item in list_vacancies:
            if 'superjob.ru' in item['url']:
                item['published_at'] = datetime.fromtimestamp(item['published_at'])
                item['published_at'] = item['published_at'].strftime('%d-%m-%Y %H:%M:%S')
                item['published_at'] = datetime.strptime(item['published_at'], '%d-%m-%Y %H:%M:%S')
            else:
                item['published_at'] = datetime.fromisoformat(item['published_at'])
                item['published_at'] = item['published_at'].strftime('%d-%m-%Y %H:%M:%S')
                item['published_at'] = datetime.strptime(item['published_at'], '%d-%m-%Y %H:%M:%S')
        sorted_list = sorted(list_vacancies, key=operator.itemgetter('published_at'), reverse=True)
        for item in sorted_list:
            item['published_at'] = item['published_at'].strftime('%d-%m-%Y %H:%M:%S')
        return sorted_list




