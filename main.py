import heapq
from collections import Counter
import argparse
from pathlib import Path
import re
import datetime
from rich import print


class Node:
    """
    Represents a node in the Huffman tree.
    Each node stores its character (for leaf nodes), frequency,
    and references to its left and right children.
    """

    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    # Define comparison methods for the priority queue (min-heap)
    def __lt__(self, other):
        if other is None:
            return False  
        if not isinstance(other, Node):
            return NotImplemented
        return self.freq < other.freq

    def __eq__(self, other):
        if other is None:
            return False
        if not isinstance(other, Node):
            return False
        return self.freq == other.freq

    # For better representation, especially in verbose mode
    def __repr__(self):
        return f"Node(char='{self.char}', freq={self.freq})"


def build_huffman_tree(text, verbose=False):
    """
    Builds the Huffman tree for the given text.

    Args:
        text (str): The input string to be encoded.
        verbose (bool): If True, prints detailed steps.

    Returns:
        Node: The root node of the Huffman tree, or None if text is empty.
    """
    if not text:
        if verbose:
            print("VERBOSE: Input text is empty. Cannot build Huffman tree.")
        return None

    # 1. Calculate frequency of each character
    frequency = Counter(text)
    if verbose:
        print("\nVERBOSE: ---- Character Frequencies ----")
        for char, freq in sorted(frequency.items()):
            print(f"VERBOSE: Character '{char}': {freq}")

    # 2. Create a leaf node for each character and add it to a min-priority queue
    priority_queue = [Node(char, freq) for char, freq in frequency.items()]
    heapq.heapify(priority_queue)  

    if verbose:
        print("\nVERBOSE: ---- Initial Priority Queue (Min-Heap) ----")
        for node in heapq.nsmallest(len(priority_queue), priority_queue):
            print(f"VERBOSE: {node}")
        print("VERBOSE: ------------------------------------------")

    # 3. Build the tree
    while len(priority_queue) > 1:
        left_child = heapq.heappop(priority_queue)
        right_child = heapq.heappop(priority_queue)

        if verbose:
            print("\nVERBOSE: ---- Tree Building Step ----")
            print(f"VERBOSE: Popped Left Child: {left_child}")
            print(f"VERBOSE: Popped Right Child: {right_child}")

        # Create a new internal node with these two nodes as children
        merged_freq = left_child.freq + right_child.freq
        internal_node = Node(None, merged_freq)
        internal_node.left = left_child
        internal_node.right = right_child

        if verbose:
            print(
                f"VERBOSE: Created Internal Node: {internal_node} (Left: '{left_child.char}', Right: '{right_child.char}')"
            )

        # Add the new node to the priority queue
        heapq.heappush(priority_queue, internal_node)

        if verbose:
            print(f"VERBOSE: Priority Queue after pushing {internal_node}:")
            for node in heapq.nsmallest(
                len(priority_queue), priority_queue
            ):  # Show sorted view
                print(f"VERBOSE:   {node}")
            print("VERBOSE: -----------------------------")

    # The remaining node is the root of the Huffman tree
    if verbose and priority_queue:
        print("\nVERBOSE: ---- Huffman Tree Built ----")
        print(f"VERBOSE: Root of the tree: {priority_queue[0]}")
        print("VERBOSE: ---------------------------")
    return priority_queue[0] if priority_queue else None


def generate_huffman_codes_recursive(
    root_node, current_code, codes_dict, verbose=False
):
    """
    Recursively traverses the Huffman tree to generate codes for each character.

    Args:
        root_node (Node): The current node in the Huffman tree.
        current_code (str): The binary code accumulated so far on the path from the root.
        codes_dict (dict): A dictionary to store the generated Huffman codes.
        verbose (bool): If True, prints detailed steps.
    """
    if root_node is None:
        return

    # Store the current code for this character.
    if root_node.char is not None:
        final_code = current_code if current_code else "0"  
        codes_dict[root_node.char] = final_code
        if verbose:
            print(
                f"VERBOSE: Generated Code - Character: '{root_node.char}', Path: {final_code if final_code else '(root is leaf)'}"
            )
        return

    # Traverse left (assign '0')
    if verbose:
        print(
            f"VERBOSE: Traversing Left from Node(freq={root_node.freq}). Current code: {current_code} -> {current_code + '0'}"
        )
    generate_huffman_codes_recursive(
        root_node.left, current_code + "0", codes_dict, verbose
    )

    # Traverse right (assign '1')
    if verbose:
        print(
            f"VERBOSE: Traversing Right from Node(freq={root_node.freq}). Current code: {current_code} -> {current_code + '1'}"
        )
    generate_huffman_codes_recursive(
        root_node.right, current_code + "1", codes_dict, verbose
    )


def get_huffman_codes(root_node, verbose=False):
    """
    Generates Huffman codes for all characters in the tree.

    Args:
        root_node (Node): The root node of the Huffman tree.
        verbose (bool): If True, prints detailed steps.

    Returns:
        dict: A dictionary mapping characters to their Huffman codes.
    """
    if root_node is None:
        if verbose:
            print("VERBOSE: Root node is None. Cannot generate codes.")
        return {}

    codes = {}
    if verbose:
        print("\nVERBOSE: ---- Generating Huffman Codes ----")

    # Special case: if the tree has only one node (e.g., input string "aaa")
    # This means the root is a leaf node.
    if (
        root_node.char is not None
        and root_node.left is None
        and root_node.right is None
    ):
        codes[root_node.char] = "0"
        if verbose:
            print(
                f"VERBOSE: Single node tree. Character: '{root_node.char}', Code: '0'"
            )
        return codes

    generate_huffman_codes_recursive(root_node, "", codes, verbose)
    if verbose:
        print("VERBOSE: ---------------------------------")
    return codes


def huffman_encode(text, huffman_codes, verbose=False):
    """
    Encodes the input text using the generated Huffman codes.

    Args:
        text (str): The original string.
        huffman_codes (dict): A dictionary mapping characters to their Huffman codes.
        verbose (bool): If True, prints detailed steps.

    Returns:
        str: The Huffman encoded string.
    """
    if verbose:
        print("\nVERBOSE: ---- Encoding Text ----")
    encoded_text = ""
    for i, char in enumerate(text):
        code = huffman_codes.get(char)
        if code is None:
            # This should not happen if the tree was built from the text
            raise ValueError(f"Character '{char}' not found in Huffman codes.")
        encoded_text += code
        if verbose and i < 5:  
            print(
                f"VERBOSE: Encoding '{char}' to '{code}'. Current encoded: ...{encoded_text[-20:]}"
            )
    if verbose:
        print(
            f"VERBOSE: Final Encoded Text (first 100 chars): {encoded_text[:100]}{'...' if len(encoded_text) > 100 else ''}"
        )
        print("VERBOSE: ----------------------")
    return encoded_text


def huffman_decode(encoded_text, huffman_tree_root, verbose=False):
    """
    Decodes the Huffman encoded text using the Huffman tree.

    Args:
        encoded_text (str): The Huffman encoded string.
        huffman_tree_root (Node): The root of the Huffman tree.
        verbose (bool): If True, prints detailed steps.

    Returns:
        str: The original decoded string.
    """
    if not encoded_text or huffman_tree_root is None:
        if verbose:
            print("VERBOSE: Encoded text is empty or tree root is None. Cannot decode.")
        return ""

    if verbose:
        print("\nVERBOSE: ---- Decoding Text ----")

    decoded_text = []
    current_node = huffman_tree_root

    # Handle single node tree (root is a leaf)
    if (
        current_node.char is not None
        and current_node.left is None
        and current_node.right is None
    ):
        if all(bit == "0" for bit in encoded_text): 
            decoded_string = current_node.char * len(encoded_text)
            if verbose:
                print(
                    f"VERBOSE: Single-node tree decoding. Decoded to: {decoded_string[:100]}{'...' if len(decoded_string) > 100 else ''}"
                )
            return decoded_string
        else:
            raise ValueError("Invalid code for single-node tree during decoding.")

    for i, bit in enumerate(encoded_text):
        if bit == "0":
            current_node = current_node.left
            if verbose and i < 20:
                print(
                    f"VERBOSE: Bit '{bit}' -> Traversing Left. Current node: {current_node}"
                )
        elif bit == "1":
            current_node = current_node.right
            if verbose and i < 20:
                print(
                    f"VERBOSE: Bit '{bit}' -> Traversing Right. Current node: {current_node}"
                )
        else:
            raise ValueError(f"Invalid bit '{bit}' in encoded string.")

        if current_node is None: 
            raise ValueError("Invalid path in Huffman tree during decoding.")

        if current_node.char is not None:  # Reached a leaf node
            decoded_text.append(current_node.char)
            if verbose and i < 20:
                print(
                    f"VERBOSE: Found character '{current_node.char}'. Resetting to root."
                )
            current_node = huffman_tree_root  

    final_decoded_string = "".join(decoded_text)
    if verbose:
        print(
            f"VERBOSE: Final Decoded Text (first 100 chars): {final_decoded_string[:100]}{'...' if len(final_decoded_string) > 100 else ''}"
        )
        print("VERBOSE: ----------------------")
    return final_decoded_string


def visualize_huffman_tree(
    root_node, view=True, output_file=None, format="png", verbose=False, input_text=None
):
    """
    Visualizes the Huffman tree using Graphviz.

    Args:
        root_node (Node): The root node of the Huffman tree.
        view (bool): If True, opens the generated graph image.
        output_file (str, optional): Path where the visualization should be saved.
                                     If None, a file will be created in the visualization folder.
        format (str): The format of the output file (png, pdf, etc.)
        verbose (bool): If True, prints detailed steps.
        input_text (str, optional): Original input text to use for the filename.

    Returns:
        str: The path to the created visualization file.
    """
    try:
        from graphviz import Digraph
    except ImportError:
        print("Error: The graphviz package is required for tree visualization.")
        print("Install it using: pip install graphviz")
        print(
            "You may also need to install the Graphviz software: https://graphviz.org/download/"
        )
        return None

    if root_node is None:
        if verbose:
            print("VERBOSE: Root node is None. Cannot visualize tree.")
        return None

    if verbose:
        print("\nVERBOSE: ---- Visualizing Huffman Tree ----")

    # Create a new directed graph
    dot = Digraph(comment="Huffman Tree", format=format)
    dot.attr(rankdir="TB")  # Top to bottom layout

    # Counter for unique node IDs
    node_counter = [0]

    def add_nodes_edges(node, parent_id=None):
        if node is None:
            return

        # Create a unique ID for this node
        current_id = str(node_counter[0])
        node_counter[0] += 1

        # Prepare label text
        if node.char is not None:
            # For leaf nodes, show character and frequency
            char_repr = (
                node.char if node.char.isprintable() else f"ASCII({ord(node.char)})"
            )
            label = f"'{char_repr}': {node.freq}"
        else:
            # For internal nodes, just show frequency
            label = f"freq={node.freq}"

        # Add the node to the graph
        shape = "box" if node.char is not None else "ellipse"  # Make leaf nodes boxes
        dot.node(current_id, label, shape=shape)

        # If this is not the root, connect it to its parent
        if parent_id is not None:
            # Label the edge with 0 for left child, 1 for right child
            edge_label = "0" if parent_id[1] == "L" else "1"
            dot.edge(parent_id[0], current_id, label=edge_label)

        # Recursively add children
        add_nodes_edges(node.left, (current_id, "L"))
        add_nodes_edges(node.right, (current_id, "R"))

    # Start building the graph from the root
    add_nodes_edges(root_node)

    # Determine the output file path
    if output_file is None:
        # Create visualization directory if it doesn't exist
        vis_dir = Path.cwd() / "huffman_visualizations"
        vis_dir.mkdir(parents=True, exist_ok=True)

        # Generate filename from input text if provided
        if input_text:
            # Clean and truncate the input text for a valid filename
            # Remove invalid filename characters and replace with underscore
            clean_text = re.sub(r'[\\/*?:"<>|]', "_", input_text)
            # Truncate if too long (max 30 chars)
            if len(clean_text) > 30:
                clean_text = clean_text[:27] + "..."
        else:
            clean_text = "huffman_tree"

        # Add timestamp for uniqueness
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{clean_text}_{timestamp}"

        output_file = str(vis_dir / filename)

    # Render the graph to file
    output_path = dot.render(filename=output_file, view=view, cleanup=True)

    if verbose:
        print(f"VERBOSE: Tree visualization saved to {output_path}")
        print("VERBOSE: --------------------------------------")

    return output_path


# --- Main Execution ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Huffman Coding Algorithm Implementation"
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose output for debugging.",
    )
    parser.add_argument(
        "--visualize",
        action="store_true",
        help="Visualize the Huffman tree (requires graphviz).",
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Path where to save the tree visualization.",
        default=None,
    )
    parser.add_argument(
        "--format",
        type=str,
        choices=["png", "pdf", "svg", "jpg"],
        default="png",
        help="Format of the visualization output file.",
    )
    # We will get the input string via input() prompt, not as a command-line argument here.
    args = parser.parse_args()

    input_text = input("Enter the string to encode: ")

    if not input_text:
        print("Input text is empty. Exiting.")
    else:
        print(f'\nOriginal Text: "{input_text}"')
        if args.verbose:
            print("VERBOSE mode enabled.")

        # Calculate character frequencies for display
        char_frequencies = Counter(input_text)

        # 1. Build Huffman Tree
        huffman_tree_root = build_huffman_tree(input_text, args.verbose)

        if huffman_tree_root:
            # Visualize the tree if requested
            if args.visualize:
                try:
                    output_path = visualize_huffman_tree(
                        huffman_tree_root,
                        output_file=args.output,
                        format=args.format,
                        verbose=args.verbose,
                        input_text=input_text,  # Pass the input_text for filename generation
                    )
                    if output_path:
                        print(f"\nHuffman tree visualization saved to: {output_path}")
                except Exception as e:
                    print(f"Error visualizing Huffman tree: {e}")

            # 2. Generate Huffman Codes
            huffman_codes = get_huffman_codes(huffman_tree_root, args.verbose)

            print("\n--- Huffman Codes ---")
            for char_code_pair in sorted(
                huffman_codes.items()
            ):  # Sort for consistent output
                print(f"  Character: '{char_code_pair[0]}', Code: {char_code_pair[1]}")
            print("---------------------")

            # 3. Encode the text
            encoded_text = huffman_encode(input_text, huffman_codes, args.verbose)
            print(f"\nEncoded Text: {encoded_text}")

            original_length_bits = (
                len(input_text) * 8
            )  
            encoded_length_bits = len(encoded_text)

            print("\n--- Compression Statistics ---")
            print(
                f"  Original length (ASCII, 8 bits/char): {original_length_bits} bits"
            )
            print(f"  Encoded length (Huffman):             {encoded_length_bits} bits")
            if original_length_bits > 0:
                compression_ratio = (
                    (original_length_bits - encoded_length_bits)
                    / original_length_bits
                    * 100
                )
                space_saved = original_length_bits - encoded_length_bits
                print(f"  Space saved:                          {space_saved} bits")
                print(
                    f"  Compression ratio:                    {compression_ratio:.2f}%"
                )
            print("-----------------------------")

            # 4. Decode the text (for verification)
            decoded_text = huffman_decode(encoded_text, huffman_tree_root, args.verbose)
            print(f'\nDecoded Text: "{decoded_text}"')

            if input_text == decoded_text:
                print(
                    "\nSUCCESS: Encoding and Decoding successful! Original text matches decoded text."
                )
            else:
                print(
                    "\nERROR: Decoding failed! Original text does NOT match decoded text."
                )
        else:
            print(
                "Could not build Huffman tree (e.g., empty input text or other error)."
            )

