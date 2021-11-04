def search(key, value, attribute):
    if key == attribute:
        return value
    else:
        if type(value) is dict:
            keys = value.keys()
            for key in keys:
                next = search(key, value[key], attribute)
                if next is not None:
                    return next
                else:
                    continue
    return None