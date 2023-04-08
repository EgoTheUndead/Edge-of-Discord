
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