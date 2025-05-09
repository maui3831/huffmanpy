from rich import print


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

    decoded_chars = []
    current_node = huffman_tree_root

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

        if current_node.char is not None:
            decoded_chars.append(current_node.char)
            if verbose and i < 20:
                print(
                    f"VERBOSE: Found character '{current_node.char}'. Resetting to root."
                )
            current_node = huffman_tree_root

    final_decoded_string = "".join(decoded_chars)
    print("VERBOSE: ----------------------") if verbose else None
    return final_decoded_string
