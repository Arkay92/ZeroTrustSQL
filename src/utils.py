def str_to_int(s):
    return int.from_bytes(s.encode('utf-8'), byteorder='big')

def int_to_str(i):
    if isinstance(i, int):
        return str(i)
    try:
        return i.to_bytes((i.bit_length() + 7) // 8, byteorder='big').decode('latin1')
    except (UnicodeDecodeError, ValueError):
        return str(i)
