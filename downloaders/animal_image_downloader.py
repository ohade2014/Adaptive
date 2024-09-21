#! /usr/bin/env python3
# coding: utf-8
# Author:  Ohad ELiyahou
# Date:    September 2024
# Summary:
import requests
import tempfile


class ImageDownloader:

    def __init__(self, default_headers: dict = None):
        self._default_headers = default_headers

    def download(self, image_url: str, file_path: str = None, headers: dict = None) -> str:
        image_response = requests.get(url=image_url,
                                      headers=headers if headers else self._default_headers)
        if image_response.status_code != 200:
            raise ValueError(f'Failed to download image for: {image_url}, status code: {image_response.status_code}')
        if file_path:
            with open(file_path, 'b+') as file:
                file.write(image_response.content)
                return file_path
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
            tmp_file.write(image_response.content)
            return tmp_file.name


def create_image_downloader():
    return ImageDownloader()
