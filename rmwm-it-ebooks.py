#!/usr/bin env python
# __author__ = 'ShadonSniper'
import os
import sys
import binascii
import argparse

hex_link_pat = "".join("0A 3C 3C 0A 2F 54 79 70 65 20 2F 41 6E 6E 6F 74 0A 2F 53 75 "
                       "62 74 79 70 65 20 2F 4C 69 6E 6B 0A 2F 52 65 63 74 20 5B 20 "
                       "32 31 30 20 31 38 2E 35 20 32 39 34 20 36 2E 35 20 5D 0A 2F "
                       "42 6F 72 64 65 72 20 5B 20 30 20 30 20 30 20 5D 0A 2F 41 20 "
                       "3C 3C 0A 2F 54 79 70 65 20 2F 41 63 74 69 6F 6E 0A 2F 53 20 "
                       "2F 55 52 49 0A 2F 55 52 49 20 28 68 74 74 70 3A 2F 2F 77 77 "
                       "77 2E 69 74 2D 65 62 6F 6F 6B 73 2E 69 6E 66 6F 2F 29 0A 3E "
                       "3E 0A 3E 3E".split())

hex_text_pat = "".join("0A 42 54 0A 31 20 30 20 30 20 31 20 30 20 30 20 54 6D 0A 28 "
                       "77 77 77 2E 69 74 2D 65 62 6F 6F 6B 73 2E 69 6E 66 6F 29 54 "
                       "6A 0A 45 54".split())


def remove_watermark(path):
    pdf_bin_data = ""
    if path.endswith(".pdf"):
        try:
            with open(path, "rb") as pdf_file:
                pdf_bin_data = pdf_file.read()
                pdf_bin_data = pdf_bin_data.replace(binascii.unhexlify(hex_link_pat), "")
                pdf_bin_data = pdf_bin_data.replace(binascii.unhexlify(hex_text_pat), "")
        except IOError:
            sys.stderr.write("Error in opening file.")
    else:
        raise ValueError("Format error: the file is not a PDF format.")
    return pdf_bin_data


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    requiredNamed = parser.add_argument_group('Mandatory arguments')
    requiredNamed.add_argument("-F", "--file", dest='filepath', action="store", help='Specify absolute path of pdf file')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    args = parser.parse_args()
    filepath = args.filepath
    if filepath is None:
        parser.print_help()
        exit(0)
    if os.path.exists(filepath) and os.path.isabs(filepath):
        newFile = 'new_' + os.path.split(filepath)[1]
        try:
            with open(newFile, 'wb') as f:
                f.write(remove_watermark(filepath))
                f.close()
                print 'Watermark removal done!'
        except IOError:
            sys.stderr.write("Problem when writing file.")
    else:
        raise ValueError("Invalid path or is not a file.")
