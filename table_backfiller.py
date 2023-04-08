import json
import csv
import requests




def download_image(url, filename):
    response = requests.get(url)

    # Open a file in binary mode
    with open(filename, mode='wb') as f:
        # Write the content of the response (i.e. the image) to the file
        f.write(response.content)

def has_tags(item, tags: list[str]):
    if "Tags" not in item:
        return False

    return all(tag in item["Tags"] for tag in tags)


def is_hex_tile(item, tag: str):
    if item["Name"] != "Custom_Token":
        return False

    return has_tags(item, [tag])

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
    with open('game_source.json', encoding="utf8") as f:
        data = json.load(f)
    continent_tiles = []
    continent_port_tiles = []
    island_tiles = []
    island_port_tiles = []

    for item in data["ObjectStates"]:
        if is_hex_tile(item, "continent"):
            append_tile_record(continent_tiles,item)
        if is_hex_tile(item,"continent_port"):
            append_tile_record(continent_port_tiles,item)
        if is_hex_tile(item, "island"):
            append_tile_record(island_tiles, item)
        if is_hex_tile(item, "island_port"):
            append_tile_record(island_port_tiles, item)

    write_csv('csv_files/continent_tiles.csv', continent_tiles)
    write_csv('csv_files/continent_port_tiles.csv', continent_port_tiles)
    write_csv('csv_files/island_tiles.csv', island_tiles)
    write_csv('csv_files/island_port_tiles.csv', island_port_tiles)


if __name__ == "__main__":
    process_file()
