# Huffman Coding Implementation in Python

[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Python](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/)

For Introduction to Artificial Intelligence
by AI Group 2

- [Huffman Coding Implementation in Python](#huffman-coding-implementation-in-python)
  - [1. Introduction](#1-introduction)
  - [2. How the Code Works](#2-how-the-code-works)
  - [3. Requirements](#3-requirements)
  - [4. How to Run](#4-how-to-run)
    - [Verbose Mode](#verbose-mode)
    - [GUI Mode](#gui-mode)
  - [5. Example Output](#5-example-output)
  - [6. Features](#6-features)
  - [7. Conclusion](#7-conclusion)

## 1. Introduction

This project is an implementation of the Huffman coding algorithm in Python. Huffman coding is a popular algorithm for lossless data compression. It assigns variable-length codes to input characters, with lengths based on the frequencies of corresponding characters. More frequent characters get shorter codes, while less frequent characters get longer codes, leading to an overall reduction in the number of bits required to represent the data.

This implementation demonstrates the core steps of the Huffman algorithm:

- Calculating character frequencies.
- Building a Huffman tree (a binary tree where leaves are characters and their frequencies).
- Generating Huffman codes by traversing the tree.
- Encoding an input string using the generated codes.
- Decoding the encoded string back to the original.

## 2. How the Code Works

The Python script (`main.py`) is structured as follows:

- **`Node` Class:** Represents a node in the Huffman tree. Each node stores its character (for leaf nodes), frequency, and references to its left and right children.
- **`build_huffman_tree(text, verbose=False)`:**
  1. Calculates the frequency of each character in the input `text`.
  2. Creates a leaf `Node` for each character and adds it to a min-priority queue (implemented using `heapq`).
  3. Iteratively extracts the two nodes with the minimum frequencies from the priority queue.
  4. Creates a new internal node with these two nodes as children and a frequency equal to the sum of their frequencies.
  5. Adds this new internal node back to the priority queue.
  6. This process continues until only one node (the root of the Huffman tree) remains in the queue.
- **`generate_huffman_codes_recursive(root_node, current_code, codes_dict, verbose=False)`:**
  - Recursively traverses the Huffman tree from the `root_node`.
  - Appends '0' to the `current_code` when moving to a left child and '1' when moving to a right child.
  - When a leaf node (character) is reached, the accumulated `current_code` is stored in the `codes_dict` for that character.
- **`get_huffman_codes(root_node, verbose=False)`:**
  - Initializes an empty dictionary for codes.
  - Calls `generate_huffman_codes_recursive` to populate the codes dictionary.
  - Handles a special case for single-node trees (e.g., input "aaa").
- **`huffman_encode(text, huffman_codes, verbose=False)`:**
  - Iterates through the input `text`.
  - Appends the Huffman code for each character (from `huffman_codes`) to create the `encoded_text`.
- **`huffman_decode(encoded_text, huffman_tree_root, verbose=False)`:**
  - Traverses the `huffman_tree_root` based on the bits in the `encoded_text`.
  - Moves left for a '0' and right for a '1'.
  - When a leaf node is reached, its character is appended to the `decoded_text`, and traversal restarts from the root for the next character.
- **Main Execution (`if __name__ == "__main__":`)**
  1. Prompts the user to enter a string.
  2. Builds the Huffman tree.
  3. Generates Huffman codes.
  4. Encodes the input string.
  5. Prints the original text, Huffman codes, encoded text, and compression statistics.
  6. Decodes the encoded text to verify the process.
  7. Includes an optional `--verbose` or `-v` command-line argument to display detailed steps of the algorithm OR  `--gui` or`-g` to run in the interactive graphical user mode in browser .
-

## 3. Requirements

- Python 3.x
- `rich` (for styled terminal output): `pip install rich`
- `graphviz` (optional, for tree visualization):
  - Python library: `pip install graphviz`
  - Graphviz software: [https://graphviz.org/download/](https://graphviz.org/download/)

No external libraries beyond standard Python modules (`heapq`, `collections.Counter`, `argparse`, `re`, `pathlib.Path`) are strictly required for the core Huffman encoding/decoding logic. `rich` enhances the display, and `graphviz` is needed only if you use the `--visualize` option.

## 4. How to Run

1. Save the code as `main.py` (or your preferred filename).
2. Open a terminal or command prompt.
3. Navigate to the directory where you saved the file.
4. Run the script using the Python interpreter:

    ```bash
    python main.py
    ```

5. The program will prompt you to: `Enter the string to encode:`
6. Type your desired string and press Enter.

### Verbose Mode

To see a detailed step-by-step execution of the algorithm, run the script with the `-v` or `--verbose` flag:

```bash
python main.py -v
```

### GUI Mode

To run interactive GUI mode, the `gui.py` file provides a graphical user interface (GUI) for the Huffman coding implementation using the Streamlit library. You can run the GUI in two ways:

1. Using Streamlit:
    ```bash
    streamlit run gui.py
    ```
2. Using the Python script with the `-g`  or `--gui` flag:
    ```bash
    python main.py -g
    ```

After running either command, open the provided URL in your web browser to access the GUI.

## 5. Example Output

```txt
Original Text: "BANANA BANDANA"

--- Huffman Codes ---
  Character: ' ', Frequency: 1, Code: 1111
  Character: 'A', Frequency: 6, Code: 0
  Character: 'B', Frequency: 2, Code: 110
  Character: 'D', Frequency: 1, Code: 1110
  Character: 'N', Frequency: 4, Code: 10
---------------------

Encoded Text: 1100100100111111001011100100

--- Compression Statistics ---
  Original length (ASCII, 8 bits/char): 112 bits
  Encoded length (Huffman):             28 bits
  Space saved:                          84 bits
  Compression ratio:                    75.00%
-----------------------------

Decoded Text: "BANANA BANDANA"

SUCCESS: Encoding and Decoding successful! Original text matches decoded text.
```

Huffman tree for the example above:

![BANANA BANDANA Huffman Tree](<docs/assets/BANANA BANDANA.svg>)

## 6. Features

- **Character Frequency Calculation:** Uses `collections.Counter` for efficient frequency counting.
- **Min-Priority Queue:** Employs `heapq` for managing nodes during tree construction.
- **Huffman Tree Construction:** Dynamically builds the optimal prefix code tree.
- **Encoding:** Converts input text to its Huffman-coded binary string.
- **Decoding:** Reconstructs the original text from the Huffman-coded string and the tree.
- **Compression Statistics:** Calculates and displays the original size, encoded size, space saved, and compression ratio.
- **Verbose Mode:** Provides detailed output for each step of the algorithm, useful for understanding and debugging.
- **Tree Visualization:** Generates a visual representation of the Huffman tree using Graphviz.
- **Custom Output Path:** Allows specifying a custom path for saving the visualization.
- **Visualization Format Selection:** Supports different output formats for the visualization (e.g., png, pdf, svg).
- **Handles Single Character/Single Node Trees:** Correctly encodes and decodes strings with only one unique character (e.g., "aaaaa") or very short strings.

## 7. Conclusion

This implementation successfully demonstrates the Huffman coding algorithm, providing a clear path from an input string to its compressed representation and back. The verbose mode is particularly helpful for educational purposes to trace the algorithm's logic.
