#!/bin/python3

"""Xor Obfuscation-tool

This tool obfuscates files using a single-byte XOR operation. It supports
multiple output formats.
"""

import sys
import argparse
from pathlib import Path
import pyfiglet

# Print banner with pyfiglet
result = pyfiglet.figlet_format("XOR OBFUSCATOR", font="small")
print(result)

def main():
    """
    Parses command-line arguments and performs XOR obfuscation on a file.
    Command-line Arguments:
    """
    parser = argparse.ArgumentParser(description ="A XOR obfuscation tool.")
    # Required arguments
    parser.add_argument('--input','-i', required=True,dest='input_file',
    help='The name of the input file.')
    parser.add_argument('--output','-o', required=True,dest='output_file',
    help='The name of the output file.')
    parser.add_argument('--key','-k', required=True,dest='input_key',
    help='1 byte hexadecimal string.')
    # Optional argument
    parser.add_argument('--format','-f', choices=["python", "raw", "c-array"],dest='input_format',
    help='Choose a format to output the ciphertext. Options: python, raw, c-array. [Optional]')
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

    # Converting the list to a bytes object
    ciphertext = bytes(ciphertext_list)

    formatinput = args.input_format
    # Prints a Python list
    if formatinput == "python":
        formatted = ", ".join([f"0x{b:02x}" for b in ciphertext])
        print(f"Ciphertext (python-list): [{formatted}]")
    # Prints raw bytes
    elif formatinput == "raw":
        print(f"Ciphertext (raw bytes): {ciphertext!r}")
    # Prints a c-array
    elif formatinput == "c-array":
        c_array = ", ".join([f"0x{b:02x}" for b in ciphertext])
        print("C-ARRAY:\n")
        print(f"unsigned char xored_shellcode[] = {{ {c_array} }};")

    # Saving the output to a file
    outputfile = args.output_file
    outputpath = Path.cwd() / outputfile
    outputpath.parent.mkdir(parents=True, exist_ok=True)
    with open(outputpath, "wb") as file:
        file.write(ciphertext)
    print(f"\nSuccessfully saved file as {outputpath}")

if __name__ == "__main__":
    main()

