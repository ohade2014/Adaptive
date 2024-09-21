#! /usr/bin/env python3
# coding: utf-8
# Author:  Ohad ELiyahou
# Date:    September 2024
# Summary:
import requests
import tempfile
import extractors.animals_extractor as ae
import extractors.animal_page_extractor as ape

if __name__ == '__main__':
    main_webpage_response = requests.get(url='https://en.wikipedia.org/wiki/List_of_animal_names')
    if main_webpage_response.status_code != 200:
        raise ValueError
    main_webpage = main_webpage_response.text
    extractor = ae.create_wiki_animal_extractor(webpage=main_webpage)
    r = extractor.extract_animals(extended=True)
    for animal in r.get_list_of_animals():
        name = animal.get_name()
        page_url = animal.get_page_url()
        if not page_url:
            print(f'No page url for animal: {name}')
            continue
        response = requests.get(page_url)
        if response.status_code != 200:
            raise ValueError(f'Failed to get page for animal:{name}')
        webpage = response.text
        try:
            extractor = ape.AnimalPageExtractor(webpage=webpage)
        except Exception as e:
            print(f'Failed to fetch page for animal: {animal.get_name()}')
            continue
        image_url = extractor.extract_image_url()
        if not image_url:
            print(f'No image url for animal: {name}')
            continue
        image_response = requests.get(image_url, headers={
            'User-Agent': 'CoolBot/0.0 (https://example.org/coolbot/; coolbot@example.org)'})
        if image_response.status_code != 200:
            raise ValueError(f'Failed to download image for: {name}')
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
            tmp_file.write(image_response.content)
            print(f'File name for aminal: {animal.get_name()}: {tmp_file.name}')
