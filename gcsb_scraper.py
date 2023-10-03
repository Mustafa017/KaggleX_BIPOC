from pydantic import BaseModel
from typing import List
import json
import requests
from bs4 import BeautifulSoup


class Activity(BaseModel):
    title: str
    duration: int
    type: str


class Step(BaseModel):
    activities: List[Activity]


class Module(BaseModel):
    title: str
    description: str
    steps: List[Step]


# with open('mock.json') as f:
#     data = json.load(f)
#     modules = [Module(**x) for x in data]

# print(modules)

def scraper(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    ql_course = soup.find("ql-course").attrs['modules']
    data = json.loads(ql_course)
    return data


def main():
    data = scraper(url)
    modules = [Module(**x) for x in data]
    print(modules)


url = "https://www.cloudskillsboost.google/course_templates/53?catalog_rank=%7B%22rank%22%3A1%2C%22num_filters%22%3A0%2C%22has_search%22%3Atrue%7D&search_id=25346338"

if __name__ == "__main__":
    main()
