"""Exports search function"""
from json import loads


def search(key, value, attribute):
    """Recursively searches a dictionary for a given attribute."""
    if key == attribute:
        return value
    # Attempt JSON parse
    try:
        value = loads(value)
    except (ValueError, TypeError):
        pass
    if isinstance(value, dict):
        dict_keys = value.keys()
        for dict_key in dict_keys:
            next_value = search(dict_key, value[dict_key], attribute)
            if next_value is not None:
                return next_value
    return None

def clean_gnome_id(gnome_id):
    no_hash = gnome_id[1:].lstrip('0')
    if int(no_hash) < 10:
        gnome_id = '#000' + no_hash
    elif int(no_hash) < 100:
        gnome_id = '#00' + no_hash
    elif int(no_hash) < 1000:
        gnome_id = '#0' + no_hash
    return gnome_id
