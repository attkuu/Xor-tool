#!/bin/python3

"""Xor Obfuscation-tool

This tool obfuscates files using a single-byte XOR operation. It supports
multiple output formats including raw hex, byte strings, and C-style arrays.
"""

import sys
import argparse
from pathlib import Path

def main():
    """
    Parses command-line arguments and performs XOR obfuscation on a file.
    Command-line Arguments:
        --input, -i: Path to the file to be obfuscated.
        --output, -o: Path where the obfuscated file will be saved.
        --key, -k: A 1-byte hex string (e.g., '0xAA' or 'FF') used as the XOR key.
        --format, -f: Optional output display format (hex, bytes, or c-array).
    """
    parser = argparse.ArgumentParser(description ="A XOR obfuscation tool.")
    parser.add_argument(
        '--input',
        '-i',
        type=str,
        required=True,
        dest='input_file',
        help='The name of the input file.'
    )
    parser.add_argument(
        '--output',
        '-o',
        type=str,
        required=True,
        dest='output_file',
        help='The name of the output file.'
    )
    parser.add_argument(
        '--key',
        '-k',
        type=str,
        required=True,
        dest='input_key',
        help='1 byte hexadecimal string.'
    )
    parser.add_argument(
        '--format',
        '-f',
        type=str,
        choices=["hex", "bytes", "c-array"],
        dest='input_format',
        help='Choose a format to output the ciphertext. Options: hex, bytes, c-array. [Optional]'
    )
    # Reading input file
    args = parser.parse_args()
    inputfile = args.input_file
    try:
        inputpath = Path.cwd() / inputfile
        with open(inputpath, "rb") as file:
            plaintext = file.read()
    except FileNotFoundError:
        print(f"Error, the file {inputpath} was not found!")
        sys.exit(1)
    keyinput = args.input_key
    # Checking that the key input is a valid hexadecimal string
    if keyinput.startswith("0x"):
        hexainput = keyinput[2:]
    else:
        hexainput = keyinput
    try:
        key = bytes.fromhex(hexainput)
        if len(key) != 1:
            raise ValueError
    except ValueError:
        print(f"Error: {keyinput} is not a valid one byte hexadecimal string.")
        sys.exit(1)

    key_byte = key[0]
    ciphertext_list = []
    # Obfuscating with XOR
    for byte in plaintext:
        ciphertext_list.append(byte ^ key_byte)

    ciphertext = bytes(ciphertext_list)

    # Printing output
    formatinput = args.input_format
    if formatinput == "hex":
        print(f"Ciphertext (hex): {ciphertext.hex()}")
    elif formatinput == "bytes":
        print(f"Ciphertext (bytes): {ciphertext!r}")
    elif formatinput == "c-array":
        hex_string = ciphertext.hex()
        c_array = ""
        for i in range(0, len(hex_string), 2):
            c_array += f"0x{hex_string[i:i+2]}, "
        c_array = c_array.rstrip(', ')
        print(f"C Array = {{ {c_array} }};")

    # Saving the output to a file
    outputfile = args.output_file
    outputpath = Path.cwd() / outputfile
    outputpath.parent.mkdir(parents=True, exist_ok=True)
    with open(outputpath, "wb") as file:
        file.write(ciphertext)
    print(f"Successfully saved file as {outputpath}")

if __name__ == "__main__":
    main()
