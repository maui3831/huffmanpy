import argparse
import subprocess
from collections import Counter
from rich import print

from huffman_encoder import build_huffman_tree, get_huffman_codes, huffman_encode
from huffman_decoder import huffman_decode
from visualization import visualize_huffman_tree


def main():
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
        "input_text_arg",
        type=str,
        nargs="?",
        help="Input text to be encoded. If not provided, the program will prompt for it.",
        default=None,
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Path (filename without extension) where to save the tree visualization. Directory will be created if it doesn't exist.",
        default=None,
    )
    parser.add_argument(
        "--format",
        type=str,
        choices=["png", "pdf", "svg", "jpg"],
        default="png",
        help="Format of the visualization output file.",
    )
    parser.add_argument(
        "-g",
        "--gui",
        action="store_true",
        help="Launch the Streamlit web interface instead of CLI mode",
    )

    args = parser.parse_args()

    # streamlit gui
    if args.gui:
        try:
            subprocess.run(["streamlit", "run", "gui.py"])
        except Exception as e:
            print(f"[bold red]Error launching GUI:[/bold red] {e}")
        return

    input_text = input("Enter the string to encode: ")

    if not input_text:
        print("[yellow]Input text is empty. Exiting.[/yellow]")
        return

    frequency = Counter(input_text)

    print(f'\n[bold magenta]Original Text:[/bold magenta] "{input_text}"')
    if args.verbose:
        print("[cyan]VERBOSE mode enabled.[/cyan]")

    # 1. Build Huffman Tree
    huffman_tree_root = build_huffman_tree(input_text, frequency, args.verbose)

    if huffman_tree_root:
        # Visualize the tree if requested
        if args.visualize:
            print("\nAttempting to visualize Huffman tree...")
            try:
                output_path = visualize_huffman_tree(
                    huffman_tree_root,
                    view=True,
                    output_file=args.output,
                    format=args.format,
                    input_text=input_text,
                )
                if output_path:
                    print(
                        f"\n[green]Huffman tree visualization saved to:[/green] {output_path}"
                    )
                else:
                    print("[yellow]Visualization was not generated.[/yellow]")
            except Exception as e:
                print(f"[bold red]Error during visualization process:[/bold red] {e}")

        # 2. Generate Huffman Codes
        huffman_codes = get_huffman_codes(huffman_tree_root, args.verbose)

        print("\n[bold blue]--- Huffman Codes ---[/bold blue]")
        if huffman_codes:
            for char, code in sorted(huffman_codes.items()):
                char_display = char if char.isprintable() else f"ASCII({ord(char)})"
                print(
                    f"  Character: '{char_display}', Frequency: {frequency[char]}, Code: {code}"
                )
        else:
            print("  No Huffman codes generated (e.g. empty tree).")
        print("[bold blue]---------------------[/bold blue]")

        # 3. Encode the text
        encoded_text = huffman_encode(input_text, huffman_codes, args.verbose)
        print(f"\n[bold magenta]Encoded Text:[/bold magenta] {encoded_text}")

        original_length_bits = len(input_text) * 8
        encoded_length_bits = len(encoded_text)

        # Calculate huffman table size (overhead)
        huffman_table_bits = 0
        for char, code in huffman_codes.items():
            # For each character: store character (8 bits) + code itself
            huffman_table_bits += 8 + len(code)

        # Total size including the table
        total_compressed_bits = encoded_length_bits + huffman_table_bits

        print("\n[bold blue]--- Compression Statistics ---[/bold blue]")
        print(f"  Original length (ASCII, 8 bits/char): {original_length_bits} bits")
        print(f"  Encoded text length:                  {encoded_length_bits} bits")
        print(f"  Huffman table size:                   {huffman_table_bits} bits")
        print(f"  Total compressed size:                {total_compressed_bits} bits")
        if original_length_bits > 0:
            space_saved = original_length_bits - total_compressed_bits
            # Calculate compression ratio based on total size including table
            compression_ratio = (
                (space_saved / original_length_bits * 100) if space_saved > 0 else 0
            )
            print(f"  Space saved:                          {space_saved} bits")
            print(f"  Compression ratio:                    {compression_ratio:.2f}%")
        print("[bold blue]-----------------------------[/bold blue]")

        # 4. Decode the text (for verification)
        decoded_text = huffman_decode(encoded_text, huffman_tree_root, args.verbose)
        print(f'\n[bold magenta]Decoded Text:[/bold magenta] "{decoded_text}"')

        if input_text == decoded_text:
            print(
                "\n[bold green]SUCCESS:[/bold green] Encoding and Decoding successful! Original text matches decoded text."
            )
        else:
            print(
                "\n[bold red]ERROR:[/bold red] Decoding failed! Original text does NOT match decoded text."
            )
    else:
        print(
            "[yellow]Could not build Huffman tree (e.g., empty input text or other error).[/yellow]"
        )


if __name__ == "__main__":
    main()
