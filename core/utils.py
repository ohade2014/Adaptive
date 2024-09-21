#! /usr/bin/env python3
# coding: utf-8
# Author:  Ohad ELiyahou
# Date:    September 2024
# Summary:


PREFIX_WIKI_URL = 'https://en.wikipedia.org'


def normalize_image_url(image_url: str) -> str:
    return f'https:{image_url}'


def get_wiki_url(postfix: str) -> str:
    return PREFIX_WIKI_URL + postfix
