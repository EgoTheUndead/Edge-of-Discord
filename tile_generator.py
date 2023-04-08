import json
import csv
import os
from pathlib import Path
import re

import psd_tools.api.layers
from psd_tools import PSDImage

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
    return f"{item_name.upper()}_{ordinal}"


def write_json(filename, data):
    with open(filename, mode='w', encoding="utf8") as f:
        json_string = json.dumps(data, indent=2, ensure_ascii=False)
        json_string = re.sub(r"(\d+\.\d+)e(-?\d\d)", r"\1E\2", json_string)
        f.write(json_string)

def process_file(csv_path):
    psd = PSDImage.open('assets/tile_template.psd')

    with open('game.json', encoding="utf8") as f:
        data = json.load(f)

    with open(csv_path, mode='r', encoding="utf8") as f:
        reader = csv.reader(f)
        first_line = True
        for row in reader:
            if first_line:
                first_line = False
                continue

            guid = row[0]
            visible_layers = ["ОСНОВА", "СЕКЦИИ", "ЛАНДШАФТЫ", "МЕСТА", "ОБЪЕКТЫ", "СТОЛИЦЫ"]
            # tile type and icon
            visible_layers.append(get_layer_name(row[2], 1))
            visible_layers.append(get_layer_name(row[3], 1))

            # tile type and icon
            visible_layers.append(get_layer_name(row[4], 2))
            visible_layers.append(get_layer_name(row[5], 2))

            # tile type and icon
            visible_layers.append(get_layer_name(row[6], 3))
            visible_layers.append(get_layer_name(row[7], 3))

            update_visibility(psd, visible_layers)

            def should_output_layer(layer):
                print(f"{layer.name}")

            image = psd.composite(layer_filter=lambda layer: layer.name in visible_layers)

            Path(tiles_path).mkdir(parents=True, exist_ok=True)
            image_name = f"{guid}.png"
            image_local_path = os.path.join(tiles_path, image_name)

            image.save(image_local_path)

            target_object = tabletop_utils.get_object_by_guid(data, guid)

            if use_local_images:
                image_game_url = os.path.abspath(image_local_path)
            else:
                image_game_url = "https://raw.githubusercontent.com/EgoTheUndead/Edge-of-Discord/main/output/tiles/"+image_name

            target_object["CustomImage"]["ImageURL"] = image_game_url

            write_json('game.json', data)

    print_layers()


if __name__ == "__main__":
    process_file('csv_files/continent_port_tiles.csv')
