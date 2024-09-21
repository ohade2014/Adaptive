#! /usr/bin/env python3
# coding: utf-8
# Author:  Ohad ELiyahou
# Date:    September 2024
# Summary:
from unittest import TestCase
import extractors.animal_page_extractor as ape


class TestAnimalPageExtractor(TestCase):

    def setUp(self):
        with open('mocks/animal_main_page_with_image_in_main_table.txt', 'r') as file:
            self._animal_page_with_image_in_table = file.read()
        with open('mocks/animal_main_page_without_image_in_main_table.txt', 'r') as file:
            self._animal_page_without_image_in_table = file.read()

    """
    GIVEN   Animal Page html (as mock response) in Wiki (https://en.wikipedia.org/wiki/Aardvark) with image exists in the main table (Yellow background)  
    WHEN    extracting the animal data using the animal page extractor
    THEN    we get an image URL
    """
    def test_animal_page_extractor_with_image_in_main_table(self):
        page_extractor = ape.create_animal_page_extractor(self._animal_page_with_image_in_table)
        self.assertEqual('https://upload.wikimedia.org/wikipedia/commons/thumb/f/f0/Orycteropus_afer_175359469.jpg/220px-Orycteropus_afer_175359469.jpg', page_extractor.extract_image_url())

    """
    GIVEN   Animal Page html (as mock response) in Wiki (https://en.wikipedia.org/wiki/Bull) without main table  
    WHEN    extracting the animal data using the animal page extractor
    THEN    we get an image URL
    """
    def test_animal_page_extractor_without_image_in_main_table(self):
        page_extractor = ape.create_animal_page_extractor(self._animal_page_without_image_in_table)
        self.assertEqual('https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/A_Friesian_Bull%2C_Llandeilo_Graban_-_geograph.org.uk_-_579885.jpg/220px-A_Friesian_Bull%2C_Llandeilo_Graban_-_geograph.org.uk_-_579885.jpg', page_extractor.extract_image_url())