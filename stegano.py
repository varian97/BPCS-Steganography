#!/usr/bin/python3
import argparse

def create_arguments():
    """Create command line argument for this program.
    """
    
    parser = argparse.ArgumentParser(
        description='A BPCS-based algorithm Steganography Program'
    )
    parser.add_argument("original_image", help="The original image path that you will put a hidden message")
    parser.add_argument("secret_message", help="Your secret message file path. The message must be stored inside a file.")
    parser.add_argument("bpcs_threshold", help="alpha Treshold in BPCS algorithm")
    parser.add_argument("-e", "--extract", help="Extract the secret message from a stegano image. \n If this option is used, <original_image> argument is treated as <stegano_image> and <secret_message> will become the stored secret message path", action="store_true")
    parser.add_argument("-k", "--key", help="Key to encrypt message using Vigenere256bit")
    parser.add_argument("-r", "--randomize", help="Randomize the message placement inside the bitplane", action="store_true")
    parser.add_argument("-c", "--cgc", help="should the bitplane use CGC instead of PBC", action="store_true")
    parser.add_argument("-o", "--output", help="Stegano Image output. The image that has a hidden message stored inside.")

    return parser.parse_args()

if __name__ == '__main__':

    args = create_arguments()
    if (args.randomize):
        print("this should randomize")
    if (args.key):
        print("key:", args.key)
    print(args.original_image)
