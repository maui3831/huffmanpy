# huffman_project/main.py
import argparse
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
    args = parser.parse_args()

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
                output_path, is_reused = visualize_huffman_tree(
                    huffman_tree_root,
                    view=True,
                    output_file=args.output,
                    format=args.format,
                    input_text=input_text,
                )
                if output_path:
                    if is_reused:
                        print(
                            f"\n[green]Reusing existing visualization:[/green] {output_path}"
                        )
                    else:
                        print(
                            f"\n[green]Huffman tree visualization saved to:[/green] {output_path}"
                        )
                else:
                    print("[yellow]Visualization was not generated.[/yellow]")
            except (
                Exception
            ) as e:  # Catch any unexpected errors during visualization call
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

        print("\n[bold blue]--- Compression Statistics ---[/bold blue]")
        print(f"  Original length (ASCII, 8 bits/char): {original_length_bits} bits")
        print(f"  Encoded length (Huffman):             {encoded_length_bits} bits")
        if original_length_bits > 0:
            space_saved = original_length_bits - encoded_length_bits
            compression_ratio = (
                (space_saved / original_length_bits * 100)
                if original_length_bits > 0
                else 0
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
