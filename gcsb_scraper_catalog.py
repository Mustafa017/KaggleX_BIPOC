from dataclasses import dataclass, asdict
from typing import List, Optional
import requests
from selectolax.parser import HTMLParser
import csv
import json
from urllib.parse import urljoin

"""

A data class is a class typically containing mainly data, although there aren’t really any restrictions. 
It is created using the new @dataclass decorator.
A data class is a regular Python class. The only thing that sets it apart is that it has basic 
data model methods like .__init__(), .__repr__(), and .__eq__() implemented for you.

"""


@dataclass
class Course:
    title: str
    href: str
    description: str
    level: str
    cost: str
    duration: str


@dataclass
class Response:
    body: HTMLParser
    next_page: dict


def get_html(url):
    payload = {'format': 'courses'}
    r = requests.get(url, params=payload)
    html_tree = HTMLParser(r.text)
    next_page_selector = html_tree.css_first("a.next_page")
    if next_page_selector:
        next_page = next_page_selector.attributes
    else:
        next_page = {"href": False}
    return Response(body=html_tree,  next_page=next_page)


def parse_link(html):
    links = html.css("a.next_page")
    return [link.attrs['href'] for link in links]


def parse_html(html, selector):
    if html.css_first(selector):
        return html.css_first(selector, strict=True).text(strip=True)
    else:
        return html.css_first(selector, default=None, strict=True)


def extract_text(html):
    courses = html.css("div.catalog-item")

    catalog = []
    for course in courses:
        new_course = Course(
            title=parse_html(course, "h3.catalog-item__title"),
            href=course.css_first(
                "h3.catalog-item__title a").attributes['href'],
            description=parse_html(course, "p.catalog-item__description"),
            level=parse_html(course, "div.catalog-item-level"),
            cost=parse_html(course, "div.catalog-item-cost"),
            duration=parse_html(course, "div.catalog-item-duration")
        )
        print(new_course)
        print("\n")
        catalog.append(asdict(new_course))
    return catalog


def write_csv(res):
    with open('data/catalog.csv', "a") as f:
        writer = csv.DictWriter(
            f, fieldnames=["title", "href", "description", "duration", "level", "cost"])
        writer.writerows(res)


def run_pagination():
    url = "https://www.cloudskillsboost.google/catalog"
    while True:
        page = get_html(url)
        # print(page.body.html)
        # print(page.body.css_first('ql-course'))
        parse_link(page.body)
        catalog = extract_text(page.body)
        write_csv(catalog)
        if page.next_page['href'] is False:
            break
        else:
            url = urljoin(url, page.next_page['href'])
            print(url)


def main():
    run_pagination()


if __name__ == "__main__":
    main()
