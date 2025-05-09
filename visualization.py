from pathlib import Path
import re
from rich import print


def visualize_huffman_tree(
    root_node, view=True, output_file=None, format="png", input_text=None
):
    """
    Visualizes the Huffman tree using Graphviz.

    Args:
        root_node (Node): The root node of the Huffman tree.
        view (bool): If True, opens the generated graph image.
        output_file (str, optional): Path where the visualization should be saved.
                                     If None, a file will be created in the visualization folder.
        format (str): The format of the output file (png, pdf, etc.)
        input_text (str, optional): Original input text to use for the filename.

    Returns:
        str: The path to the created visualization file, or None on error.
    """
    try:
        from graphviz import Digraph
    except ImportError:
        print(
            "[bold red]Error:[/bold red] The [cyan]graphviz[/cyan] package is required for tree visualization."
        )
        print("Install it using: [green]pip install graphviz[/green]")
        print(
            "You may also need to install the Graphviz software: [blue]https://graphviz.org/download/[/blue]"
        )
        return None

    if root_node is None:
        return None

    # Check if output_file is provided
    if output_file is None:
        vis_dir = Path.cwd() / "huffman_visualizations"
        vis_dir.mkdir(parents=True, exist_ok=True)

        if input_text:
            clean_text = re.sub(r'[\\/*?:"<>|]', "_", input_text)
            if len(clean_text) > 30:
                clean_text = clean_text[:27] + "..."
        else:
            clean_text = "huffman_tree"

        filename_base = clean_text
        output_file_path = vis_dir / filename_base

        # Check if a visualization for this input already exists
        existing_file = list(vis_dir.glob(f"{filename_base}.{format}"))
        if existing_file:
            existing_path = str(existing_file[0])
            print(f"[green]Reusing existing visualization:[/green] {existing_path}")
            if view:
                import os

                os.startfile(existing_path) if os.name == "nt" else print(
                    f"[yellow]Cannot automatically open file on this OS. File is at: {existing_path}[/yellow]"
                )
            return existing_path
    else:
        output_file_path = Path(output_file)

    dot = Digraph(comment="Huffman Tree", format=format)
    dot.attr(rankdir="TB")

    node_counter = [0]

    def add_nodes_edges(node, parent_id=None):
        if node is None:
            return

        current_id = str(node_counter[0])
        node_counter[0] += 1

        if node.char is not None:
            char_repr = (
                node.char if node.char.isprintable() else f"ASCII({ord(node.char)})"
            )
            label = f"'{char_repr}': {node.freq}"
            shape = "box"
        else:
            label = f"freq={node.freq}"
            shape = "ellipse"

        dot.node(current_id, label, shape=shape)

        if parent_id is not None:
            edge_label = "0" if parent_id[1] == "L" else "1"
            dot.edge(parent_id[0], current_id, label=edge_label)

        add_nodes_edges(node.left, (current_id, "L"))
        add_nodes_edges(node.right, (current_id, "R"))

    add_nodes_edges(root_node)

    try:
        # Graphviz render automatically adds the format extension
        # It expects filename without extension for the 'filename' argument
        rendered_path = dot.render(
            filename=str(output_file_path.name),
            directory=str(output_file_path.parent),
            view=view,
            cleanup=True,
            format=format,
        )
        return rendered_path
    except Exception as e:
        print(f"[bold red]Error rendering graph with Graphviz:[/bold red] {e}")
        if (
            "make sure the Graphviz executables are on your systems' PATH"
            in str(e).lower()
        ):
            print(
                "This might mean Graphviz is not installed correctly or not in your system PATH."
            )
            print(
                "Download and install from: [blue]https://graphviz.org/download/[/blue]"
            )
        return None
