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
import logging


class AnimalPageExtractor:

    def __init__(self, webpage: str):
        self._webpage = webpage
        self._soup = bs4.BeautifulSoup(self._webpage, "html.parser")
        self._main_table = self._resolve_main_table()

    def _resolve_main_table(self):
        try:
            element_name = 'table'
            element_attributes = {'class': ['infobox', 'biota']}
            relevant_element = self._soup.find(element_name, element_attributes)
            return relevant_element.find('tbody')
        except Exception as _e:
            logging.debug(f'Failed to resolve main table')

    def extract_image_url(self) -> t.Optional[str]:
        if self._main_table:
            if image_url := self._resolve_image_from_main_table():
                return image_url
        return self._resolve_image_from_page()

    def _resolve_image_from_main_table(self) -> t.Optional[str]:
        if not (img_tag := self._main_table.find('img')):
            logging.debug('Can not find image item in main table')
            return
        if image_url_src := img_tag['src']:
            return utils.normalize_image_url(image_url=image_url_src)

    def _resolve_image_from_page(self) -> t.Optional[str]:
        if first_image := self._soup.find('img', {'class': ['mw-file-element']}):
            if image_url_src := first_image['src']:
                return utils.normalize_image_url(image_url=image_url_src)


def create_animal_page_extractor(webpage: str):
    return AnimalPageExtractor(webpage=webpage)
