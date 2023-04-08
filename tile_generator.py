import json
import csv
from psd_tools import PSDImage





def process_file():
    tile_table = {}

    with open('game_source.json', encoding="utf8") as f:
        data = json.load(f)

    with open('csv_files/continent_port_tiles.csv', mode='w', newline='') as f:
        reader= csv.reader(f)
        for row in reader:
            tile_table["guid"] = row[0]
            tile_table[1]["type"] = row[2]
            tile_table[1]["icon"] = row[3]
            tile_table[2]["type"] = row[4]
            tile_table[2]["icon"] = row[5]
            tile_table[3]["type"] = row[6]
            tile_table[3]["icon"] = row[7]

    psd = PSDImage.open('assets/tile_template.psd')
    layer = psd.layers['ГОРОД 2_2']
    image = layer.as_PIL()
    # Save the image to a file
    image.save('layer.png')


if __name__ == "__main__":
    process_file()
