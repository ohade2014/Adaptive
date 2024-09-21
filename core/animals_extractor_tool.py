#! /usr/bin/env python3
# coding: utf-8
# Author:  Ohad ELiyahou
# Date:    September 2024
# Summary:
import requests
import core.common as co
import extractors.animals_wiki_extractor as awe
import extractors.animal_page_extractor as ape
import downloaders.animal_image_downloader as aid
from exporters.animal_exporter_html import AnimalExporterHTML

image_downloader = aid.create_image_downloader()


def _extract_main_page():
    main_webpage_response = requests.get(url='https://en.wikipedia.org/wiki/List_of_animal_names')
    if main_webpage_response.status_code != 200:
        raise ValueError(f'Failed to get main animals page, status code: {main_webpage_response.status_code}')
    return main_webpage_response.text


def _download_image(animal: co.Animal) -> str:
    name = animal.get_name()
    if not (page_url := animal.get_page_url()):
        raise ValueError(f'No page url found for {name}')
    response = requests.get(page_url)
    if response.status_code != 200:
        raise ValueError(f'Failed to get page for animal:{name}, status code: {response.status_code}')
    webpage = response.text
    extractor = ape.create_animal_page_extractor(webpage=webpage)
    image_url = extractor.extract_image_url()
    if not image_url:
        raise ValueError(f'Failed to get image url for animal:{name}, status code: {response.status_code}')
    return image_downloader.download(image_url=image_url,
                                     headers={
                                         'User-Agent': 'CoolBot/0.0 (https://example.org/coolbot/; '
                                                       'coolbot@example.org)'})


if __name__ == '__main__':
    main_webpage = _extract_main_page()
    wiki_animal_extractor = awe.create_wiki_animal_extractor(webpage=main_webpage)
    animal_extractor_output = wiki_animal_extractor.extract_animals(extended=True)
    for animal_obj in animal_extractor_output.get_list_of_animals():
        file_path = _download_image(animal=animal_obj)
        animal_obj.set_image_path(image_path=file_path)
        print(f'Animal name: {animal_obj.get_name()},'
              f' collateral_adjectives: {animal_obj.get_collateral_adjectives_list()},'
              f' Image local file path: {file_path}')
    AnimalExporterHTML.export(animal_list=animal_extractor_output.get_list_of_animals())
    print('r')
