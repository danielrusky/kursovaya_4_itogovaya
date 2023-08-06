import os

import requests

params = {
    "text": "NAME: программист",
    "area": 2,
    "accept_incomplete_resumes": False,
    "salary": "NAME: программист",
    "page": 0,
    "pages": 13,
    "per_page": 1
}

data = requests.get("https://api.hh.ru/vacancies", params=params)


super_job_key = os.getenv('sj_key')