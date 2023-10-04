from pydantic import BaseModel
from typing import List
import requests
from selectolax.parser import HTMLParser
import csv


class Course(BaseModel):
    title: str
    href: str
    description: str
    duration: str
    level: str
    cost: str


def get_html(page):
    url = f"https://www.cloudskillsboost.google/catalog?format%5B%5D=courses&page={page}"
    r = requests.get(url)
    html_tree = HTMLParser(r.text)
    return html_tree


def parse_html(html):
    courses = html.css("div.catalog-item")

    catalog = []
    for course in courses:
        new_course = Course(
            title=course.css_first("h3.catalog-item__title").text().strip(),
            href=course.css_first(
                "h3.catalog-item__title a").attributes['href'],
            description=course.css_first(
                "p.catalog-item__description").text().strip(),
            duration=course.css_first(
                "div.catalog-item-duration").text().strip(),
            level=course.css_first("div.catalog-item-level").text().strip(),
            cost=course.css_first("div.catalog-item-cost").text().strip()
        )
        catalog.append(dict(new_course))
    return catalog


def write_csv(res):
    with open('catalog.csv', "a") as f:
        writer = csv.DictWriter(
            f, fieldnames=["title", "href", "description", "duration", "level", "cost"])
        writer.writerows(res)


def main():
    for i in range(1, 11):
        tree = get_html(i)
        res = parse_html(tree)
        write_csv(res)


if __name__ == "__main__":
    main()
