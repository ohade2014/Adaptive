#! /usr/bin/env python3
# coding: utf-8
# Author:  Ohad ELiyahou
# Date:    September 2024
# Summary:
import typing as t


class AnimalExtractorException(Exception):
    pass


class AnimalPageExtractorException(Exception):
    pass


class Animal(object):

    def __init__(self, name: str, collateral_adjectives_list: t.List[str] = None, page_url: str = None,
                 image_url: str = None) -> None:
        self._name = name
        self._collateral_adjectives_list = collateral_adjectives_list
        self._page_url = page_url
        self._image_url = image_url

    def get_name(self) -> str:
        return self._name

    def get_collateral_adjectives_list(self) -> t.List[str]:
        return self._collateral_adjectives_list

    def get_page_url(self) -> str:
        return self._page_url

    def get_image_url(self) -> str:
        return self._image_url


class AnimalsExtractorOutput(object):

    def __init__(self, list_of_animals: t.List[Animal]) -> None:
        self._list_of_animals = list_of_animals

    def get_list_of_animals(self) -> t.List[Animal]:
        return self._list_of_animals
