# XOR obfuscation tool

This is a XOR obfuscation tool that uses a 1-byte hexadecimal key to encrypt the contents of a file and save the result to a new file.

## Usage:
-i, --input: The name of the input file.

-o, --output: The name of the output file where the result will be saved.

-k, --key: A 1-byte hexadecimal key (e.g., 0xAF or AF).

## Optional argument:

-f, --format: Selects the output format for the ciphertext printed to the console. Options: python-array, raw, c-array.

## Example Command:
(Encrypts the file secret.txt using the key 0xAB and saves it as secret.bin. The ciphertext is printed to the console as a C array.)

python xortool.py --input secret.txt --output secret.bin --key 0xAB --format c-array

## Output Format Examples:
If the command above is run and secret.txt contains "Hello", the console output would look like this:

Python-array:
Ciphertext (python-array): array('B', [9, 36, 45, 45, 46, 75])

C-array:
unsigned char xored_shellcode[] = { 0x09, 0x24, 0x2d, 0x2d, 0x2e };


