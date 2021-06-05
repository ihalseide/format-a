# Format A

This is a binary data format that I came up with on my own (that definitely has been thought of before). It's good for storing a large amount of numbers, uncompressed (although you could always gzip the binary files). The numbers will stay in the order that you put them in.

Advantages: it's simple.

Disadvantages: every number takes the same number of bytes to encode, and, for example, if you choose too large of a byte width, the file will be larger than necessary.

Data layout:

1. a byte, called C, indicating how many bytes every single subsequent number is encoded within
2. an unsigned number, called N, indicating how many numbers are in the number list
3. an ordered list of N numbers, where each number in the list is represented with C bytes

All numbers after the first byte are big-endian. The total size of the structure is `C * (N + 1) + 1` bytes. There is an option as to whether the numbers in the list are signed or unsigned.

## Command Line Usage

Run it with `$ python a.py`.

    usage: a.py [-h] [-c | -d] [-u] [-w WIDTH] [-X | -b | -o | -x] [-p] file
    
    positional arguments:
      file        the name of the file to encode or decode
    
    optional arguments:
      -h, --help  show this help message and exit
      -c          count the number of numbers in the input file
      -d          decode file as input
      -u          treat numbers as unsigned
      -w WIDTH    specify the actual byte-width of each number when encoding (default: automatic based on the data), or the maximum byte-width when decoding (default: 10
                  bytes)
      -X          hexadecimal number format (upper case)
      -b          binary number format
      -o          octal number format
      -x          hexadecimal number format (lower case)
      -p          prefix numbers with the base prefix (not base 10)
    
    If -d or -c is supplied, the given file will be decoded into stdout, otherwise stdin will be scanned for numbers separated by spaces and written to the given file.

Examples


## Library Usage

Download "format\_a.py" and slap it into your project files. Wherever you need it, just `import format_a`.

## License

This project is licensed under the MIT License. See the file "LICENSE.txt" for more information.

