import json

import imgkit
import openpyxl
from string import Template

from tabletop_simulator import tabletop_utils



def get_html(replacements : dict[str,str]):
    with open('assets/spell_card.html', encoding="utf8") as f:
        html_template = Template(f.readlines())
        return html_template.substitute(replacements)


def process_worksheet(json_data, worksheet):
    first_line = True
    row_titles = []
    for row in worksheet.rows:
        if first_line:
            first_line = False
            row_titles.extend([i.value for i in row])
            continue

        replacements = {}
        for i in range(8):
            replacements[row_titles[i]] = row[i].value

        html_str = get_html(replacements)

        # Specify the path where the output image will be saved
        image_path = f"output/{row[1].value}.png"

        # Set the configuration options for wkhtmltoimage
        config = imgkit.config(wkhtmltoimage='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltoimage.exe')

        imgkit.from_string(html_str, image_path, config=config)
def process_workbook(filename):
    workbook = openpyxl.load_workbook(filename)
    with open('game.json', encoding="utf8") as f:
        json_data = json.load(f)

    process_worksheet(json_data, workbook["spells"])

    tabletop_utils.write_json('game.json', json_data)



if __name__ == "__main__":
    # process_file('csv_files/continent_port_tiles.csv')
    process_workbook("assets/spells.xlsx")
