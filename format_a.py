#!/usr/bin/env python3

'''
This script is for reading and writing files of a custom data format. It is for
storing a long list of numbers.

The Data Format:

WIDTH : 1 byte, LENGTH : WIDTH bytes, ARRAY : WIDTH * LENGTH bytes

* Anything after the array would be hidden/unused.

* Big endian encoding

'''

from math import log


def byte_length (bit_length):
    print('bits', bit_length)
    return (-8 & (bit_length + 7)) >> 3


def auto_width (numbers):
    return byte_length(max(x.bit_length() for x in numbers))


def write_one (file, num, width=1, signed=True):
    '''Write one number of a certain byte width to a file'''
    try:
        b = num.to_bytes(width, byteorder='big', signed=signed)
        return file.write(b)
    except OverflowError as e:
        # Store error data
        e.x = num
        raise e


def read_one (file, width=1, signed=True):
    '''Read one number of a certain byte width from a file'''
    b = file.read(width)
    return int.from_bytes(b, byteorder='big', signed=signed)


def read_file (file, max_width=None, signed=True):
    '''Read a file using the file format. Returns a tuple of (width, length, array)'''

    width, length = count_file(file, max_width)
    array = [read_one(file, width, signed) for i in range(length)]

    return width, length, array


def count_file (file, max_width=None):
    width = read_one(file)

    if not width:
        raise ValueError('byte width in file is zero')

    if max_width is not None and width > max_width:
        raise ValueError('maximum byte width exceeded in file')

    length = read_one(file, width, signed=False)
    return width, length


def write_file (file, array, width, signed=True):
    '''Write an array of numbers to a file of this format'''
    write_one(file, width)
    write_one(file, len(array), width, signed=False)
    for x in array:
        write_one(file, x, width, signed)


def error (*args, **kwargs):
    print(*args, **kwargs, file=sys.stderr)

# Global
base = 10
prefixp = False

def repr_num (num):
    if base == 10:
        return str(num)

    if base == 16:
        s = hex(num)
    elif base == 8:
        s = oct(num)
    elif base == 2:
        s = bin(num)

    if not prefixp:
        s = s[2:]
    return s


# Command-line script
if __name__ == "__main__":
    import sys, argparse

    # Global
    flag = "store_true"

    p = argparse.ArgumentParser()
    p.add_argument("file", help="the name of the file to encode or decode")
    g1 = p.add_mutually_exclusive_group()
    g1.add_argument("-d", dest="decode", action=flag, help="decode file as input")
    g1.add_argument("-c", dest="count", action=flag, help="count the number of numbers in the input file")
    p.add_argument("-w", dest="width", type=int, help="specify the actual byte-width of each number when encoding (default: automatic based on the data), or the maximum byte-width when decoding (default: 10 bytes)")
    p.add_argument("-u", dest="unsigned", action=flag, help="treat numbers as unsigned")
    p.add_argument("-p", dest="prefix", action=flag, help="prefix numbers with the base prefix")
    g = p.add_mutually_exclusive_group()
    g.add_argument("-b", dest="bin", action=flag, help="use binary number format")
    g.add_argument("-o", dest="oct", action=flag, help="use octal number format")
    g.add_argument("-x", dest="hex", action=flag, help="use hexadecimal number format")
    args = p.parse_args()

    signed = not args.unsigned
    prefixp = args.prefix

    # Byte width sanity check
    if args.width is not None and args.width <= 0:
        error("byte width is 0 or below")
        sys.exit(-1)

    # Number base
    if args.hex:
        base = 16
    elif args.oct:
        base = 8
    elif args.bin:
        base = 2

    # Now either encode or decode
    if args.decode:
        # Read a file in
        if args.width is None:
            # Default byte-width limit when reading
            args.width = 10

        try:
            with open(args.file, "rb") as file:
                width, length, nums = read_file(file, args.width, signed) 
            print(" ".join(repr_num(x) for x in nums))
            sys.exit(0)
        except Exception as e:
            error(e)
            sys.exit(1)
    elif args.count:
        # Count the file data length
        with open(args.file, "rb") as file:
            width, length = count_file(file, args.width)
        print(repr_num(length))
        sys.exit(0)
    else:
        # Write a file out, with input data from stdin
        data = sys.stdin.read()
        nums = [int(x.strip()) for x in data.split(" ")]

        if args.width is None:
            # Default byte-width limit when writing
            args.width = auto_width(nums)
            print('auto width', args.width)

        try:
            with open(args.file, "wb") as file:
                write_file(file, nums, args.width, signed)
            sys.exit(0)
        except OverflowError as e:
            error("Overflow error: integer '%d' is too big to store in a byte width of %d" % (e.x, args.width))
            sys.exit(1)


'''
Copyright (c) 2021 Izak Nathanael Halseide
'''
