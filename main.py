import os

from api_classes import HeadHunterAPI, SuperJobAPI
from json_interaction import SortFileJSON, SaveToJSON, LoadFileJSON, DeleteFileJSON, \
    RespondFileJSON, hh_for_dict, sj_for_dict, sorted_data, instance_vacancy_sorted, top_n_vacancies

SUPER_JOB_API_KEY = os.environ.get('sj_key')


# Создание экземпляра класса для работы с API сайтов с вакансиями
hh_api = HeadHunterAPI()
superjob_api = SuperJobAPI()

# Получение вакансий с разных платформ
hh_vacancies = hh_api.get_vacancies("Python")
sj_vacancies = superjob_api.get_vacancies("Python")
json_saver = SaveToJSON()


def user_interaction():
    platforms = ['1', '2', '3']
    platform = 0

    # Выбор платформы и сохранений вакансий в файл
    while platform not in platforms:
        resposibility_sj = 'см. в предыдущее поле'
        platform = input("Выберите платформу (1 или 2 или 3(все)):\n   1) HeadHunter\n   2) SuperJob\n   3) Все\n")
        if platform == "1":
            print("Вы выбрали HeadHunter")
            json_saver.add_vacancy(hh_for_dict(hh_vacancies), 'data/all_vacancies.json')
        elif platform == "2":
            print("Вы выбрали SuperJob")
            json_saver.add_vacancy(sj_for_dict(sj_vacancies), 'data/all_vacancies.json')
        elif platform == "3":
            print("Вы выбрали все платформы вакансий")
            json_saver.add_vacancies(hh_for_dict(hh_vacancies), sj_for_dict(sj_vacancies), 'data/all_vacancies.json')
        else:
            print("Неправильный ввод. Попробуйте ещё раз.\n")

    # Фильтр вакансии по зарплате не менее чем
    min_salary = int(input("Введите минимальную зарплату:\n"))
    json_loader = LoadFileJSON()
    dict_vacancy_with_salary_filter = json_loader.get_vacancies_by_salary(min_salary, 'data/all_vacancies.json')

    # Записываю в файл data suitable_vacancies.json
    json_saver.add_vacancy(dict_vacancy_with_salary_filter, 'data/suitable_vacancies.json')

    # Сортировка вакансий по зарплате от меньшего к большему
    # json_sort = SortFileJSON()

    # Удаляю вакансию по ссылке
    # vac_del_url = input('Введите url нежелаемой вакансии')
    json_deleter = DeleteFileJSON()
    json_deleter.delete_vacancy("https://hh.ru/vacancy/84302495", 'data/suitable_vacancies_del.json')

    # Поисковый запрос пользователя в описании вакансии
    response = input("Введите поисковый запрос:\n")
    json_response = RespondFileJSON()
    json_response.get_vacancies_by_response(response, 'data/suitable_vacancies_by_response.json')
    suitable_vacancies = json_loader.read_file("data/suitable_vacancies_by_response.json")

    #  сортируем список вакансий по дате
    sort_data = sorted_data(suitable_vacancies)

    # создаем экземпляры класса после применения всех фильтров и сортировки
    list_instance_vacancy_sorted = instance_vacancy_sorted(sort_data)

    # выводим топ N список вакансий
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    list_top = top_n_vacancies(list_instance_vacancy_sorted, top_n)

    # сохраняем top N список вакансий в json файл
    while True:
        save_json = input("Сохранить в json файл? [y/n]: ")
        if save_json.lower() == 'y':
            json_saver.save_json(list_instance_vacancy_sorted, "data/vacancy.json")
            json_saver.save_json(list_top, "data/vacancy_top.json")
            break
        elif save_json.lower() == 'n':
            print('Программа завершена')
            break
        else:
            print('Неверный ввод')


if __name__ == "__main__":
    user_interaction()



