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


class WikiAnimalsExtractor:

    def __init__(self, webpage: str):
        self._webpage = webpage
        table_body = self._resolve_table()
        self._name_index = self._resolve_name_index(table_body=table_body)
        self._collateral_adjectives_index = self._resolve_collateral_adjectives_index(table_body=table_body)
        self._animal_items = self._resolve_animal_items(table_body=table_body)

    def extract_animals(self, extended: bool = False) -> co.AnimalsExtractorOutput:
        animal_list = list()
        for index, animal_item in enumerate(self._animal_items):
            name = self._resolve_name(animal_item=animal_item)
            collateral_adjectives_list = self._resolve_collateral_adjectives_list(animal_item=animal_item)
            #similar_animal =
            page_url = None
            if extended:
                page_url = self._resolve_page_url(animal_item=animal_item)
            animal_list.append(co.Animal(name=name, collateral_adjectives_list=collateral_adjectives_list,
                                         page_url=page_url))
        return co.AnimalsExtractorOutput(list_of_animals=animal_list)

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

    def _resolve_collateral_adjectives_list(self, animal_item: bs4.Tag) -> t.Optional[t.List[str]]:
        try:
            collateral_adjectives_items = self._resolve_attribute_item(animal_item=animal_item,
                                                                       attribute_index=self._collateral_adjectives_index,
                                                                       attribute_name='collateral_adjectives')
            collateral_adjectives_item_values = list(collateral_adjectives_items.stripped_strings)
            if not collateral_adjectives_item_values:
                raise co.AnimalExtractorException(f'Can not resolve collateral_adjectives,'
                                                  f' exist values in attribute: {collateral_adjectives_item_values},'
                                                  f'animal item: {animal_item.get_text()}')
            return list(filter(lambda x: x not in ['-', '—'], collateral_adjectives_item_values))
        except co.AnimalExtractorException as e:
            print(f'{e}')

    def _resolve_page_url(self, animal_item: bs4.Tag) -> str:
        name_attribute_item = self._resolve_attribute_item(animal_item=animal_item, attribute_index=self._name_index,
                                                           attribute_name='Name')
        if not (animal_a := name_attribute_item.find('a')):
            raise co.AnimalExtractorException(
                f'Can not resolve animal image URL, no page URL found in: {animal_item.text}')
        if not (animal_url := animal_a['href']):
            raise co.AnimalExtractorException(
                f'Can not resolve animal image URL, Page reference exists: {animal_a.text}')
        return utils.get_wiki_url(postfix=animal_url)

    def _resolve_attribute_value(self, animal_item, attribute_index: int, attribute_name: str):
        animal_attribute_item = self._resolve_attribute_item(animal_item=animal_item, attribute_index=attribute_index,
                                                             attribute_name=attribute_name)
        if not animal_attribute_item:
            raise co.AnimalExtractorException(f'Can not find animal attribute for item: {animal_item.text}')
        if not (animal_attribute_item_strings := [r.stripped_strings for r in animal_attribute_item.contents if
                                                  isinstance(r, bs4.NavigableString)]):
            raise co.AnimalExtractorException(f'Can not find animal relevant values for item: {animal_item.text}')
        return animal_attribute_item_strings

    @staticmethod
    def _resolve_attribute_item(animal_item: bs4.Tag, attribute_index: int, attribute_name: str) -> bs4.Tag:
        animal_attributes = animal_item.find_all('td')
        if not animal_attributes or len(animal_attributes) <= attribute_index:
            raise co.AnimalExtractorException(
                f'Can not find animal {attribute_name} for animal item: {animal_item.get_text()}')
        return animal_attributes[attribute_index]

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

    @staticmethod
    def _resolve_header_index(table_body: bs4.Tag, header_name: str) -> t.Optional[int]:
        table_headers = [r.text for r in table_body.find_all('th')]
        try:
            return table_headers.index(header_name)
        except Exception as _e:
            raise co.AnimalExtractorException(f'Can not find {header_name} column index')

    def _resolve_name_index(self, table_body: bs4.Tag) -> t.Optional[int]:
        return self._resolve_header_index(table_body=table_body, header_name='Animal')

    def _resolve_collateral_adjectives_index(self, table_body: bs4.Tag) -> t.Optional[int]:
        return self._resolve_header_index(table_body=table_body, header_name='Collateral adjective')

    @staticmethod
    def _resolve_animal_items(table_body) -> t.List[bs4.Tag]:
        return [r for r in table_body.find_all('tr') if r.find('td')]


def create_wiki_animal_extractor(webpage: str):
    return WikiAnimalsExtractor(webpage=webpage)


if __name__ == '__main__':
    webpage = requests.get(url='https://en.wikipedia.org/wiki/List_of_animal_names')
    extractor = create_wiki_animal_extractor(webpage=webpage.text)
    r = extractor.extract_animals(extended=True)
    print('r')
