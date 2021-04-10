#!/usr/bin/env python3

'''
This script is for reading and writing files of a custom data format. It is for
storing a long list of numbers.

The Data Format:

WIDTH : 1 byte, LENGTH : WIDTH bytes, ARRAY : WIDTH * LENGTH bytes

* Anything after the array would be hidden/unused.

* Big endian encoding

'''


def write_one (file, num, width=1, signed=True):
    '''Write one number of a certain byte width to a file'''
    b = num.to_bytes(width, byteorder='big', signed=signed)
    return file.write(b)


def read_one (file, width=1, signed=True):
    '''Read one number of a certain byte width from a file'''
    b = file.read(width)
    return int.from_bytes(b, byteorder='big', signed=signed)


def read_file (file):
    '''Read a file using the file format. Returns a tuple of (width, length, array)'''
    width = read_one(file)
    assert width
    length = read_one(file, width, signed=False)
    array = [read_one(file, width) for i in range(length)]
    return width, length, array


def write_file (file, array, width):
    '''Write an array of numbers to a file of this format'''
    write_one(file, width)
    write_one(file, len(array), width, signed=False)
    for x in array:
        write_one(file, x, width)


if __name__ == '__main__':
    import sys, argparse

    p = argparse.ArgumentParser(epilog='Note: appending to the file data does not mean the file will be opened in append-only mode, and also the -o option cannot be present with -a or -p')
    p.add_argument('-i, --info', dest='info', action='store_true', help='print out human-readable file info (only when reading)')
    p.add_argument('file', help='the name of the file to read or write')
    p.add_argument('-o', dest='overwrite', type=str, help='write comma-separated numbers to the file')
    p.add_argument('-a', dest='append', type=str, help='append a comma-separated list numbers to the file')
    p.add_argument('-p', dest='prepend', type=str, help='prepend a comma-separated list numbers to the file')
    p.add_argument('-w', dest='width', default=1, type=int, help='specify the byte-width of each number when writing (default is 1)')
    args = p.parse_args()

    if args.overwrite:
        if args.append or args.prepend:
            print(sys.argv[0], 'error', 'writing to a file while also appending or prepending is not allowed', sep=': ', file=sys.stderr)

        # Take numbers from the -write argument
        with open(args.file, 'wb') as file:
            try:
                nums = [int(x.strip()) for x in args.overwrite.split(',')]
            except ValueError:
                print(sys.argv[0], 'error', 'the number list to write is formatted incorrectly', sep=': ', file=sys.stderr)
                sys.exit(-1)

            write_file(file, nums, args.width) 
    else:
        # Get file data
        with open(args.file, 'rb') as file:
            width, length, nums = read_file(file) 

        if args.append or args.prepend:
            error = False

            # Prepend the numbers passed to the -prepend argument
            if args.prepend:
                try:
                    nums = [int(x.strip()) for x in args.prepend.split(',')] + nums
                except ValueError:
                    error = True
                    print(sys.argv[0], 'error', 'the number list to prepend is formatted incorrectly', sep=': ', file=sys.stderr)

            # Append the numbers passed to the -append argument
            if args.append:
                try:
                    nums += [int(x.strip()) for x in args.append.split(',')]
                except ValueError:
                    error = True
                    print(sys.argv[0], 'error', 'the number list to append is formatted incorrectly', sep=': ', file=sys.stderr)

            if error:
                sys.exit(-1)

            with open(args.file, 'wb') as file:
                write_file(file, nums, max(width, args.width or 0))
        else:
            if args.info:
                # Read and print out file info
                print(width, 'byte(s) per number,')
                print(length, 'number(s) in total,')
                print('numbers:', end=' ')

            print(', '.join(str(x) for x in nums))


'''
Copyright (c) 2021 Izak Nathanael Halseide
'''
