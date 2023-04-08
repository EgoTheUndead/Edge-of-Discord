import json
import csv
import os
from pathlib import Path

import psd_tools.api.layers
from psd_tools import PSDImage

tiles_path = "output/tiles"


def update_visibility(psd: PSDImage, visible_layers: list[str]):
    for layer in psd:
        if isinstance(layer, psd_tools.api.layers.Group):
            layer.visible = True
            for sublayer in layer:
                sublayer.visible = sublayer.name in visible_layers

        else:
            layer.visible = layer.name in visible_layers


def get_layer_name(item_name: str, ordinal: int):
    return f"{item_name.upper()}_{ordinal}"


def process_file():
    tile_table = {}
    psd = PSDImage.open('assets/tile_template.psd')

    with open('game_source.json', encoding="utf8") as f:
        data = json.load(f)

    with open('csv_files/continent_port_tiles.csv', mode='r', encoding="utf8") as f:
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

            image = psd.composite(layer_filter=lambda layer : layer.name in visible_layers)

            Path(tiles_path).mkdir(parents=True, exist_ok=True)
            image.save(os.path.join(tiles_path, f"{guid}.png"))


if __name__ == "__main__":
    process_file()
