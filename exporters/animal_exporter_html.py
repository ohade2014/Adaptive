#! /usr/bin/env python3
# coding: utf-8
# Author:  Ohad ELiyahou
# Date:    September 2024
# Summary:
import typing as t
import core.common as co


class AnimalExporterHTML:

    @staticmethod
    def export(animal_list: t.List[co.Animal]) -> None:
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Animals and Collateral Adjectives</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                }}
                .animal {{
                    margin-bottom: 20px;
                }}
                img {{
                    width: 200px;
                    height: auto;
                    margin-top: 10px;
                }}
            </style>
        </head>
        <body>
            <h1>List of Animals and Their Collateral Adjectives</h1>
            <div class="animal-list">
        """
        for animal in animal_list:
            html_content += f"""
            <div class="animal">
                <h2>{animal.get_name()}</h2>
                <p><strong>Collateral Adjectives:</strong> {', '.join(animal.get_collateral_adjectives_list()) if animal.get_collateral_adjectives_list() else '-'}</p>
                <img src="{animal.get_image_path()}" alt="{animal.get_name()} image"/>
            </div>
            """

        html_content += """
            </div>
        </body>
        </html>
        """

        with open('animal_list.html', 'w+') as file:
            file.write(html_content)
        print("HTML file created: animal_list.html")
