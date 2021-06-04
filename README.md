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
