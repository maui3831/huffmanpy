# Huffman Coding Implementation in Python

For Introduction to Artificial Intelligence
by AI Group 2

## 1. Introduction

This project is an implementation of the Huffman coding algorithm in Python. Huffman coding is a popular algorithm for lossless data compression. It assigns variable-length codes to input characters, with lengths based on the frequencies of corresponding characters. More frequent characters get shorter codes, while less frequent characters get longer codes, leading to an overall reduction in the number of bits required to represent the data.

This implementation demonstrates the core steps of the Huffman algorithm:

* Calculating character frequencies.
* Building a Huffman tree (a binary tree where leaves are characters and their frequencies).
* Generating Huffman codes by traversing the tree.
* Encoding an input string using the generated codes.
* Decoding the encoded string back to the original.

## 2. How the Code Works

The Python script (`main.py`) is structured as follows:

* **`Node` Class:** Represents a node in the Huffman tree. Each node stores its character (for leaf nodes), frequency, and references to its left and right children.
* **`build_huffman_tree(text, verbose=False)`:**
  1. Calculates the frequency of each character in the input `text`.
  2. Creates a leaf `Node` for each character and adds it to a min-priority queue (implemented using `heapq`).
  3. Iteratively extracts the two nodes with the minimum frequencies from the priority queue.
  4. Creates a new internal node with these two nodes as children and a frequency equal to the sum of their frequencies.
  5. Adds this new internal node back to the priority queue.
  6. This process continues until only one node (the root of the Huffman tree) remains in the queue.
* **`generate_huffman_codes_recursive(root_node, current_code, codes_dict, verbose=False)`:**
  * Recursively traverses the Huffman tree from the `root_node`.
  * Appends '0' to the `current_code` when moving to a left child and '1' when moving to a right child.
  * When a leaf node (character) is reached, the accumulated `current_code` is stored in the `codes_dict` for that character.
* **`get_huffman_codes(root_node, verbose=False)`:**
  * Initializes an empty dictionary for codes.
  * Calls `generate_huffman_codes_recursive` to populate the codes dictionary.
  * Handles a special case for single-node trees (e.g., input "aaa").
* **`huffman_encode(text, huffman_codes, verbose=False)`:**
  * Iterates through the input `text`.
  * Appends the Huffman code for each character (from `huffman_codes`) to create the `encoded_text`.
* **`huffman_decode(encoded_text, huffman_tree_root, verbose=False)`:**
  * Traverses the `huffman_tree_root` based on the bits in the `encoded_text`.
  * Moves left for a '0' and right for a '1'.
  * When a leaf node is reached, its character is appended to the `decoded_text`, and traversal restarts from the root for the next character.
* **Main Execution (`if __name__ == "__main__":`)**
  1. Prompts the user to enter a string.
  2. Builds the Huffman tree.
  3. Generates Huffman codes.
  4. Encodes the input string.
  5. Prints the original text, Huffman codes, encoded text, and compression statistics.
  6. Decodes the encoded text to verify the process.
  7. Includes an optional `--verbose` or `-v` command-line argument to display detailed steps of the algorithm.

## 3. Requirements

* Python 3.x

No external libraries beyond standard Python modules (`heapq`, `collections.Counter`, `argparse`) are required.

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

## 5. Example Output

```txt
Enter the string to encode: BCAADDDCCACACAC

Original Text: "BCAADDDCCACACAC"

--- Huffman Codes ---
  Character: 'A', Code: 10
  Character: 'B', Code: 1110
  Character: 'C', Code: 0
  Character: 'D', Code: 110
---------------------

Encoded Text: 11100101011011011000100100100

--- Compression Statistics ---
  Original length (ASCII, 8 bits/char): 120 bits
  Encoded length (Huffman):             30 bits
  Space saved:                          90 bits
  Compression ratio:                    75.00%
-----------------------------

Decoded Text: "BCAADDDCCACACAC"

SUCCESS: Encoding and Decoding successful! Original text matches decoded text.
```

## 6. Features

* **Character Frequency Calculation:** Uses `collections.Counter` for efficient frequency counting.
* **Min-Priority Queue:** Employs `heapq` for managing nodes during tree construction.
* **Huffman Tree Construction:** Dynamically builds the optimal prefix code tree.
* **Encoding:** Converts input text to its Huffman-coded binary string.
* **Decoding:** Reconstructs the original text from the Huffman-coded string and the tree.
* **Compression Statistics:** Calculates and displays the original size, encoded size, space saved, and compression ratio.
* **Verbose Mode:** Provides detailed output for each step of the algorithm, useful for understanding and debugging.
* **Handles Single Character/Single Node Trees:** Correctly encodes and decodes strings with only one unique character (e.g., "aaaaa") or very short strings.

## 7. Conclusion

This implementation successfully demonstrates the Huffman coding algorithm, providing a clear path from an input string to its compressed representation and back. The verbose mode is particularly helpful for educational purposes to trace the algorithm's logic.
