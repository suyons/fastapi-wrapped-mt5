from typing import Optional
import MetaTrader5 as mt5
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


def resolve_filling(symbol_info, requested: Optional[int]) -> int:
    """Return a filling type that the symbol supports.

    filling_mode is a bitmask: bit k is set when ORDER_TYPE_FILLING == k is supported.
    ORDER_FILLING_FOK=0 → bit 0 (value 1), IOC=1 → bit 1 (value 2), RETURN=2 → bit 2 (value 4).
    """
    filling_mode = symbol_info.filling_mode
    fok_ok = bool(filling_mode & (1 << mt5.ORDER_FILLING_FOK))
    ioc_ok = bool(filling_mode & (1 << mt5.ORDER_FILLING_IOC))
    ret_ok = bool(filling_mode & (1 << mt5.ORDER_FILLING_RETURN))

    if requested is not None:
        req = int(requested)
        if req == mt5.ORDER_FILLING_FOK and fok_ok:
            return mt5.ORDER_FILLING_FOK
        if req == mt5.ORDER_FILLING_IOC and ioc_ok:
            return mt5.ORDER_FILLING_IOC
        if req == mt5.ORDER_FILLING_RETURN and ret_ok:
            return mt5.ORDER_FILLING_RETURN

    if ioc_ok:
        return mt5.ORDER_FILLING_IOC
    if fok_ok:
        return mt5.ORDER_FILLING_FOK
    return mt5.ORDER_FILLING_RETURN
