# Format A

This is a data format that I came up with on my own (that definitely has been thought of before).

C = 1-byte number that tells how many bytes each number is
N = C bytes that tell the length of the data
Data[0...N] = N\*C bytes that represent N numbers, each of size C

    struct A {
    	char C;
    	char N[<C>];
    	char Data[N][<C>];
    }

## Command Line Tool

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

