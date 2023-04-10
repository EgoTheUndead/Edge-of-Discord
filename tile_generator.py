import json
import csv
import os
from pathlib import Path
import re

import psd_tools.api.layers
from psd_tools import PSDImage
import openpyxl

from tabletop_simulator import tabletop_utils

tiles_path = "output/tiles"
use_local_images = False

all_object_layers = set()


def print_layers():
    layers = set()
    for layer in all_object_layers:
        layers.add(re.sub(r"_\d", '', layer))

    layers_sorted = list(layers)
    layers_sorted.sort()

    for name in layers_sorted:
        print(name)


def update_visibility(psd: PSDImage, visible_layers: list[str]):
    for layer in psd:
        if isinstance(layer, psd_tools.api.layers.Group):
            layer.visible = True
            for sublayer in layer:
                all_object_layers.add(sublayer.name)
                sublayer.visible = sublayer.name in visible_layers

        else:
            layer.visible = layer.name in visible_layers


def get_layer_name(item_name: str, ordinal: int):
    if item_name == "НЕТ":
        return item_name
    return f"{item_name}_{ordinal}"



def generate_tile(json_data, guid, visible_layers):
    if guid is None:
        return

    psd = PSDImage.open('assets/tile_template.psd')

    update_visibility(psd, visible_layers)

    image = psd.composite(layer_filter=lambda layer: layer.name in visible_layers)

    Path(tiles_path).mkdir(parents=True, exist_ok=True)
    image_name = f"{guid}.png"
    image_local_path = os.path.join(tiles_path, image_name)
    image.save(image_local_path)
    if use_local_images:
        image_game_url = os.path.abspath(image_local_path)
    else:
        image_game_url = "https://raw.githubusercontent.com/EgoTheUndead/Edge-of-Discord/main/output/tiles/" + image_name

    target_object = tabletop_utils.get_object_by_guid(json_data, guid)
    target_object["CustomImage"]["ImageURL"] = image_game_url


def process_worksheet(json_data, worksheet):
    first_line = True
    for row in worksheet.rows:
        if first_line:
            first_line = False
            continue

        visible_layers = ["ЛАНДШАФТЫ", "МЕСТА", "ОБЪЕКТЫ", "СТОЛИЦЫ"]
        visible_zones = []
        guid = row[0].value
        # tile(zone) type and icon
        visible_zones.append(get_layer_name(row[2].value, 1))
        visible_layers.append(get_layer_name(row[3].value, 1))

        # tile type and icon
        visible_zones.append(get_layer_name(row[4].value, 2))
        visible_layers.append(get_layer_name(row[5].value, 2))

        # tile type and icon
        visible_zones.append(get_layer_name(row[6].value, 3))
        visible_layers.append(get_layer_name(row[7].value, 3))

        visible_layers.extend(visible_zones)

        if 'НЕТ' in visible_zones:
            visible_layers.extend(["ОСНОВА (МИНИ)"])
        else:
            visible_layers.extend(["ОСНОВА", "СЕКЦИИ"])

        generate_tile(json_data, guid, visible_layers)


def process_workbook(filename):
    workbook = openpyxl.load_workbook(filename)
    with open('game.json', encoding="utf8") as f:
        json_data = json.load(f)

    sheets_to_process = [
        "island_port_tiles",
        "island_tiles",
        "continent_tiles",
        "continent_port_tiles",
        "dungeons",
        "dungeons2",
        "dungeons3",
        "starting_tiles",
    ]

    for sheet_name in sheets_to_process:
        worksheet = workbook[sheet_name]
        process_worksheet(json_data, worksheet)

    tabletop_utils.write_json('game.json', json_data)
    print_layers()


if __name__ == "__main__":
    # process_file('csv_files/continent_port_tiles.csv')
    process_workbook("assets/tiles.xlsx")
