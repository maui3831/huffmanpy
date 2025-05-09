import heapq
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

    def __repr__(self):
        return f"Node(char='{self.char}', freq={self.freq})"


def build_huffman_tree(text, frequency, verbose=False):
    """
    Builds the Huffman tree for the given text.

    Args:
        text (str): The input string to be encoded.
        frequency (Counter): A Counter object with character frequencies.
        verbose (bool): If True, prints detailed steps.

    Returns:
        Node: The root node of the Huffman tree, or None if text is empty.
    """
    if not text:
        if verbose:
            print("VERBOSE: Input text is empty. Cannot build Huffman tree.")
        return None

    if verbose:
        print("\nVERBOSE: ---- Character Frequencies ----")
        for char, freq in sorted(frequency.items()):
            print(f"VERBOSE: Character '{char}': {freq}")

    priority_queue = [Node(char, freq) for char, freq in frequency.items()]
    heapq.heapify(priority_queue)

    if verbose:
        print("\nVERBOSE: ---- Initial Priority Queue (Min-Heap) ----")
        for node in heapq.nsmallest(len(priority_queue), priority_queue):
            print(f"VERBOSE: {node}")
        print("VERBOSE: ------------------------------------------")

    while len(priority_queue) > 1:
        left_child = heapq.heappop(priority_queue)
        right_child = heapq.heappop(priority_queue)

        if verbose:
            print("\nVERBOSE: ---- Tree Building Step ----")
            print(f"VERBOSE: Popped Left Child: {left_child}")
            print(f"VERBOSE: Popped Right Child: {right_child}")

        merged_freq = left_child.freq + right_child.freq
        internal_node = Node(None, merged_freq)
        internal_node.left = left_child
        internal_node.right = right_child

        if verbose:
            print(
                f"VERBOSE: Created Internal Node: {internal_node} (Left: '{left_child.char}', Right: '{right_child.char}')"
            )

        heapq.heappush(priority_queue, internal_node)

        if verbose:
            print(f"VERBOSE: Priority Queue after pushing {internal_node}:")
            for node in heapq.nsmallest(len(priority_queue), priority_queue):
                print(f"VERBOSE:   {node}")
            print("VERBOSE: -----------------------------")

    if verbose and priority_queue:
        print("\nVERBOSE: ---- Huffman Tree Built ----")
        print(f"VERBOSE: Root of the tree: {priority_queue[0]}")
        print("VERBOSE: ---------------------------")
    return priority_queue[0] if priority_queue else None


def _generate_huffman_codes_recursive(
    root_node, current_code, codes_dict, verbose=False
):
    """
    Recursively traverses the Huffman tree to generate codes for each character.
    (Internal helper function)
    """
    if root_node is None:
        return

    if root_node.char is not None:
        final_code = current_code if current_code else "0"
        codes_dict[root_node.char] = final_code
        if verbose:
            print(
                f"VERBOSE: Generated Code - Character: '{root_node.char}', Path: {final_code if final_code else '(root is leaf)'}"
            )
        return

    if verbose:
        print(
            f"VERBOSE: Traversing Left from Node(freq={root_node.freq}). Current code: {current_code} -> {current_code + '0'}"
        )
    _generate_huffman_codes_recursive(
        root_node.left, current_code + "0", codes_dict, verbose
    )

    if verbose:
        print(
            f"VERBOSE: Traversing Right from Node(freq={root_node.freq}). Current code: {current_code} -> {current_code + '1'}"
        )
    _generate_huffman_codes_recursive(
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

    _generate_huffman_codes_recursive(root_node, "", codes, verbose)
    print("VERBOSE: ---------------------------------") if verbose else None
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
    encoded_text = []
    for i, char in enumerate(text):
        code = huffman_codes.get(char)
        if code is None:
            raise ValueError(f"Character '{char}' not found in Huffman codes.")
        encoded_text.append(code)
        if verbose and i < 5:
            current_encoded_preview = "".join(encoded_text)
            print(
                f"VERBOSE: Encoding '{char}' to '{code}'. Current encoded: ...{current_encoded_preview[-20:]}"
            )
    print("VERBOSE: ----------------------") if verbose else None

    final_encoded_text = "".join(encoded_text)
    return final_encoded_text
