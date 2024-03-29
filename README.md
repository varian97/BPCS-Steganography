# BPCS-Steganography
Steganography using BPCS

# Requirements

1. Install Python
2. Install Python Dependencies

```
pip install numpy opencv-python
```
# How to Run

## Embedding

```
python stegano.py [original_image] [message_location] [threshold] -k [key] -r
```

```
-k : key for encryption (optional, default: not using key or not encrypted message)
-r : using random or not (optional, default: not random or sequential)
```

## Extraction

```
python stegano.py -e [image path] [location to store message] [threshold] -k [kunci] -r
```

```
-e: required for extraction
-k: key for decrytipn (optional, default: not using key)
-r: using random or not to read message (optional, default: read sequential)
```

# About

Created by:
1. Varian Caesar - 13514041
2. Bervianto Leo P - 13514047
3. M. Reza Ramadhan - 13514107

# License
```
MIT License

Copyright (c) 2018 Varian Caesar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
