#!/usr/bin/env python3

'''
This script is for reading and writing files of a custom data format. It is for
storing a long list of numbers.

The Data Format:

WIDTH : 1 byte, LENGTH : WIDTH bytes, ARRAY : WIDTH * LENGTH bytes

* Anything after the array would be hidden/unused.

* Big endian encoding

'''

from format_a import *


def error (*args, **kwargs):
    print(*args, **kwargs, file=sys.stderr)


def repr_num (num):
    global args

    base = args.base

    if base == 10:
        return str(num)

    if base == 16:
        s = hex(num)
        if args.hexup:
            s = s.upper()
    elif base == 8:
        s = oct(num)
    elif base == 2:
        s = bin(num)

    if not args.prefix:
        s = s[2:]
    return s


# Command-line script
if __name__ == "__main__":
    import sys, argparse

    # Global
    flag = "store_true"

    p = argparse.ArgumentParser(epilog='If -d or -c is supplied, the given file will be decoded into stdout, otherwise stdin will be scanned for numbers separated by spaces and written to the given file.')
    p.add_argument("file", help="the name of the file to encode or decode")
    g1 = p.add_mutually_exclusive_group()
    g1.add_argument("-c", dest="count", action=flag, help="count the number of numbers in the input file")
    g1.add_argument("-d", dest="decode", action=flag, help="decode file as input")
    p.add_argument("-u", dest="unsigned", action=flag, help="treat numbers as unsigned")
    p.add_argument("-w", dest="width", type=int, help="specify the actual byte-width of each number when encoding (default: automatic based on the data), or the maximum byte-width when decoding (default: 10 bytes)")
    g2 = p.add_mutually_exclusive_group()
    g2.add_argument("-X", dest="hexup", action=flag, help="hexadecimal number format (upper case)")
    g2.add_argument("-b", dest="bin", action=flag, help="binary number format")
    g2.add_argument("-o", dest="oct", action=flag, help="octal number format")
    g2.add_argument("-x", dest="hex", action=flag, help="hexadecimal number format (lower case)")
    p.add_argument("-p", dest="prefix", action=flag, help="prefix numbers with the base prefix (not base 10)")
    args = p.parse_args()

    signed = not args.unsigned

    # Byte width sanity check
    if args.width is not None and args.width <= 0:
        error("byte width is 0 or below")
        sys.exit(-1)

    # Number base
    args.base = 10
    if args.hex or args.hexup:
        args.base = 16
    elif args.oct:
        args.base = 8
    elif args.bin:
        args.base = 2

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
        nums = [x.strip() for x in data.split(" ")]
        nums = [int(x) for x in nums if x]

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
