import numpy as np


def structured_array_to_list(array: np.ndarray):
    if array is None:
        return None

    records = []
    for record in array:
        row = {}
        for name in array.dtype.names:
            value = record[name]
            if hasattr(value, "item"):
                row[name] = value.item()
            else:
                row[name] = value
        records.append(row)
    return records
