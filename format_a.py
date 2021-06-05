def byte_length (bit_length:int):
    return (-8 & (bit_length + 7)) >> 3


def auto_width (numbers:list):
    return byte_length(max(x.bit_length() for x in numbers))


def write_one (file, num, width:int=1, signed:bool=True):
    '''Write one number of a certain byte width to a file'''
    try:
        b = num.to_bytes(width, byteorder='big', signed=signed)
        return file.write(b)
    except OverflowError as e:
        # Store error data
        e.x = num
        raise e


def read_one (file, width:int=1, signed:bool=True):
    '''Read one number of a certain byte width from a file'''
    b = file.read(width)
    return int.from_bytes(b, byteorder='big', signed=signed)


def read_file (file, max_width:int=None, signed:bool=True):
    '''Read a file using the file format. Returns a tuple of (width, length, array)'''

    width, length = count_file(file, max_width)
    array = [read_one(file, width, signed) for i in range(length)]

    return width, length, array


def count_file (file, max_width:int=None):
    width = read_one(file)

    if not width:
        raise ValueError('byte width in file is zero')

    if max_width is not None and width > max_width:
        raise ValueError('maximum byte width exceeded in file')

    length = read_one(file, width, signed=False)
    return width, length


def write_file (file, array, width:int, signed:bool=True):
    '''Write an array of numbers to a file of this format'''
    write_one(file, width)
    write_one(file, len(array), width, signed=False)
    for x in array:
        write_one(file, x, width, signed)

