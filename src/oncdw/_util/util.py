def _get_val_from_keys(data: dict, keys: list[str], raise_error=True, default=None):
    """
    Get the value from the dictionary by checking the keys in order.
    If a key is not found, it will either raise a KeyError, or return None.
    """
    for key in keys:
        if key in data:
            return data[key]

    if raise_error:
        raise KeyError(f"None of the keys {keys} found in the dictionary {data}.")
    else:
        return default
