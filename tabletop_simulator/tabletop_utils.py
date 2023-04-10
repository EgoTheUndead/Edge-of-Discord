import json
import re

kCustomTokenName = "Custom_Token"
kTags = "Tags"
kName = "Name"


def has_tags(item, tags: list[str]):
    if kTags not in item:
        return False

    return all(tag in item[kTags] for tag in tags)


def is_hex_tile(item, tag: str):
    if item[kName] != kCustomTokenName:
        return False

    return has_tags(item, [tag])


def get_object_by_guid(tabletop_json, guid):
    for item in tabletop_json["ObjectStates"]:
        if item["GUID"] == guid:
            return item

        if 'States' in item:
            for index, state in item["States"].items():
                if state["GUID"] == guid:
                    return state

    raise Exception(f"Object with guid {guid} not found")

def write_json(filename, data):
    with open(filename, mode='w', encoding="utf8") as f:
        json_string = json.dumps(data, indent=2, ensure_ascii=False)
        json_string = re.sub(r"(\d+\.\d+)e(-?\d\d)", r"\1E\2", json_string)
        f.write(json_string)