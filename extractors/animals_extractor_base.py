#! /usr/bin/env python3
# coding: utf-8
# Author:  Ohad ELiyahou
# Date:    September 2024
# Summary:
import abc
import core.common as co


class AnimalsExtractor(abc.ABC):

    def __init__(self, webpage: str):
        self._webpage = webpage

    @abc.abstractmethod
    def extract_animals(self, extended: bool = False) -> co.AnimalsExtractorOutput:
        raise NotImplementedError
