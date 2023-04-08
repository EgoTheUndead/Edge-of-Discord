import json
import csv
import requests
from pathlib import Path

from tabletop_simulator import tabletop_utils


def download_image(url, filename):
    response = requests.get(url)

    # Open a file in binary mode
    with open(filename, mode='wb') as f:
        # Write the content of the response (i.e. the image) to the file
        f.write(response.content)

def append_tile_record(tiles_list, item):
    guid = item["GUID"]
    remote_url = item["CustomImage"]["ImageURL"]
    # local_url = f"tile_images/{guid}.jpg"

    tile = [
        guid,
        remote_url
    ]
    tiles_list.append(tile)

def write_csv(filename, tiles):
    with open(filename, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Guid', 'Remote URL'])
        writer.writerows(tiles)

def process_file():
    with open('game.json', encoding="utf8") as f:
        data = json.load(f)

    tile_groups = [
        {"tag":"continent", "file":"_continent_tiles.csv", "tiles":[]},
        {"tag": "continent_port", "file": "_continent_port_tiles.csv", "tiles":[]},
        {"tag": "island", "file": "_island_tiles.csv", "tiles":[]},
        {"tag": "island_port", "file": "_island_port_tiles.csv", "tiles":[]},

        {"tag": "dungeon", "file": "_dungeons.csv", "tiles": []},
        {"tag": "dungeon2", "file": "_dungeons2.csv", "tiles": []},
        {"tag": "dungeon3", "file": "_dungeons3.csv", "tiles": []}
    ]

    for item in data["ObjectStates"]:
        for tile_group in tile_groups:
            if tabletop_utils.is_hex_tile(item, tile_group["tag"]):
                append_tile_record(tile_group["tiles"], item)

    csv_files_folder = "output/csv_files/"
    Path("output/csv_files/").mkdir(parents=True, exist_ok=True)
    for tile_group in tile_groups:
        write_csv(csv_files_folder + tile_group["file"], tile_group["tiles"])



if __name__ == "__main__":
    process_file()
