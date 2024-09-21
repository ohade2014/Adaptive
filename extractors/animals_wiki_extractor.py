#! /usr/bin/env python3
# coding: utf-8
# Author:  Ohad ELiyahou
# Date:    September 2024
# Summary:
import re
import bs4
import logging
import typing as t
import core.common as co
import core.utils as utils
import extractors.animals_extractor_base as aeb


class WikiAnimalsExtractor(aeb.AnimalsExtractor):

    def __init__(self, webpage: str):
        super().__init__(webpage=webpage)
        table_body = self._resolve_table()
        self._name_index = self._resolve_name_index(table_body=table_body)
        self._collateral_adjectives_index = self._resolve_collateral_adjectives_index(table_body=table_body)
        self._animal_items = self._resolve_animal_items(table_body=table_body)

    def extract_animals(self, extended: bool = False) -> co.AnimalsExtractorOutput:
        animal_name_to_data = dict()
        animal_to_similar_name = dict()
        for index, animal_item in enumerate(self._animal_items):
            name = self._resolve_name(animal_item=animal_item)
            if name == 'Procyonidae':
                print('f')
            self._resolve_similar_animal(name=name, animal_item=animal_item,
                                         animal_to_similar_name=animal_to_similar_name)
            collateral_adjectives_list = self._resolve_collateral_adjectives_list(animal_item=animal_item)
            page_url = None
            if extended:
                page_url = self._resolve_page_url(animal_item=animal_item)
            animal_name_to_data[name.lower()] = co.Animal(name=name,
                                                          collateral_adjectives_list=collateral_adjectives_list,
                                                          page_url=page_url)
        self._update_missing_fields(animal_name_to_data=animal_name_to_data,
                                    animal_to_similar_name=animal_to_similar_name)
        return co.AnimalsExtractorOutput(list_of_animals=list(animal_name_to_data.values()))

    def _resolve_name(self, animal_item: bs4.Tag) -> str:
        name_item_attribute = self._resolve_attribute_item(animal_item=animal_item, attribute_index=self._name_index,
                                                           attribute_name='Name')
        if not name_item_attribute or not (name_item := name_item_attribute.find('a')):
            raise co.AnimalExtractorException(f'Can not resolve name, Name attribute: {name_item_attribute}')
        relevant_names = list()
        for name_item_content in name_item.contents:
            if isinstance(name_item_content, bs4.NavigableString):
                relevant_names.extend(list(name_item_content.stripped_strings))
        if len(relevant_names) != 1:
            raise co.AnimalExtractorException(
                f'Unexpected number of names found ({relevant_names}) for animal: {animal_item}')
        return relevant_names[0]

    def _resolve_similar_animal(self, name: str, animal_item: bs4.Tag,
                                animal_to_similar_name: t.Dict[str, str]) -> None:
        name_item_attribute = self._resolve_attribute_item(animal_item=animal_item, attribute_index=self._name_index,
                                                           attribute_name='Name')
        name_item_attribute_text = name_item_attribute.text
        match = re.search(r'see\s+([A-Za-z]+)', name_item_attribute_text, re.IGNORECASE)
        if match:
            similar_name = match.group(1)
            animal_to_similar_name[name] = similar_name

    def _resolve_collateral_adjectives_list(self, animal_item: bs4.Tag) -> t.Optional[t.List[str]]:
        try:
            collateral_adjectives_items = self._resolve_attribute_item(animal_item=animal_item,
                                                                       attribute_index=self._collateral_adjectives_index,
                                                                       attribute_name='collateral_adjectives')
            relevant_collateral_adjectives_items = list()
            for collateral_adjectives_item in collateral_adjectives_items.contents:
                if isinstance(collateral_adjectives_item, bs4.NavigableString):
                    relevant_collateral_adjectives_items.extend(list(collateral_adjectives_item.stripped_strings))
            return list(filter(lambda x: x not in ['-', '—'], relevant_collateral_adjectives_items))
        except co.AnimalExtractorException as _e:
            logging.exception('Failed to fetch collateral_adjectives')

    def _resolve_page_url(self, animal_item: bs4.Tag) -> str:
        try:
            name_attribute_item = self._resolve_attribute_item(animal_item=animal_item,
                                                               attribute_index=self._name_index,
                                                               attribute_name='Name')
            if not (animal_a := name_attribute_item.find('a')):
                raise co.AnimalExtractorException(
                    f'Can not resolve animal image URL, no page URL found in: {animal_item.text}')
            if not (animal_url := animal_a['href']):
                raise co.AnimalExtractorException(
                    f'Can not resolve animal image URL, Page reference exists: {animal_a.text}')
            return utils.get_wiki_url(postfix=animal_url)
        except co.AnimalExtractorException as _e:
            logging.exception('Failed to fetch page URL')

    def _resolve_table(self):
        soup = bs4.BeautifulSoup(self._webpage, "html.parser")
        element_name = 'table'
        element_attributes = {'class': ['wikitable', 'sortable', 'sticky-header', 'jquery-tablesorter']}
        relevant_elements = soup.find_all(element_name, element_attributes)
        if len(relevant_elements) <= 1:
            raise co.AnimalExtractorException('Unexpected number of table elements while extracting the animals table,'
                                              ' probably page has been changed')
        relevant_animal_table = relevant_elements[1]
        if not (t_body := relevant_animal_table.find('tbody')):
            raise co.AnimalExtractorException('Can not find animal table body in element')
        return t_body

    def _resolve_name_index(self, table_body: bs4.Tag) -> t.Optional[int]:
        return self._resolve_header_index(table_body=table_body, header_name='Animal')

    def _resolve_collateral_adjectives_index(self, table_body: bs4.Tag) -> t.Optional[int]:
        return self._resolve_header_index(table_body=table_body, header_name='Collateral adjective')

    @staticmethod
    def _resolve_header_index(table_body: bs4.Tag, header_name: str) -> t.Optional[int]:
        table_headers = [r.text for r in table_body.find_all('th')]
        try:
            return table_headers.index(header_name)
        except Exception as _e:
            raise co.AnimalExtractorException(f'Can not find {header_name} column index')

    @staticmethod
    def _resolve_animal_items(table_body) -> t.List[bs4.Tag]:
        return [r for r in table_body.find_all('tr') if r.find('td')]

    @staticmethod
    def _resolve_attribute_item(animal_item: bs4.Tag, attribute_index: int, attribute_name: str) -> bs4.Tag:
        animal_attributes = animal_item.find_all('td')
        if not animal_attributes or len(animal_attributes) <= attribute_index:
            raise co.AnimalExtractorException(
                f'Can not find animal {attribute_name} for animal item: {animal_item.get_text()}')
        return animal_attributes[attribute_index]

    @staticmethod
    def _update_missing_fields(animal_name_to_data: t.Dict[str, co.Animal],
                               animal_to_similar_name: t.Dict[str, str]) -> None:
        for animal_name, similar_animal_name in animal_to_similar_name.items():
            if (animal_data := animal_name_to_data.get(animal_name.lower())) and (
            similar_animal_data := animal_name_to_data.get(similar_animal_name.lower())):
                if not animal_data.get_collateral_adjectives_list():
                    animal_data.set_collateral_adjectives_list(similar_animal_data.get_collateral_adjectives_list())


def create_wiki_animal_extractor(webpage: str):
    return WikiAnimalsExtractor(webpage=webpage)
