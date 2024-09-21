#! /usr/bin/env python3
# coding: utf-8
# Author:  Ohad ELiyahou
# Date:    September 2024
# Summary:
import bs4
import requests
import typing as t
import core.common as co
import core.utils as utils



class AnimalPageExtractor:

    def __init__(self, webpage: str):
        self._webpage = webpage
        self._main_table = self._resolve_main_table()

    def _resolve_main_table(self):
        soup = bs4.BeautifulSoup(self._webpage, "html.parser")
        element_name = 'table'
        element_attributes = {'class': ['infobox', 'biota']}
        relevant_element = soup.find(element_name, element_attributes)
        if not relevant_element:
            raise co.AnimalPageExtractorException('Could not find main table element')
        if not (table_body := relevant_element.find('tbody')):
            raise co.AnimalPageExtractorException('Could not extract the table body')
        return table_body

    def extract_image_url(self) -> t.Optional[str]:
        if not(img_tag := self._main_table.find('img')):
            raise
        if image_url_src := img_tag['src']:
            return utils.normalize_image_url(image_url_src)


if __name__ == '__main__':
    example_url = 'https://en.wikipedia.org/wiki/Aardvark'
    response = requests.get(example_url)
    webpage = response.text
    s = AnimalPageExtractor(webpage=webpage)
    r = s.extract_image_url()
    print(r)