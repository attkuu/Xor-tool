#!/bin/python3

"""Xor Obfuscation-tool

This tool obfuscates files using a single-byte XOR operation. It supports
multiple output formats.
"""

import sys
import argparse
from pathlib import Path
import array
import pyfiglet

def print_banner():
    """
    Prints an ASCII banner using pyfiglet.
    """
    banner = pyfiglet.figlet_format("XOR OBFUSCATOR", font="small")
    print(banner)

def xor_operation(key, plain):
    """
    Performs a single-byte XOR operation on the plaintext.

    Returns the XORed ciphertext.
    """
    ciphertext_list = []
    # Obfuscating with XOR
    for byte in plain:
        ciphertext_list.append(byte ^ key)

    ciphertext = bytes(ciphertext_list)
    return ciphertext

def print_output(formatinput, ciphertext):
    """
    Prints the ciphertext to the console based on the chosen format.

    """
    # Prints a Python array
    if formatinput == "python":
        python_array =  array.array("B", ciphertext)
        print(f"Ciphertext (python-array): {python_array}")
    # Prints raw bytes
    elif formatinput == "raw":
        print(f"Ciphertext (raw bytes): {ciphertext!r}")
    # Prints a c-array
    elif formatinput == "c-array":
        c_array = ", ".join([f"0x{b:02x}" for b in ciphertext])
        print("C-ARRAY:\n")
        print(f"unsigned char xored_shellcode[] = {{ {c_array} }};")

def main():
    """
    Handles the command-line arguments and manages the file input and output.

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
    parser.add_argument('--format','-f', choices=["python", "raw", "c-array"],dest='output_format',
    help='Choose a format to output the ciphertext. Options: python-array, raw, c-array. [Optional]')
    args = parser.parse_args()

    # Printing the banner
    print_banner()

    # Reading input file
    inputfile = args.input_file
    try:
        inputpath = Path(inputfile)
        with open(inputpath, "rb") as file:
            plaintext = file.read()
    except FileNotFoundError:
        print(f"ERROR: The file {inputpath} was not found!")
        sys.exit(1)

    keyinput = args.input_key
    # Checking that the key input is a valid hexadecimal string
    if keyinput.startswith("0x"):
        hexinput = keyinput[2:]
    else:
        hexinput = keyinput
    try:
        # Converts the hex string to a bytes object
        key = bytes.fromhex(hexinput)
        if len(key) != 1:
            raise ValueError
    except ValueError:
        print(f"ERROR: {keyinput} is not a valid one byte hexadecimal string.")
        sys.exit(1)

    # Extract the single byte from the key object
    key_byte = key[0]

    # Calling the Xor function
    ciphertext = xor_operation(key_byte, plaintext)

    # Calling the print_output function if user chooses so.
    if args.output_format:
        print_output(args.output_format, ciphertext)

    # Saving the output to a file
    outputfile = args.output_file
    outputpath = Path(outputfile)
    outputpath.parent.mkdir(parents=True, exist_ok=True)
    with open(outputpath, "wb") as file:
        file.write(ciphertext)
    print(f"\nSuccessfully saved file as {outputpath}")

if __name__ == "__main__":
    main()


