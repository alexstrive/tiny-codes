"""
In many applications—such as search engines or
compressed indexes—we need to represent lists of integers (e.g., document IDs or
gap values between them). These integers often follow a skewed distribution
(many small values, few large ones), so we want a prefix-free,
variable-length encoding scheme that favors small numbers.

# Gamma encoding

Gamma encoding is one such method that achieves this.

Gamma encoding represents an integer x > 0 using two parts:

1. Unary representation of the length of x in binary minus 1 (called the length prefix)
2. Binary representation of x without the leading 1 (called the offset)


Step-by-step encoding for x:
1. Let N = floor(log2(x)) + 1 — the number of bits in the binary representation of x.
2. Write N - 1 in unary (i.e., N-1 zeros followed by a one).
3. Write the lower N - 1 bits of x (i.e., drop the leading 1 of x’s binary form).

Final gamma code = [unary(N-1)][binary(x) without leading 1]

Example 1

Let's encode the number 10:
1. Binary representation of 10 = 1010
2. N = 4 -> N-1 = 3 -> unary(N-1) = 0001
3. Offset: remove leading from 1010 010

Gamma code = 0001010

Example 2
Let's encode the number 5:
1. Binary representation of 5: 101 -> N=3
2. Unary part 00 followed by 1 -> 001
3. Offset = binary without leading 1 -> 01

Gamma code = 00101

# Gamma decoding

1. Count the number of leading zeros before the first 1 -> call it `L`
2. Read the next L bits after the 1 that's the offset
3. Reconstruct x = 2^L+offset

Example

Decode 00101
1. First 2 zeros -> L=2
2. Next 1 (marker), then L=2 bits 01
3. So x=2^2+1=4+1=5

Decoded value = 5

# Properties
1. Prefix-free – no code is a prefix of another
2. Efficient for small numbers (common in gap encoding)
3. Used in compressed inverted indexes
4. Gamma Code Length = 2*log_2(x) + 1 -- grows logarithmically with the value of x
5. Not efficient for large numbers: fixed-length or Golomb/Rice codes might be better
6. Cannot encode zero: only positive ints `x > 0`

"""


def gamma_encode_number(n: int) -> str:
    """Encodes a single positive integer using Elias gamma coding."""

    if n <= 0:
        raise ValueError("Gamma encoding is only defined for positive integers")

    # get binary repr without '0b'
    binary = bin(n)[2:]

    # remove leading '1'
    offset = binary[1:]

    # number of offset bits
    length = len(binary) - 1

    # unary prefix
    prefix = "0" * length + "1"

    return prefix + offset


def gamma_encode_list(nums: list[int]) -> str:
    """Encodes a list of positive integers."""

    return "".join(gamma_encode_number(n) for n in nums)


def gamma_decode(stream: str) -> list[int]:
    """Decodes a gamma-encoded bit string into a list of integers."""

    i = 0
    decoded = []

    while i < len(stream):
        # Count leading zeros (unary length prefix)
        zeros = 0
        while i < len(stream) and stream[i] == "0":
            zeros += 1
            i += 1

        if i >= len(stream):
            raise ValueError("Malformed gamma stream (prefix cutoff)")

        i += 1

        # Read next 'zeros' bits as offset
        if i + zeros > len(stream):
            raise ValueError("Malformed gamma stream (offset cutoff)")

        offset = stream[i : i + zeros]
        i += zeros

        # Reconstruct the original number
        binary = "1" + offset
        decoded.append(int(binary, 2))

    return decoded
