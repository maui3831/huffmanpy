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
    - [Command-Line Interface (CLI)](#command-line-interface-cli)
    - [Web Interface (Streamlit GUI)](#web-interface-streamlit-gui)
    - [Verbose Mode](#verbose-mode)
    - [GUI Mode](#gui-mode)
  - [5. Example Output](#5-example-output)
  - [6. Features](#6-features)
  - [7. Conclusion](#7-conclusion)

## 1. Introduction

This project is an implementation of the Huffman coding algorithm in Python. Huffman coding is a popular algorithm for lossless data compression. It assigns variable-length codes to input characters, with lengths based on the frequencies of corresponding characters. More frequent characters get shorter codes, while less frequent characters get longer codes, leading to an overall reduction in the number of bits required to represent the data.

This implementation demonstrates the core steps of the Huffman algorithm and provides both a command-line interface (CLI) and an interactive web interface using Streamlit.

The core logic includes:

- Calculating character frequencies.
- Building a Huffman tree (a binary tree where leaves are characters and their frequencies).
- Generating Huffman codes by traversing the tree.
- Encoding an input string using the generated codes.
- Decoding the encoded string back to the original.
- Visualizing the Huffman tree.

## 2. How the Code Works

The project is structured into several Python scripts:

- **`huffman_encoder.py` & `huffman_decoder.py`:**
  - **`Node` Class:** Represents a node in the Huffman tree. Each node stores its character (for leaf nodes), frequency, and references to its left and right children.
  - **`build_huffman_tree(text, frequency, verbose=False)`:**
    1. Calculates the frequency of each character in the input `text`.
    2. Creates a leaf `Node` for each character and adds it to a min-priority queue (implemented using `heapq`).
    3. Iteratively extracts the two nodes with the minimum frequencies from the priority queue.
    4. Creates a new internal node with these two nodes as children and a frequency equal to the sum of their frequencies.
    5. Adds this new internal node back to the priority queue.
    6. This process continues until only one node (the root of the Huffman tree) remains in the queue.
  - **`_generate_huffman_codes_recursive(root_node, current_code, codes_dict, verbose=False)`:** (Internal helper)
    - Recursively traverses the Huffman tree from the `root_node`.
    - Appends '0' to the `current_code` when moving to a left child and '1' when moving to a right child.
    - When a leaf node (character) is reached, the accumulated `current_code` is stored in the `codes_dict` for that character.
  - **`get_huffman_codes(root_node, verbose=False)`:**
    - Initializes an empty dictionary for codes.
    - Calls `_generate_huffman_codes_recursive` to populate the codes dictionary.
    - Handles a special case for single-node trees (e.g., input "aaa").
  - **`huffman_encode(text, huffman_codes, verbose=False)`:**
    - Iterates through the input `text`.
    - Appends the Huffman code for each character (from `huffman_codes`) to create the `encoded_text`.
  - **`huffman_decode(encoded_text, huffman_tree_root, verbose=False)`:**
    - Traverses the `huffman_tree_root` based on the bits in the `encoded_text`.
    - Moves left for a '0' and right for a '1'.
    - When a leaf node is reached, its character is appended to the `decoded_text`, and traversal restarts from the root for the next character.
- **`visualization.py`:**
  - **`visualize_huffman_tree(...)`:** Generates a visual representation of the Huffman tree using Graphviz and can reuse existing visualizations for the same input.
- **`main.py` (CLI):**
  1. Parses command-line arguments (input text, verbose mode, visualization options).
  2. If no input text is provided via arguments, prompts the user to enter a string.
  3. Builds the Huffman tree.
  4. Generates Huffman codes.
  5. Encodes the input string.
  6. Prints the original text, Huffman codes, encoded text, and compression statistics.
  7. Decodes the encoded text to verify the process.
  8. Optionally visualizes the tree if requested.
- **`gui.py` (Web Interface):**
  1. Uses Streamlit to create an interactive web application.
  2. Allows users to input text directly or upload a text file.
  3. Performs Huffman encoding and decoding.
  4. Displays the encoded text, decoded text (snippet), Huffman codes in a table (using Pandas), compression statistics, and the Huffman tree visualization.
  5. Offers a verbose mode to show detailed processing logs.

## 3. Requirements

- Python 3.x
- `rich` (for styled terminal output in CLI): `pip install rich`
- `graphviz` (optional, for tree visualization):
  - Python library: `pip install graphviz`
  - Graphviz software: [https://graphviz.org/download/](https://graphviz.org/download/)
- `streamlit` (for the web interface): `pip install streamlit`
- `pandas` (for displaying tables in the web interface): `pip install pandas`

Core Huffman logic (`huffman_encoder.py`, `huffman_decoder.py`) primarily uses standard Python modules (`heapq`, `collections.Counter`). `rich` enhances the CLI display, `graphviz` is needed for tree visualization, and `streamlit` and `pandas` are required for the GUI.

## 4. How to Run

1. Ensure all requirements are installed (see [section 3](#3-requirements)).
2. Open a terminal or command prompt.
3. Navigate to the directory where you saved the files.

### Command-Line Interface (CLI)

Run the `main.py` script:

```bash
python main.py
```
The program will prompt you to: `Enter the string to encode:`
Type your desired string and press Enter.

You can also provide the input text directly as an argument:
```bash
python main.py "your text here"
```

**CLI Options:**
- `-v` or `--verbose`: Enable verbose output for debugging.
- `--visualize`: Visualize the Huffman tree (requires Graphviz).
- `--output <filename>`: Specify the filename (without extension) for the saved tree visualization.
- `--format <format>`: Specify the format for the visualization (e.g., `png`, `svg`, `pdf`).
- `--gui`: Launch the Streamlit web interface instead (see below).

### Web Interface (Streamlit GUI)

To launch the interactive web interface, run:

```bash
streamlit run gui.py
```
Alternatively, you can use the `--gui` flag with `main.py`:
```bash
python main.py --gui
```
This will open the Huffman Coding application in your web browser. You can then input text or upload a file to see the compression in action.

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

**(CLI Output Example)**
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
- **Verbose Mode (CLI & GUI):** Provides detailed output for each step of the algorithm, useful for understanding and debugging.
- **Tree Visualization:** Generates a visual representation of the Huffman tree using Graphviz, viewable in the GUI or saved as a file from the CLI.
- **Reusing Existing Visualizations:** The visualization function checks for and reuses previously generated tree images for the same input to save time.
- **Custom Output Path & Format (CLI):** Allows specifying a custom path and format for saving the visualization.
- **Handles Single Character/Single Node Trees:** Correctly encodes and decodes strings with only one unique character (e.g., "aaaaa") or very short strings.
- **Interactive Web Interface (Streamlit):** Provides a user-friendly GUI for text input, file upload, and viewing results.
- **Tabular Display of Huffman Codes (GUI):** Shows character frequencies and their corresponding Huffman codes in a clear table format using Pandas.

## 7. Conclusion

This implementation successfully demonstrates the Huffman coding algorithm, providing a clear path from an input string to its compressed representation and back. The availability of both a CLI with detailed verbose options and an interactive Streamlit GUI makes it a versatile tool for learning about and experimenting with Huffman coding. The verbose mode is particularly helpful for educational purposes to trace the algorithm's logic.
