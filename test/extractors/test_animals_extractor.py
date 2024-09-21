#! /usr/bin/env python3
# coding: utf-8
# Author:  Ohad ELiyahou
# Date:    September 2024
# Summary:
from unittest import TestCase
import typing as t
import core.common as co
import extractors.animals_wiki_extractor as awe


class TestWikiAnimalsExtractor(TestCase):

    def setUp(self):
        with open('mocks/animals_page.txt', 'r') as file:
            self._valid_animal_page = file.read()
        with open('mocks/non_valid_animal_page.txt', 'r') as file:
                self._non_valid_animal_page = file.read()

    """
    GIVEN   An empty mock response  
    WHEN    calling the extractor constructor
    THEN    AnimalExtractorException will be raised with a warning that the page may be changed and the table can not be found
    """
    def test_non_valid_animal_page_extract(self):
        with self.assertRaises(co.AnimalExtractorException):
            self._extractor = awe.create_wiki_animal_extractor(webpage=self._non_valid_animal_page)

    """
    GIVEN   Wiki all Animal Page (as mock response)(https://en.wikipedia.org/wiki/List_of_animal_names)  
    WHEN    extracting the animals data using WikiAnimalsExtractor
    THEN    we get an AnimalsExtractorOutput with a list of animals
    """
    def test_valid_animal_page_extract(self):
        self._extractor = awe.create_wiki_animal_extractor(webpage=self._valid_animal_page)
        animals_output = self._extractor.extract_animals()
        self.assertTrue(len(animals_output.get_list_of_animals()) > 0)

    """
    GIVEN   Wiki all Animal Page (as mock response) (https://en.wikipedia.org/wiki/List_of_animal_names) with a row for Weasel
    WHEN    extracting the animals data using WikiAnimalsExtractor
    THEN    we get the Weasel Animal object with the expected_collateral_adjectives and the expected_page_url
    """
    def test_animals_extractor_for_animal_with_single_collateral_adjectives(self):
        self._test_animal_extractor(animal_name='Weasel', expected_page_url='https://en.wikipedia.org/wiki/Weasel',
                                    expected_collateral_adjectives=['musteline'])

    """
    GIVEN   Wiki all Animal Page (as mock response) (https://en.wikipedia.org/wiki/List_of_animal_names) with a row for
            Bull
    WHEN    extracting the animals data using WikiAnimalsExtractor
    THEN    we get the Bull Animal object with the expected_collateral_adjectives (that has been taken from the Cattle
            Animal data) and the expected_page_url
    """
    def test_animals_extractor_for_animal_with_reference_to_another_animal(self):
        self._test_animal_extractor(animal_name='Bull', expected_page_url='https://en.wikipedia.org/wiki/Bull',
                                    expected_collateral_adjectives=['bovine','taurine (male)', 'vaccine (female)',
                                                                    'vituline (young)'])

    """
    GIVEN   Wiki all Animal Page (as mock response) (https://en.wikipedia.org/wiki/List_of_animal_names) with a row for
            Bee
    WHEN    extracting the animals data using WikiAnimalsExtractor
    THEN    we get the Bee Animal object with the expected_collateral_adjectives (multiple values) 
            and the expected_page_url
    """
    def test_animals_extractor_for_animal_with_multiple_collateral_adjectives(self):
        self._test_animal_extractor(animal_name='Bee', expected_page_url='https://en.wikipedia.org/wiki/Bee',
                                    expected_collateral_adjectives=['apian','apiarian', 'apic'])

    def _test_animal_extractor(self, animal_name: str, expected_page_url: str,
                               expected_collateral_adjectives: t.List[str]):
        self._extractor = awe.create_wiki_animal_extractor(webpage=self._valid_animal_page)
        animals_output = self._extractor.extract_animals(extended=True)
        relevant_animal_list = list(filter(lambda animal: animal.get_name() == animal_name, animals_output.get_list_of_animals()))
        self.assertEqual(1, len(relevant_animal_list))
        relevant_animal: co.Animal = relevant_animal_list[0]
        self.assertEqual(expected_page_url, relevant_animal.get_page_url())
        self.assertCountEqual(expected_collateral_adjectives, relevant_animal.get_collateral_adjectives_list())